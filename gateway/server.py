import grpc

from concurrent.futures import ThreadPoolExecutor, as_completed

from generated import resource_pb2
from generated import resource_pb2_grpc
from messaging.broker import MessageBroker


NODES = {
    "CSE": "localhost:50051",
    "Library": "localhost:50052",
    "Community": "localhost:50053"
}

broker = MessageBroker()


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
    Search all available resource nodes concurrently.
    """

    all_resources = []

    broker.publish({
        "type": "SEARCH_REQUEST",
        "query": query,
        "sender": "GATEWAY"
    })

    with ThreadPoolExecutor(
        max_workers=len(NODES)
    ) as executor:

        future_to_node = {
            executor.submit(
                search_node,
                node_name,
                address,
                query
            ): node_name
            for node_name, address in NODES.items()
        }

        for future in as_completed(future_to_node):

            node_name = future_to_node[future]

            try:
                success, resources = future.result()

                if success:
                    print(
                        f"[Gateway] {node_name} returned "
                        f"{len(resources)} resource(s)."
                    )

                    all_resources.extend(resources)

            except Exception as error:
                print(
                    f"[Gateway] Unexpected error while "
                    f"contacting {node_name}: {error}"
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