import grpc

from generated import resource_pb2
from generated import resource_pb2_grpc


NODES = {
    "CSE": "localhost:50051",
    "Library": "localhost:50052",
    "Community": "localhost:50053"
}


def search_node(node_name, address, query):
    try:
        channel = grpc.insecure_channel(address)
        stub = resource_pb2_grpc.ResourceServiceStub(channel)

        response = stub.SearchResources(
            resource_pb2.SearchRequest(query=query),
            timeout=3
        )

        return list(response.resources)

    except grpc.RpcError as error:
        print(f"[Gateway] {node_name} unavailable: {error.code()}")
        return []


def search_all_nodes(query):
    all_resources = []

    for node_name, address in NODES.items():
        print(f"[Gateway] Searching {node_name} node...")

        resources = search_node(
            node_name,
            address,
            query
        )

        all_resources.extend(resources)

    return all_resources


def main():
    print("========================================")
    print(" Distributed Educational Resource Gateway")
    print("========================================")

    query = input("\nEnter search query: ").strip()

    if not query:
        print("Please enter a search query.")
        return

    print(f"\nSearching for: {query}")
    print("-" * 50)

    resources = search_all_nodes(query)

    print("\nSearch Results")
    print("=" * 50)

    if not resources:
        print("No resources found.")
        return

    for resource in resources:
        print(f"Resource ID : {resource.resource_id}")
        print(f"Title       : {resource.title}")
        print(f"Subject     : {resource.subject}")
        print(f"Type        : {resource.resource_type}")
        print(f"Author      : {resource.author}")
        print(f"Node        : {resource.node_id}")
        print("-" * 50)


if __name__ == "__main__":
    main()