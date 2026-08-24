from queue import Queue
from threading import Lock


class MessageBroker:
    """
    Simple in-process message broker.

    Demonstrates Message-Oriented Communication:
    producers publish messages to a queue,
    consumers retrieve messages from the queue.
    """

    def __init__(self):
        self.queue = Queue()
        self.lock = Lock()

    def publish(self, message):
        """
        Add a message to the message queue.
        """
        with self.lock:
            self.queue.put(message)

        print(f"[Broker] Message published: {message}")

    def consume(self):
        """
        Retrieve the next available message.

        Returns:
            message if available
            None if the queue is empty
        """
        if self.queue.empty():
            return None

        message = self.queue.get()

        print(f"[Broker] Message consumed: {message}")

        return message

    def pending_messages(self):
        """
        Return the number of messages currently waiting.
        """
        return self.queue.qsize()