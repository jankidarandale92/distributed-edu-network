import grpc

from concurrent.futures import ThreadPoolExecutor, as_completed

from generated import resource_pb2
from generated import resource_pb2_grpc

from messaging.broker import MessageBroker
from messaging.consumer import MessageConsumer
from registry.client import RegistryClient


REGISTRY_ADDRESS = "localhost:50054"


broker = MessageBroker()
consumer = MessageConsumer(broker)
registry_client = RegistryClient(REGISTRY_ADDRESS)


def search_node(node_id, node_type, address, query):
    """
    Send a search request to one resource node.

    Returns:
        (True, resources)  -> node responded successfully
        (False, [])        -> node is unavailable
    """

    channel = grpc.insecure_channel(address)

    try:
        stub = resource_pb2_grpc.ResourceServiceStub(
            channel
        )

        response = stub.SearchResources(
            resource_pb2.SearchRequest(
                query=query
            ),
            timeout=3
        )

        return True, list(response.resources)

    except grpc.RpcError as error:

        print(
            f"[Gateway] {node_id} unavailable: "
            f"{error.code()}"
        )

        return False, []

    finally:
        channel.close()


def discover_nodes():
    """
    Discover currently registered resource nodes
    through the gRPC Node Registry.
    """

    try:
        nodes = registry_client.get_nodes()

        discovered_nodes = {}

        for node in nodes:

            # Ignore invalid or incomplete registry entries
            if not node.node_id or not node.address:
                continue

            discovered_nodes[node.node_id] = {
                "node_type": node.node_type,
                "address": node.address
            }

        return discovered_nodes

    except grpc.RpcError as error:

        print(
            f"[Gateway] Registry unavailable: "
            f"{error.code()}"
        )

        return {}


def search_all_nodes(query):
    """
    Discover registered resource nodes and search
    all of them concurrently.
    """

    all_resources = []

    # Discover nodes dynamically from Registry
    discovered_nodes = discover_nodes()

    if not discovered_nodes:

        print(
            "[Gateway] No registered resource nodes found."
        )

        return all_resources

    print(
        f"[Gateway] Discovered "
        f"{len(discovered_nodes)} registered node(s)."
    )

    # Publish search request through message-oriented
    # communication
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
                node_info["node_type"],
                node_info["address"],
                query
            ): node_id
            for node_id, node_info
            in discovered_nodes.items()
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

    try:

        query = input(
            "\nEnter search query: "
        ).strip()

        if not query:

            print(
                "Please enter a search query."
            )

            return

        print(
            f"\nSearching for: {query}"
        )

        print("-" * 50)

        resources = search_all_nodes(query)

        print("\nSearch Results")
        print("=" * 50)

        if not resources:

            print("No resources found.")

            return

        for resource in resources:

            print(
                f"Resource ID : "
                f"{resource.resource_id}"
            )

            print(
                f"Title       : "
                f"{resource.title}"
            )

            print(
                f"Subject     : "
                f"{resource.subject}"
            )

            print(
                f"Type        : "
                f"{resource.resource_type}"
            )

            print(
                f"Author      : "
                f"{resource.author}"
            )

            print(
                f"Node        : "
                f"{resource.node_id}"
            )

            print("-" * 50)

    finally:

        registry_client.close()


if __name__ == "__main__":
    main()