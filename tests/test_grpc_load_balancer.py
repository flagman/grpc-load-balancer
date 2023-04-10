import os
import sys
import time
import unittest
import multiprocessing


import grpc
import requests
from prometheus_client import Gauge, start_http_server

from example_service import (
    create_example_grpc_server,
    create_example_grpc_client,
    example_service_pb2,
)

if sys.platform == "darwin":
    multiprocessing.set_start_method("fork")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from grpc_load_balancer import GrpcConnnectionForwarder, EnvConfigLoader  # nopep8


def connection_counter_callback(value: int, counter: Gauge) -> None:
    counter.set(value)


def forwarder_init_process(forwarder_port, prometheus_port, event):
    grpc_server = create_example_grpc_server()
    connection_counter = Gauge(
        f'connections_num', 'Number of connections forwarded')
    forwarder = GrpcConnnectionForwarder(
        grpc_server, callback=lambda value: connection_counter_callback(
            value, connection_counter)
    )
    start_http_server(prometheus_port)
    forwarder.serve(host="localhost", port=forwarder_port)
    event.wait()
    forwarder.stop()


class TestGrpcLoadBalancer(unittest.TestCase):
    def check_metric_value(self, port: int, metric_name: str, expected_value: float):
        metrics_response = requests.get(f"http://localhost:{port}/metrics")
        for line in metrics_response.text.splitlines():
            if line.startswith(metric_name):
                value = float(line.split()[-1])
                self.assertEqual(value, expected_value)
                return
        self.fail(f"Metric '{metric_name}' not found in the response.")

    def test_forwarding(self):
        forwarder_ports = [30000 + i for i in range(2)]
        prometheus_ports = [20000 + i for i in range(2)]
        events = [multiprocessing.Event() for _ in range(2)]
        forwarder_processes = [
            multiprocessing.Process(target=forwarder_init_process, args=(
                forwarder_port, prometheus_port, event))
            for (forwarder_port, prometheus_port, event) in zip(forwarder_ports, prometheus_ports, events)
        ]

        for process in forwarder_processes:
            process.start()

        time.sleep(1)  # Allow the servers to start

        channels = [grpc.insecure_channel(
            f"localhost:{forwarder_port}") for forwarder_port in forwarder_ports]
        clients = [create_example_grpc_client(channel) for channel in channels]

        request = example_service_pb2.GetValueRequest(key=42)
        responses = [client.GetValue(request) for client in clients]

        for response in responses:
            self.assertEqual(response.value, "Value for key 42")

        # Check if connections_num_ is incremented
        for port in prometheus_ports:
            self.check_metric_value(port, f"connections_num", 1)

        # Close the channels
        for channel in channels:
            channel.close()

        time.sleep(1)  # Allow time for the channels to close

        # Check if connections_num_ is decremented
        for port in prometheus_ports:
            self.check_metric_value(port, f"connections_num", 0)

        for process in forwarder_processes:
            process.terminate()
            process.join()

    def test_metrics_based_server_finder(self):
        os.environ['LB_METRICS_NAME'] = 'connections_num'
        os.environ['LB_HOST1_HOST'] = 'localhost'
        os.environ['LB_HOST1_PORT'] = '20000'
        os.environ['LB_HOST1_METRICS_PORT'] = '20001'
        os.environ['LB_HOST2_HOST'] = 'localhost'
        os.environ['LB_HOST2_PORT'] = '30000'
        os.environ['LB_HOST2_METRICS_PORT'] = '30001'
        # 1) Initialise forwarders, grpc servers and Prometheus using env file
        env_config_loader = EnvConfigLoader(prefix="LB")
        metrics_based_server_finder = env_config_loader.init_metrics_based_server_finder()
        forwarder_processes = []
        events = []

        # host_config = {
        #     "host": os.environ[host_key],
        #     "port": os.environ[port_key],
        #     "metrics_port": os.environ[metrics_port_key],
        #     "metrics_path": os.environ.get(metrics_path_key, None),
        #     "scheme": os.environ.get(scheme_key, "http"),
        # }

        for host_config in metrics_based_server_finder.hosts_config:
            event = multiprocessing.Event()
            process = multiprocessing.Process(target=forwarder_init_process, args=(
                int(host_config['port']), int(host_config['metrics_port']), event))
            forwarder_processes.append(process)
            events.append(event)

        for process in forwarder_processes:
            process.start()

        time.sleep(1)  # Allow the servers to start
        best_host = metrics_based_server_finder.fetch_metrics()
        self.assertEqual(best_host, ('localhost', '20000'))

        # 3) Connect to the first forwarder
        channel = grpc.insecure_channel(f"{best_host[0]}:{best_host[1]}")
        client = create_example_grpc_client(channel)

        request = example_service_pb2.GetValueRequest(key=42)
        response = client.GetValue(request)
        self.assertEqual(response.value, "Value for key 42")

        # 4) Fetch best hosts again, it should be the second host
        new_best_host = metrics_based_server_finder.fetch_metrics()
        self.assertEqual(new_best_host, ('localhost', '30000'))

        # Clean up
        channel.close()
        for event in events:
            event.set()
        for process in forwarder_processes:
            process.terminate()
            process.join()


if __name__ == "__main__":
    unittest.main()
