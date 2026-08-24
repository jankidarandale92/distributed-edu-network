from messaging.broker import MessageBroker


def main():
    broker = MessageBroker()

    print("========================================")
    print(" Message-Oriented Communication Test")
    print("========================================")

    # Producer publishes messages
    broker.publish({
        "type": "SEARCH_REQUEST",
        "query": "Distributed Systems",
        "sender": "STUDENT-001"
    })

    broker.publish({
        "type": "SEARCH_REQUEST",
        "query": "Python",
        "sender": "STUDENT-002"
    })

    print(f"\nPending messages: {broker.pending_messages()}")

    # Consumer retrieves messages
    print("\nConsuming messages...")

    while broker.pending_messages() > 0:
        message = broker.consume()
        print(f"Consumer received: {message}")

    print("\nAll messages processed.")


if __name__ == "__main__":
    main()