# gRPC Load Balancer

`grpc_load_balancer` is a Python package that allows you to easily configure and manage separate gRPC server and client instances using a metrics-based load balancing approach. This is useful when you have multiple services running and want to distribute the load efficiently among them. The package includes a connection forwarder, a metrics-based server finder, and a configuration loader.
It implemetns the following design:
![Design](https://grpc.io/img/image_1.png)


## Features

- Forward connections from clients to gRPC servers.
- Use Prometheus metrics to select the best server to handle a request.
- Configure and manage gRPC servers and clients using environment variables.

## Installation

You can install `grpc_load_balancer` using pip:

```bash
pip install grpc_load_balancer
```

Install promethus-client:

```bash
pip install prometheus-client
```

## Usage 
## Configuring and running a gRPC server

Here's a simple example of how to use grpc_connection_forwarder with a gRPC server and prometeus-client:

# Import the required modules:
```python 
import grpc
from grpc_connection_forwarder import GrpcConnnectionForwarder
from prometheus_client import start_http_server, Gauge
```


# Initialize your gRPC server(s)
```python
    grpc_server = create_example_grpc_server() # implement this function yourself
    connection_counter = Gauge(
        f'connections_num', 'Number of connections forwarded')
    forwarder = GrpcConnnectionForwarder(
        grpc_server, callback=lambda value: connection_counter.set(value)
    )
    start_http_server(prometheus_port)
    # forwarder_port - port to listen connections from gRPC clients

    # Note this call is blocking
    forwarder.serve(host="0.0.0.0", port=forwarder_port)

    # If you want to run the server in a separate thread, and want to stop it later, use the forwarder.stop() method
    
```

## Configuring and running a gRPC client
# Import the required modules:    
```python
import grpc
from grpc_connection_forwarder import EnvConfigLoader, MetricsBasedServerFinder
```



# Initialize the configuration loader
```python
# This is example how your environment variables can look like
# os.environ['LB_METRICS_NAME'] = 'connections_num'
# os.environ['LB_HOST1_HOST'] = 'localhost'
# os.environ['LB_HOST1_PORT'] = '20000'
# os.environ['LB_HOST1_METRICS_PORT'] = '20001'
# os.environ['LB_HOST2_HOST'] = 'localhost'
# os.environ['LB_HOST2_PORT'] = '30000'
# os.environ['LB_HOST2_METRICS_PORT'] = '30001'

env_config_loader = EnvConfigLoader(prefix="LB")
```

# Initialize the server finder, find the best server and connect to it
```python
    metrics_based_server_finder = env_config_loader.init_metrics_based_server_finder()
    best_host = metrics_based_server_finder.fetch_metrics()
    channel = grpc.insecure_channel(f"{best_host[0]}:{best_host[1]}")
    client = create_example_grpc_client(channel) # implement this function yourself
    # Use the client to send requests to the server
```

## Troubleshooting

If you have any problems with `grpc_load_balancer`, please open an issue on GitHub.
Also, you can check [tests/test_grpc_load_balancer.py](tests/test_grpc_load_balancer.py) for more information.

## Contributing
We welcome contributions to `grpc_load_balancer`. If you find a bug or want to propose a new feature, please open a GitHub issue or submit a pull request.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
