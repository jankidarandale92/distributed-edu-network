from concurrent import futures

import grpc

from generated import registry_pb2
from generated import registry_pb2_grpc
from registry.node_registry import NodeRegistry


REGISTRY_PORT = 50054


class NodeRegistryService(
    registry_pb2_grpc.NodeRegistryServiceServicer
):
    """
    gRPC service for registering, unregistering,
    and discovering distributed resource nodes.
    """

    def __init__(self):
        self.registry = NodeRegistry()

    def RegisterNode(self, request, context):
        node = request.node

        self.registry.register_node(
            node.node_id,
            node.node_type,
            node.address
        )

        return registry_pb2.RegisterNodeResponse(
            success=True,
            message=f"Node {node.node_id} registered successfully."
        )

    def UnregisterNode(self, request, context):
        node_id = request.node_id

        if self.registry.get_node(node_id) is None:
            return registry_pb2.UnregisterNodeResponse(
                success=False,
                message=f"Node {node_id} is not registered."
            )

        self.registry.unregister_node(node_id)

        return registry_pb2.UnregisterNodeResponse(
            success=True,
            message=f"Node {node_id} unregistered successfully."
        )

    def GetNodes(self, request, context):
        response = registry_pb2.GetNodesResponse()

        nodes = self.registry.get_all_nodes()

        for node_id, node_info in nodes.items():
            response.nodes.add(
                node_id=node_id,
                node_type=node_info["node_type"],
                address=node_info["address"]
            )

        return response


def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    registry_pb2_grpc.add_NodeRegistryServiceServicer_to_server(
        NodeRegistryService(),
        server
    )

    server.add_insecure_port(
        f"[::]:{REGISTRY_PORT}"
    )

    server.start()

    print("========================================")
    print(" Distributed Node Registry")
    print("========================================")
    print(
        f"Registry Server is running on "
        f"port {REGISTRY_PORT}"
    )
    print("Waiting for registration requests...")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\nRegistry server stopped.")
        server.stop(0)


if __name__ == "__main__":
    serve()