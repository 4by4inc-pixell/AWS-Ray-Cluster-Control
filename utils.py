import os
import subprocess
import re
from typing import Dict, List, Optional
import ray

IP_REGEX = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"


def get_cluster_head_ip(config_path: str) -> str:
    assert os.path.exists(config_path)
    assert os.path.isfile(config_path)
    command = f"ray get-head-ip {config_path}"
    p = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE)
    out = p.stdout.read().decode("utf-8")
    texts = out.split("\n")
    filterd_texts = [re.match(IP_REGEX, t) for t in texts]
    filterd_texts = [t.string for t in filterd_texts if t is not None]
    assert len(filterd_texts) == 1
    return filterd_texts[-1]


def get_cluster_worker_ips(config_path: str) -> List[str]:
    assert os.path.exists(config_path)
    assert os.path.isfile(config_path)
    command = f"ray get-head-ip {config_path}"
    p = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE)
    out = p.stdout.read().decode("utf-8")
    texts = out.split("\n")
    filterd_texts = [re.match(IP_REGEX, t) for t in texts]
    filterd_texts = [t.string for t in filterd_texts if t is not None]
    return filterd_texts


def initialize_ray_for_cluster(
    cluster_ip: str,
    cluster_client_port: int,
    namespace: str,
    local_working_dir: Optional[str] = None,
    additional_pip_package: Optional[List[str]] = None,
    env_variable: Optional[Dict[str, str]] = None,
):
    runtime_env = {}
    if local_working_dir is not None:
        assert os.path.isdir(local_working_dir)
        runtime_env.update({"working_dir": local_working_dir})
    if additional_pip_package is not None:
        runtime_env.update({"pip": additional_pip_package})
    if env_variable is not None:
        runtime_env.update({"env_vars": env_variable})
    ray.init(
        address=f"ray://{cluster_ip}:{cluster_client_port}",
        namespace=namespace,
        runtime_env=runtime_env,
    )
