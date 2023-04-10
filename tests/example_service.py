import grpc
from concurrent import futures
import example_service_pb2
import example_service_pb2_grpc


class ExampleServiceServicer(example_service_pb2_grpc.ExampleServiceServicer):
    def GetValue(self, request, context):
        return example_service_pb2.GetValueResponse(value=f"Value for key {request.key}")


def create_example_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    example_service_pb2_grpc.add_ExampleServiceServicer_to_server(
        ExampleServiceServicer(), server)
    return server


def create_example_grpc_client(channel):
    return example_service_pb2_grpc.ExampleServiceStub(channel)
