import grpc

from generated import registry_pb2
from generated import registry_pb2_grpc


REGISTRY_ADDRESS = "localhost:50054"


def main():
    print("========================================")
    print(" Registry gRPC Client Test")
    print("========================================")

    channel = grpc.insecure_channel(
        REGISTRY_ADDRESS
    )

    stub = registry_pb2_grpc.NodeRegistryServiceStub(
        channel
    )

    # Register a test node
    print("\nRegistering test node...")

    register_response = stub.RegisterNode(
        registry_pb2.RegisterNodeRequest(
            node=registry_pb2.NodeInfo(
                node_id="NODE-TEST-001",
                node_type="TEST",
                address="localhost:59999"
            )
        )
    )

    print(
        f"[Client] {register_response.message}"
    )

    # Discover registered nodes
    print("\nRequesting registered nodes...")

    response = stub.GetNodes(
        registry_pb2.GetNodesRequest()
    )

    print(
        f"[Client] Total nodes: "
        f"{len(response.nodes)}"
    )

    for node in response.nodes:
        print("-" * 50)
        print(f"Node ID : {node.node_id}")
        print(f"Type    : {node.node_type}")
        print(f"Address : {node.address}")

    # Unregister test node
    print("\nUnregistering test node...")

    unregister_response = stub.UnregisterNode(
        registry_pb2.UnregisterNodeRequest(
            node_id="NODE-TEST-001"
        )
    )

    print(
        f"[Client] {unregister_response.message}"
    )

    channel.close()


if __name__ == "__main__":
    main()