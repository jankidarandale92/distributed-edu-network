import grpc

from generated import resource_pb2
from generated import resource_pb2_grpc


def run():
    channel = grpc.insecure_channel("localhost:50052")

    stub = resource_pb2_grpc.ResourceServiceStub(channel)

    response = stub.SearchResources(
        resource_pb2.SearchRequest(
            query="Python"
        )
    )

    print("\nLibrary Node Search Results:")
    print("-" * 50)

    if not response.resources:
        print("No resources found.")
        return

    for resource in response.resources:
        print(f"Resource ID : {resource.resource_id}")
        print(f"Title       : {resource.title}")
        print(f"Subject     : {resource.subject}")
        print(f"Type        : {resource.resource_type}")
        print(f"Author      : {resource.author}")
        print(f"Node        : {resource.node_id}")
        print("-" * 50)


if __name__ == "__main__":
    run()