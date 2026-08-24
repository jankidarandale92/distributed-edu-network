import grpc

from concurrent.futures import ThreadPoolExecutor, as_completed

from generated import resource_pb2
from generated import resource_pb2_grpc
from messaging.broker import MessageBroker
from messaging.consumer import MessageConsumer
from registry.node_registry import NodeRegistry


broker = MessageBroker()
consumer = MessageConsumer(broker)
registry = NodeRegistry()


# Register resource nodes with the registry
registry.register_node(
    "NODE-CSE-001",
    "CSE",
    "localhost:50051"
)

registry.register_node(
    "NODE-LIBRARY-001",
    "LIBRARY",
    "localhost:50052"
)

registry.register_node(
    "NODE-COMMUNITY-001",
    "COMMUNITY",
    "localhost:50053"
)


def search_node(node_name, address, query):
    """
    Send a search request to one resource node.

    Returns:
        (True, resources)  -> node responded successfully
        (False, [])        -> node is unavailable
    """
    try:
        channel = grpc.insecure_channel(address)

        stub = resource_pb2_grpc.ResourceServiceStub(channel)

        response = stub.SearchResources(
            resource_pb2.SearchRequest(
                query=query
            ),
            timeout=3
        )

        return True, list(response.resources)

    except grpc.RpcError as error:
        print(
            f"[Gateway] {node_name} unavailable: "
            f"{error.code()}"
        )

        return False, []


def search_all_nodes(query):
    """
    Search all registered resource nodes concurrently.
    """

    all_resources = []

    # Discover nodes from the registry
    discovered_nodes = registry.get_all_nodes()

    # Publish search request through message-oriented communication
    broker.publish({
        "type": "SEARCH_REQUEST",
        "query": query,
        "sender": "GATEWAY"
    })

    # Process the published message
    consumer.process_next_message()

    # Search all discovered nodes concurrently
    with ThreadPoolExecutor(
        max_workers=len(discovered_nodes)
    ) as executor:

        future_to_node = {
            executor.submit(
                search_node,
                node_id,
                node_info["address"],
                query
            ): node_id
            for node_id, node_info in discovered_nodes.items()
        }

        for future in as_completed(future_to_node):

            node_id = future_to_node[future]

            try:
                success, resources = future.result()

                if success:
                    print(
                        f"[Gateway] {node_id} returned "
                        f"{len(resources)} resource(s)."
                    )

                    all_resources.extend(resources)

            except Exception as error:
                print(
                    f"[Gateway] Unexpected error while "
                    f"contacting {node_id}: {error}"
                )

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