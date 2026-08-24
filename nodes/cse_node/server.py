from concurrent import futures

import grpc

from generated import resource_pb2
from generated import resource_pb2_grpc
from registry.client import RegistryClient


NODE_ID = "NODE-CSE-001"
NODE_TYPE = "CSE"
PORT = 50051
REGISTRY_ADDRESS = "localhost:50054"


class ResourceService(
    resource_pb2_grpc.ResourceServiceServicer
):

    def __init__(self):
        self.resources = [
            resource_pb2.Resource(
                resource_id="CSE-RES-001",
                title="Distributed Systems Unit 1 Notes",
                subject="Distributed Systems",
                description=(
                    "Introduction, goals, architectures "
                    "and design issues."
                ),
                resource_type="Notes",
                author="CSE Student",
                node_id=NODE_ID
            ),

            resource_pb2.Resource(
                resource_id="CSE-RES-002",
                title="Distributed Systems Unit 2 Notes",
                subject="Distributed Systems",
                description=(
                    "RPC, message-oriented communication "
                    "and P2P messaging."
                ),
                resource_type="Notes",
                author="CSE Student",
                node_id=NODE_ID
            ),

            resource_pb2.Resource(
                resource_id="CSE-RES-003",
                title="Database Management System Question Bank",
                subject="DBMS",
                description=(
                    "Important DBMS questions and "
                    "solved problems."
                ),
                resource_type="Question Bank",
                author="CSE Student",
                node_id=NODE_ID
            )
        ]

    def SearchResources(self, request, context):
        query = request.query.lower()

        matching_resources = [
            resource
            for resource in self.resources
            if (
                query in resource.title.lower()
                or query in resource.subject.lower()
                or query in resource.description.lower()
            )
        ]

        return resource_pb2.SearchResponse(
            resources=matching_resources
        )

    def GetResource(self, request, context):
        for resource in self.resources:

            if resource.resource_id == request.resource_id:
                return resource_pb2.ResourceResponse(
                    resource=resource,
                    found=True
                )

        return resource_pb2.ResourceResponse(
            found=False
        )

    def AddResource(self, request, context):

        resource_id = (
            f"CSE-RES-{len(self.resources) + 1:03d}"
        )

        new_resource = resource_pb2.Resource(
            resource_id=resource_id,
            title=request.title,
            subject=request.subject,
            description=request.description,
            resource_type=request.resource_type,
            author=request.author,
            node_id=NODE_ID
        )

        self.resources.append(new_resource)

        return resource_pb2.AddResourceResponse(
            success=True,
            message="Resource added successfully.",
            resource_id=resource_id
        )

    def HealthCheck(self, request, context):
        return resource_pb2.HealthResponse(
            node_id=NODE_ID,
            healthy=True
        )


def serve():

    # Connect to the Node Registry
    registry = RegistryClient(
        REGISTRY_ADDRESS
    )

    try:
        # Register this node with the Registry
        response = registry.register_node(
            NODE_ID,
            NODE_TYPE,
            f"localhost:{PORT}"
        )

        if response.success:
            print(
                f"[CSE] {response.message}"
            )
        else:
            print(
                f"[CSE] Registration failed: "
                f"{response.message}"
            )

        # Create gRPC server
        server = grpc.server(
            futures.ThreadPoolExecutor(
                max_workers=10
            )
        )

        # Register ResourceService
        resource_pb2_grpc.add_ResourceServiceServicer_to_server(
            ResourceService(),
            server
        )

        # Start server
        server.add_insecure_port(
            f"[::]:{PORT}"
        )

        server.start()

        print(
            f"{NODE_ID} is running on port {PORT}"
        )
        print(
            "Waiting for gRPC requests..."
        )

        # Keep server running
        server.wait_for_termination()

    except KeyboardInterrupt:

        print(
            f"\n[CSE] Stopping {NODE_ID}..."
        )

    finally:

        # Remove node from Registry
        try:
            response = registry.unregister_node(
                NODE_ID
            )

            print(
                f"[CSE] {response.message}"
            )

        except grpc.RpcError as error:

            print(
                f"[CSE] Could not unregister "
                f"from Registry: {error.code()}"
            )

        registry.close()

        try:
            server.stop(0)
        except UnboundLocalError:
            pass


if __name__ == "__main__":
    serve()