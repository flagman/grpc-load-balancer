import os
from typing import Dict, List, Optional, Union
from .metrics_based_server_finder import MetricsBasedServerFinder


class EnvConfigLoader:
    def __init__(self, prefix: str = "MB_SERVER_FINDER"):
        self.prefix = prefix

    def load_hosts_config(self) -> List[Dict[str, Optional[Union[str, int]]]]:
        hosts_config = []
        i = 1

        while True:
            host_key = self._generate_key(i, "HOST")
            if host_key not in os.environ:
                break

            host_config = self._load_host_config(i)
            hosts_config.append(host_config)
            i += 1

        return hosts_config

    def _generate_key(self, index: int, suffix: str) -> str:
        return f"{self.prefix}_HOST{index}_{suffix}"

    def _load_host_config(self, index: int) -> Dict[str, Optional[Union[str, int]]]:
        host_key = self._generate_key(index, "HOST")
        port_key = self._generate_key(index, "PORT")
        metrics_port_key = self._generate_key(index, "METRICS_PORT")
        metrics_path_key = self._generate_key(index, "METRICS_PATH")
        scheme_key = self._generate_key(index, "SCHEME")

        host_config = {
            "host": os.environ[host_key],
            "port": os.environ[port_key],
            "metrics_port": os.environ[metrics_port_key],
            "metrics_path": os.environ.get(metrics_path_key, None),
            "scheme": os.environ.get(scheme_key, "http"),
        }
        return host_config

    def init_metrics_based_server_finder(self) -> MetricsBasedServerFinder:
        hosts_config = self.load_hosts_config()
        metrics_name = os.environ[f"{self.prefix}_METRICS_NAME"]
        return MetricsBasedServerFinder(hosts_config, metrics_name)
