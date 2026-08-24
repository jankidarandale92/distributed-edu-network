from messaging.broker import MessageBroker
from messaging.consumer import MessageConsumer


def main():
    broker = MessageBroker()
    consumer = MessageConsumer(broker)

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

    # Consumer processes messages
    print("\nProcessing messages...")

    while broker.pending_messages() > 0:
        consumer.process_next_message()

    print("\nAll messages processed.")


if __name__ == "__main__":
    main()