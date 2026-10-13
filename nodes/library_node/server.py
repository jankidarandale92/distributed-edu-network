from concurrent import futures

import grpc

from generated import resource_pb2
from generated import resource_pb2_grpc
from registry.client import RegistryClient
from messaging.logical_clock import LamportClock


NODE_ID = "NODE-LIBRARY-001"
NODE_TYPE = "LIBRARY"
PORT = 50052
REGISTRY_ADDRESS = "localhost:50054"


class ResourceService(
    resource_pb2_grpc.ResourceServiceServicer
):

    def __init__(self):

        # Lamport logical clock for this resource node
        self.lamport_clock = LamportClock()

        self.resources = [
            resource_pb2.Resource(
                resource_id="LIB-RES-001",
                title="Python Programming Study Guide",
                subject="Python",
                description=(
                    "Study guide covering Python programming "
                    "fundamentals."
                ),
                resource_type="Study Guide",
                author="Library Collection",
                node_id=NODE_ID
            ),

            resource_pb2.Resource(
                resource_id="LIB-RES-002",
                title="Computer Networks Reference Notes",
                subject="Computer Networks",
                description=(
                    "Reference material covering networking "
                    "concepts and protocols."
                ),
                resource_type="Reference",
                author="Library Collection",
                node_id=NODE_ID
            ),

            resource_pb2.Resource(
                resource_id="LIB-RES-003",
                title="Data Structures and Algorithms",
                subject="DSA",
                description=(
                    "Reference material for data structures "
                    "and algorithmic problem solving."
                ),
                resource_type="Notes",
                author="Library Collection",
                node_id=NODE_ID
            )
        ]

    def SearchResources(self, request, context):

        # Receive and update Lamport timestamp
        self.lamport_clock.update(
            request.lamport_timestamp
        )

        print(
            f"[Lamport] {NODE_ID} received request "
            f"with timestamp "
            f"{request.lamport_timestamp}"
        )

        # Increment clock before sending response
        response_timestamp = self.lamport_clock.tick()

        print(
            f"[Lamport] {NODE_ID} sending response "
            f"with timestamp "
            f"{response_timestamp}"
        )

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
            resources=matching_resources,
            lamport_timestamp=response_timestamp
        )

    def GetResource(self, request, context):

        # Receive and update Lamport timestamp
        self.lamport_clock.update(
            request.lamport_timestamp
        )

        response_timestamp = self.lamport_clock.tick()

        print(
            f"[Lamport] {NODE_ID} processed GetResource "
            f"with timestamp "
            f"{response_timestamp}"
        )

        for resource in self.resources:

            if resource.resource_id == request.resource_id:

                return resource_pb2.ResourceResponse(
                    resource=resource,
                    found=True,
                    lamport_timestamp=response_timestamp
                )

        return resource_pb2.ResourceResponse(
            found=False,
            lamport_timestamp=response_timestamp
        )

    def AddResource(self, request, context):

        # Receive and update Lamport timestamp
        self.lamport_clock.update(
            request.lamport_timestamp
        )

        response_timestamp = self.lamport_clock.tick()

        print(
            f"[Lamport] {NODE_ID} processed AddResource "
            f"with timestamp "
            f"{response_timestamp}"
        )

        resource_id = (
            f"LIB-RES-{len(self.resources) + 1:03d}"
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
            resource_id=resource_id,
            lamport_timestamp=response_timestamp
        )

    def HealthCheck(self, request, context):

        # Receive and update Lamport timestamp
        self.lamport_clock.update(
            request.lamport_timestamp
        )

        response_timestamp = self.lamport_clock.tick()

        print(
            f"[Lamport] {NODE_ID} HealthCheck timestamp "
            f"{response_timestamp}"
        )

        return resource_pb2.HealthResponse(
            node_id=NODE_ID,
            healthy=True,
            lamport_timestamp=response_timestamp
        )


def serve():

    # Connect to the Node Registry
    registry = RegistryClient(
        REGISTRY_ADDRESS
    )

    server = None

    try:

        # Register this node with the Registry
        response = registry.register_node(
            NODE_ID,
            NODE_TYPE,
            f"localhost:{PORT}"
        )

        if response.success:
            print(
                f"[Library] {response.message}"
            )
        else:
            print(
                f"[Library] Registration failed: "
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

        server.wait_for_termination()

    except KeyboardInterrupt:

        print(
            f"\n[Library] Stopping {NODE_ID}..."
        )

    finally:

        # Unregister from Registry
        try:
            response = registry.unregister_node(
                NODE_ID
            )

            print(
                f"[Library] {response.message}"
            )

        except grpc.RpcError as error:

            print(
                f"[Library] Could not unregister "
                f"from Registry: {error.code()}"
            )

        registry.close()

        if server is not None:
            server.stop(0)


if __name__ == "__main__":
    serve()