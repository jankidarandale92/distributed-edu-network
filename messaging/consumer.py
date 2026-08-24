from messaging.broker import MessageBroker


class MessageConsumer:
    """
    Consumer responsible for processing messages
    from the message broker.
    """

    def __init__(self, broker):
        self.broker = broker

    def process_next_message(self):
        """
        Consume and process the next available message.
        """

        message = self.broker.consume()

        if message is None:
            print("[Consumer] No messages available.")
            return None

        print(
            f"[Consumer] Processing message: {message}"
        )

        message_type = message.get("type")

        if message_type == "SEARCH_REQUEST":

            query = message.get("query")
            sender = message.get("sender")

            print(
                f"[Consumer] Search request received "
                f"from {sender}: '{query}'"
            )

        else:
            print(
                f"[Consumer] Unknown message type: "
                f"{message_type}"
            )

        return message
    