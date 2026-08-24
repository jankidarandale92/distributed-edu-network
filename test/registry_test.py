from registry.node_registry import NodeRegistry


def main():
    registry = NodeRegistry()

    print("========================================")
    print(" Distributed Node Registry Test")
    print("========================================")

    # Register resource nodes
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

    print(
        f"\nTotal registered nodes: "
        f"{registry.node_count()}"
    )

    print("\nRegistered Nodes:")
    print("-" * 50)

    for node_id, info in registry.get_all_nodes().items():
        print(f"Node ID : {node_id}")
        print(f"Type    : {info['node_type']}")
        print(f"Address : {info['address']}")
        print("-" * 50)

    # Test lookup
    print("\nLooking up NODE-CSE-001:")

    cse_node = registry.get_node("NODE-CSE-001")

    print(cse_node)

    # Test filtering
    print("\nCommunity Nodes:")

    community_nodes = registry.get_nodes_by_type(
        "COMMUNITY"
    )

    print(community_nodes)

    # Test unregister
    print("\nUnregistering NODE-COMMUNITY-001...")

    registry.unregister_node(
        "NODE-COMMUNITY-001"
    )

    print(
        f"Remaining nodes: "
        f"{registry.node_count()}"
    )


if __name__ == "__main__":
    main()
    