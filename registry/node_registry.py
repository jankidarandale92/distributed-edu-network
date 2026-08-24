class NodeRegistry:
    """
    Maintains the identity and network address of
    resource nodes in the distributed system.
    """

    def __init__(self):
        self.nodes = {}

    def register_node(self, node_id, node_type, address):
        """
        Register a resource node.
        """

        self.nodes[node_id] = {
            "node_type": node_type,
            "address": address
        }

        print(
            f"[Registry] Registered {node_id} "
            f"({node_type}) at {address}"
        )

    def unregister_node(self, node_id):
        """
        Remove a resource node from the registry.
        """

        if node_id in self.nodes:
            del self.nodes[node_id]

            print(
                f"[Registry] Unregistered {node_id}"
            )

    def get_node(self, node_id):
        """
        Retrieve information about a specific node.
        """

        return self.nodes.get(node_id)

    def get_all_nodes(self):
        """
        Return all registered nodes.
        """

        return self.nodes.copy()

    def get_nodes_by_type(self, node_type):
        """
        Return nodes belonging to a specific node type.
        """

        return {
            node_id: info
            for node_id, info in self.nodes.items()
            if info["node_type"] == node_type
        }

    def node_count(self):
        """
        Return the number of registered nodes.
        """

        return len(self.nodes)
    