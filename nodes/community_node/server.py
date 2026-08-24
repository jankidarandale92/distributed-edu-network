from concurrent import futures
import grpc

from generated import resource_pb2
from generated import resource_pb2_grpc


NODE_ID = "NODE-COMMUNITY-001"
PORT = 50053


class ResourceService(resource_pb2_grpc.ResourceServiceServicer):

    def __init__(self):
        self.resources = [
            resource_pb2.Resource(
                resource_id="COM-RES-001",
                title="Web Development Project Guide",
                subject="Web Development",
                description="Guide for developing academic web development projects.",
                resource_type="Project Guide",
                author="Student Community",
                node_id=NODE_ID
            ),
            resource_pb2.Resource(
                resource_id="COM-RES-002",
                title="Machine Learning Study Material",
                subject="Machine Learning",
                description="Community-contributed study material covering machine learning fundamentals.",
                resource_type="Study Material",
                author="Student Community",
                node_id=NODE_ID
            ),
            resource_pb2.Resource(
                resource_id="COM-RES-003",
                title="Mini Project Documentation Examples",
                subject="Project Development",
                description="Examples and guidelines for documenting academic mini projects.",
                resource_type="Documentation",
                author="Student Community",
                node_id=NODE_ID
            )
        ]

    def SearchResources(self, request, context):
        query = request.query.lower()

        matching_resources = [
            resource
            for resource in self.resources
            if query in resource.title.lower()
            or query in resource.subject.lower()
            or query in resource.description.lower()
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
        resource_id = f"COM-RES-{len(self.resources) + 1:03d}"

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
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    resource_pb2_grpc.add_ResourceServiceServicer_to_server(
        ResourceService(),
        server
    )

    server.add_insecure_port(f"[::]:{PORT}")

    server.start()

    print(f"{NODE_ID} is running on port {PORT}")
    print("Waiting for gRPC requests...")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()