import requests
from typing import Callable, Dict, List, Optional, Tuple, Union


class MetricsBasedServerFinder:
    def __init__(
        self,
        hosts_config: List[Dict[str, Optional[Union[str, int]]]],
        metrics_name: str,
        comparison_function: Optional[Callable[[float, float], bool]] = None,
    ):
        self.hosts_config = hosts_config
        self.metrics_name = metrics_name
        self.comparison_function = comparison_function or (lambda x, y: x < y)

    def fetch_metrics(self) -> Tuple[str, int]:
        best_host = None
        best_metric_value = None

        for host_config in self.hosts_config:
            metrics_url = self._construct_metrics_url(host_config)
            metric_value = self._get_metric_value_from_url(metrics_url)

            if metric_value is not None:
                if best_host is None or self.comparison_function(metric_value, best_metric_value):
                    best_host = (host_config["host"], host_config["port"])
                    best_metric_value = metric_value

        if best_host is None:
            print("No accessible servers or metrics not found.")
        return best_host

    def _construct_metrics_url(self, host_config: Dict[str, Optional[Union[str, int]]]) -> str:
        scheme = host_config.get("scheme", "http")
        metrics_path = host_config.get("metrics_path", "")
        return f"{scheme}://{host_config['host']}:{host_config['metrics_port']}/{metrics_path}"

    def _get_metric_value_from_url(self, metrics_url: str) -> Optional[float]:
        try:
            response = requests.get(metrics_url)
            response.raise_for_status()
            return self._parse_prometheus_metrics(response.text)
        except requests.exceptions.RequestException as e:
            print(
                f"Warning: Couldn't fetch metrics from {metrics_url}, skipping. Reason: {e}")
            return None

    def _parse_prometheus_metrics(self, response_text: str) -> Optional[float]:
        for line in response_text.split("\n"):
            if line.startswith(self.metrics_name):
                return float(line[len(self.metrics_name):].strip().split(" ")[0])
        return None
