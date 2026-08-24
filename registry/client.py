import grpc

from generated import registry_pb2
from generated import registry_pb2_grpc


REGISTRY_ADDRESS = "localhost:50054"


class RegistryClient:

    def __init__(self, address=REGISTRY_ADDRESS):
        self.channel = grpc.insecure_channel(address)

        self.stub = (
            registry_pb2_grpc.NodeRegistryServiceStub(
                self.channel
            )
        )

    def register_node(
        self,
        node_id,
        node_type,
        address
    ):
        response = self.stub.RegisterNode(
            registry_pb2.RegisterNodeRequest(
                node=registry_pb2.NodeInfo(
                    node_id=node_id,
                    node_type=node_type,
                    address=address
                )
            )
        )

        return response

    def unregister_node(self, node_id):
        response = self.stub.UnregisterNode(
            registry_pb2.UnregisterNodeRequest(
                node_id=node_id
            )
        )

        return response

    def get_nodes(self):
        response = self.stub.GetNodes(
            registry_pb2.GetNodesRequest()
        )

        return list(response.nodes)

    def close(self):
        self.channel.close()