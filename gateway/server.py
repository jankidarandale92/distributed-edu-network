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

    broker.publish({
        "type": "SEARCH_REQUEST",
        "query": query,
        "sender": "GATEWAY"
    })

    consumer.process_next_message()

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


def get_resource_from_node(
    node_id,
    address,
    resource_id
):
    """
    Retrieve a specific resource from its resource node.
    """

    channel = grpc.insecure_channel(address)

    try:

        stub = resource_pb2_grpc.ResourceServiceStub(channel)

        response = stub.GetResource(
            resource_pb2.ResourceRequest(
                resource_id=resource_id
            ),
            timeout=3
        )

        if response.found:

            return True, response.resource

        return False, None

    except grpc.RpcError as error:

        print(
            f"[Gateway] {node_id} unavailable: "
            f"{error.code()}"
        )

        return False, None

    finally:

        channel.close()


def get_resource(resource_id):
    """
    Retrieve a resource using its resource ID.
    """

    discovered_nodes = discover_nodes()

    if not discovered_nodes:

        print(
            "[Gateway] No registered resource nodes found."
        )

        return None

    print(
        f"[Gateway] Searching for resource "
        f"'{resource_id}' across "
        f"{len(discovered_nodes)} registered node(s)."
    )

    target_node_id = None

    if resource_id.startswith("CSE-"):

        target_node_id = "NODE-CSE-001"

    elif resource_id.startswith("LIB-"):

        target_node_id = "NODE-LIBRARY-001"

    elif resource_id.startswith("COM-"):

        target_node_id = "NODE-COMMUNITY-001"

    if (
        target_node_id
        and target_node_id in discovered_nodes
    ):

        node_info = discovered_nodes[target_node_id]

        print(
            f"[Gateway] Resource belongs to "
            f"{target_node_id}."
        )

        success, resource = get_resource_from_node(
            target_node_id,
            node_info["address"],
            resource_id
        )

        if success:

            return resource

        print(
            f"[Gateway] Resource '{resource_id}' "
            f"was not found on {target_node_id}."
        )

        return None

    print(
        "[Gateway] Resource owner could not be "
        "determined. Searching all nodes."
    )

    with ThreadPoolExecutor(
        max_workers=len(discovered_nodes)
    ) as executor:

        future_to_node = {
            executor.submit(
                get_resource_from_node,
                node_id,
                node_info["address"],
                resource_id
            ): node_id
            for node_id, node_info
            in discovered_nodes.items()
        }

        for future in as_completed(future_to_node):

            node_id = future_to_node[future]

            try:

                success, resource = future.result()

                if success:

                    print(
                        f"[Gateway] Resource found on "
                        f"{node_id}."
                    )

                    return resource

            except Exception as error:

                print(
                    f"[Gateway] Unexpected error while "
                    f"contacting {node_id}: {error}"
                )

    return None


def add_resource_to_node(
    node_id,
    address,
    title,
    subject,
    description,
    resource_type,
    author
):
    """
    Add a new resource to a resource node.

    Returns:
        (True, resource_id, message)  -> successful
        (False, None, message)        -> failed
    """

    channel = grpc.insecure_channel(address)

    try:

        stub = resource_pb2_grpc.ResourceServiceStub(channel)

        response = stub.AddResource(
            resource_pb2.AddResourceRequest(
                title=title,
                subject=subject,
                description=description,
                resource_type=resource_type,
                author=author
            ),
            timeout=3
        )

        if response.success:

            print(
                f"[Gateway] Resource added to "
                f"{node_id}."
            )

            return (
                True,
                response.resource_id,
                response.message
            )

        return (
            False,
            None,
            response.message
        )

    except grpc.RpcError as error:

        print(
            f"[Gateway] {node_id} unavailable: "
            f"{error.code()}"
        )

        return (
            False,
            None,
            f"Node unavailable: {error.code()}"
        )

    finally:

        channel.close()


def add_resource():
    """
    Add a new resource to the CSE resource node.

    The Gateway first discovers registered nodes and
    then sends the AddResource request to the CSE node.
    """

    discovered_nodes = discover_nodes()

    if not discovered_nodes:

        print(
            "[Gateway] No registered resource nodes found."
        )

        return

    target_node_id = "NODE-CSE-001"

    if target_node_id not in discovered_nodes:

        print(
            "[Gateway] CSE resource node is not "
            "currently registered."
        )

        return

    print("\nAdd New Resource")
    print("=" * 50)

    title = input("Title       : ").strip()
    subject = input("Subject     : ").strip()
    description = input("Description : ").strip()
    resource_type = input("Type        : ").strip()
    author = input("Author      : ").strip()

    if not all([
        title,
        subject,
        description,
        resource_type,
        author
    ]):

        print(
            "\nAll fields are required."
        )

        return

    node_info = discovered_nodes[target_node_id]

    success, resource_id, message = add_resource_to_node(
        target_node_id,
        node_info["address"],
        title,
        subject,
        description,
        resource_type,
        author
    )

    if success:

        print("\nResource Added Successfully")
        print("=" * 50)
        print(f"Resource ID : {resource_id}")
        print(f"Title       : {title}")
        print(f"Subject     : {subject}")
        print(f"Type        : {resource_type}")
        print(f"Author      : {author}")
        print(f"Node        : {target_node_id}")
        print(f"Message     : {message}")
        print("-" * 50)

    else:

        print(
            f"\nFailed to add resource: {message}"
        )


def display_resource(resource):
    """
    Display complete resource information.
    """

    print("\nResource Details")
    print("=" * 50)

    print(
        f"Resource ID : {resource.resource_id}"
    )

    print(
        f"Title       : {resource.title}"
    )

    print(
        f"Subject     : {resource.subject}"
    )

    print(
        f"Description : {resource.description}"
    )

    print(
        f"Type        : {resource.resource_type}"
    )

    print(
        f"Author      : {resource.author}"
    )

    print(
        f"Node        : {resource.node_id}"
    )

    print("-" * 50)


def search_resources_flow():
    """
    Handle the resource search operation.
    """

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


def get_resource_flow():
    """
    Handle resource retrieval operation.
    """

    resource_id = input(
        "\nEnter Resource ID: "
    ).strip()

    if not resource_id:

        print(
            "Please enter a Resource ID."
        )

        return

    resource = get_resource(resource_id)

    if resource is None:

        print(
            f"\nResource '{resource_id}' "
            f"was not found."
        )

        return

    display_resource(resource)


def main():

    print("========================================")
    print(" Distributed Educational Resource Gateway")
    print("========================================")

    try:

        while True:

            print("\nGateway Menu")
            print("=" * 40)
            print("1. Search Resources")
            print("2. Get Resource by ID")
            print("3. Add Resource")
            print("4. Exit")
            print("=" * 40)

            choice = input(
                "Enter your choice: "
            ).strip()

            if choice == "1":

                search_resources_flow()

            elif choice == "2":

                get_resource_flow()

            elif choice == "3":

                add_resource()

            elif choice == "4":

                print(
                    "\nExiting Gateway..."
                )

                break

            else:

                print(
                    "\nInvalid choice. "
                    "Please select 1, 2, 3 or 4."
                )

    finally:

        registry_client.close()


if __name__ == "__main__":
    main()