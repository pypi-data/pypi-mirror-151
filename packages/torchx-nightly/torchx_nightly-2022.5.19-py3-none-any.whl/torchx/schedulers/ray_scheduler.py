# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import dataclasses
import json
import logging
import os
import time
from dataclasses import dataclass, field
from datetime import datetime
from shutil import copy2, copytree, rmtree
from tempfile import mkdtemp
from typing import Any, cast, Dict, List, Mapping, Optional, Set, Type  # noqa

from torchx.schedulers.api import (
    AppDryRunInfo,
    AppState,
    DescribeAppResponse,
    Scheduler,
    split_lines,
    Stream,
)
from torchx.schedulers.ids import make_unique
from torchx.schedulers.ray.ray_common import RayActor, TORCHX_RANK0_HOST
from torchx.specs import AppDef, macros, NONE, ReplicaStatus, Role, RoleStatus, runopts
from typing_extensions import TypedDict


try:
    from ray.autoscaler import sdk as ray_autoscaler_sdk
    from ray.dashboard.modules.job.common import JobStatus
    from ray.dashboard.modules.job.sdk import JobSubmissionClient

    _has_ray = True

except ImportError:
    _has_ray = False


def has_ray() -> bool:
    """Indicates whether Ray is installed in the current Python environment."""
    return _has_ray


class RayOpts(TypedDict, total=False):
    cluster_config_file: Optional[str]
    cluster_name: Optional[str]
    dashboard_address: Optional[str]
    working_dir: Optional[str]
    requirements: Optional[str]


if _has_ray:

    _logger: logging.Logger = logging.getLogger(__name__)

    _ray_status_to_torchx_appstate: Dict[JobStatus, AppState] = {
        JobStatus.PENDING: AppState.PENDING,
        JobStatus.RUNNING: AppState.RUNNING,
        JobStatus.SUCCEEDED: AppState.SUCCEEDED,
        JobStatus.FAILED: AppState.FAILED,
        JobStatus.STOPPED: AppState.CANCELLED,
    }

    class _EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o: RayActor):  # pyre-ignore[3]
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)

    def serialize(
        actors: List[RayActor], dirpath: str, output_filename: str = "actors.json"
    ) -> None:
        actors_json = json.dumps(actors, cls=_EnhancedJSONEncoder)
        with open(os.path.join(dirpath, output_filename), "w") as tmp:
            json.dump(actors_json, tmp)

    @dataclass
    class RayJob:
        """Represents a job that should be run on a Ray cluster.

        Attributes:
            app_id:
                The unique ID of the application (a.k.a. job).
            cluster_config_file:
                The Ray cluster configuration file.
            cluster_name:
                The cluster name to use.
            dashboard_address:
                The existing dashboard IP address to connect to
            working_dir:
            The working directory to copy to the cluster
            requirements:
                The libraries to install on the cluster per requirements.txt
            actors:
                The Ray actors which represent the job to be run. This attribute is
                dumped to a JSON file and copied to the cluster where `ray_main.py`
                uses it to initiate the job.
        """

        app_id: str
        cluster_config_file: Optional[str] = None
        cluster_name: Optional[str] = None
        dashboard_address: Optional[str] = None
        working_dir: Optional[str] = None
        requirements: Optional[str] = None
        actors: List[RayActor] = field(default_factory=list)

    class RayScheduler(Scheduler[RayOpts]):
        """
        **Config Options**

        .. runopts::
            class: torchx.schedulers.ray_scheduler.RayScheduler

        **Compatibility**

        .. compatibility::
            type: scheduler
            features:
                cancel: true
                logs: true
                distributed: true
                describe: |
                    Partial support. RayScheduler will return job status but
                    does not provide the complete original AppSpec.
                workspaces: false
                mounts: false

        """

        def __init__(self, session_name: str) -> None:
            super().__init__("ray", session_name)

        # TODO: Add address as a potential CLI argument after writing ray.status() or passing in config file
        def run_opts(self) -> runopts:
            opts = runopts()
            opts.add(
                "cluster_config_file",
                type_=str,
                required=False,
                help="Use CLUSTER_CONFIG_FILE to access or create the Ray cluster.",
            )
            opts.add(
                "cluster_name",
                type_=str,
                help="Override the configured cluster name.",
            )
            opts.add(
                "dashboard_address",
                type_=str,
                required=False,
                default="127.0.0.1:8265",
                help="Use ray status to get the dashboard address you will submit jobs against",
            )
            opts.add(
                "working_dir",
                type_=str,
                help="Copy the the working directory containing the Python scripts to the cluster.",
            )
            opts.add("requirements", type_=str, help="Path to requirements.txt")
            return opts

        def schedule(self, dryrun_info: AppDryRunInfo[RayJob]) -> str:
            cfg: RayJob = dryrun_info.request

            # Create serialized actors for ray_driver.py
            actors = cfg.actors
            dirpath = mkdtemp()
            serialize(actors, dirpath)

            job_submission_addr: str = ""
            if cfg.cluster_config_file:
                job_submission_addr = ray_autoscaler_sdk.get_head_node_ip(
                    cfg.cluster_config_file
                )  # pragma: no cover
            elif cfg.dashboard_address:
                job_submission_addr = cfg.dashboard_address
            else:
                raise RuntimeError(
                    "Either `dashboard_address` or `cluster_config_file` must be specified"
                )

            # 0. Create Job Client
            client: JobSubmissionClient = JobSubmissionClient(
                f"http://{job_submission_addr}"
            )

            # 1. Copy working directory
            if cfg.working_dir:
                copytree(cfg.working_dir, dirpath, dirs_exist_ok=True)

            # 2. Copy Ray driver utilities
            current_directory = os.path.dirname(os.path.abspath(__file__))
            copy2(os.path.join(current_directory, "ray", "ray_driver.py"), dirpath)
            copy2(os.path.join(current_directory, "ray", "ray_common.py"), dirpath)

            # 3. Parse requirements.txt
            reqs: List[str] = []
            if cfg.requirements:  # pragma: no cover
                with open(cfg.requirements) as f:
                    for line in f:
                        reqs.append(line.strip())

            # 4. Submit Job via the Ray Job Submission API
            try:
                job_id: str = client.submit_job(
                    job_id=cfg.app_id,
                    # we will pack, hash, zip, upload, register working_dir in GCS of ray cluster
                    # and use it to configure your job execution.
                    entrypoint="python3 ray_driver.py",
                    runtime_env={"working_dir": dirpath, "pip": reqs},
                )

            finally:
                rmtree(dirpath)

            # Encode job submission client in job_id
            return f"{job_submission_addr}-{job_id}"

        def _submit_dryrun(self, app: AppDef, cfg: RayOpts) -> AppDryRunInfo[RayJob]:
            app_id = make_unique(app.name)
            requirements = cfg.get("requirements")

            cluster_cfg = cfg.get("cluster_config_file")
            if cluster_cfg:
                if not isinstance(cluster_cfg, str) or not os.path.isfile(cluster_cfg):
                    raise ValueError(
                        "The cluster configuration file must be a YAML file."
                    )

                job: RayJob = RayJob(
                    app_id,
                    cluster_cfg,
                    requirements=requirements,
                )

            else:  # pragma: no cover
                dashboard_address = cfg.get("dashboard_address")
                job: RayJob = RayJob(
                    app_id=app_id,
                    dashboard_address=dashboard_address,
                    requirements=requirements,
                )
            job.cluster_name = cfg.get("cluster_name")
            job.working_dir = cfg.get("working_dir")

            for role in app.roles:
                for replica_id in range(role.num_replicas):
                    # Replace the ${img_root}, ${app_id}, and ${replica_id} placeholders
                    # in arguments and environment variables.
                    replica_role = macros.Values(
                        img_root=role.image,
                        app_id=app_id,
                        replica_id=str(replica_id),
                        rank0_env=TORCHX_RANK0_HOST,
                    ).apply(role)

                    actor = RayActor(
                        name=role.name,
                        command=[replica_role.entrypoint] + replica_role.args,
                        env=replica_role.env,
                        num_cpus=max(1, replica_role.resource.cpu),
                        num_gpus=max(0, replica_role.resource.gpu),
                    )

                    job.actors.append(actor)

            return AppDryRunInfo(job, repr)

        def _validate(self, app: AppDef, scheduler: str) -> None:
            if scheduler != "ray":
                raise ValueError(
                    f"An unknown scheduler backend '{scheduler}' has been passed to the Ray scheduler."
                )

            if app.metadata:
                _logger.warning("The Ray scheduler does not use metadata information.")

            for role in app.roles:
                if role.resource.capabilities:
                    _logger.warning(
                        "The Ray scheduler does not support custom resource capabilities."
                    )
                    break

            for role in app.roles:
                if role.port_map:
                    _logger.warning("The Ray scheduler does not support port mapping.")
                    break

        def wait_until_finish(self, app_id: str, timeout: int = 30) -> None:
            """
            ``wait_until_finish`` waits until the specified job has finished
            with a given timeout. This is intended for testing. Programmatic
            usage should use the runner wait method instead.
            """
            addr, _, app_id = app_id.partition("-")

            client = JobSubmissionClient(f"http://{addr}")
            start = time.time()
            while time.time() - start <= timeout:
                status_info = client.get_job_status(app_id)
                status = status_info
                if status in {JobStatus.SUCCEEDED, JobStatus.STOPPED, JobStatus.FAILED}:
                    break
                time.sleep(1)

        def _cancel_existing(self, app_id: str) -> None:  # pragma: no cover
            addr, _, app_id = app_id.partition("-")
            client = JobSubmissionClient(f"http://{addr}")
            client.stop_job(app_id)

        def describe(self, app_id: str) -> Optional[DescribeAppResponse]:
            addr, _, app_id = app_id.partition("-")
            client = JobSubmissionClient(f"http://{addr}")
            job_status_info = client.get_job_status(app_id)
            state = _ray_status_to_torchx_appstate[job_status_info]
            roles = [Role(name="ray", num_replicas=-1, image="<N/A>")]

            # get ip_address and put it in hostname

            roles_statuses = [
                RoleStatus(
                    role="ray",
                    replicas=[
                        ReplicaStatus(
                            id=0,
                            role="ray",
                            hostname=NONE,
                            state=state,
                        )
                    ],
                )
            ]
            return DescribeAppResponse(
                app_id=app_id,
                state=state,
                msg=job_status_info,
                roles_statuses=roles_statuses,
                roles=roles,
            )

        def log_iter(
            self,
            app_id: str,
            role_name: Optional[str] = None,
            k: int = 0,
            regex: Optional[str] = None,
            since: Optional[datetime] = None,
            until: Optional[datetime] = None,
            should_tail: bool = False,
            streams: Optional[Stream] = None,
        ) -> List[str]:
            # TODO: support regex, tailing, streams etc..
            addr, _, app_id = app_id.partition("-")
            client: JobSubmissionClient = JobSubmissionClient(f"http://{addr}")
            logs: str = client.get_job_logs(app_id)
            return split_lines(logs)

    def create_scheduler(session_name: str, **kwargs: Any) -> RayScheduler:
        if not has_ray():  # pragma: no cover
            raise RuntimeError(
                "Ray is not installed in the current Python environment."
            )

        return RayScheduler(session_name=session_name)
