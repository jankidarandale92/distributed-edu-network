class LamportClock:

    def __init__(self):
        self.time = 0

    def tick(self):
        """
        Increment the logical clock for a local event.
        """
        self.time += 1
        return self.time

    def receive(self, received_time):
        """
        Update the logical clock when receiving
        a message from another process.

        Lamport rule:
        C = max(C, received_time) + 1
        """
        self.time = max(self.time, received_time) + 1
        return self.time

    def update(self, received_time):
        """
        Update the logical clock when receiving
        a message from another process.

        This method is an alias for receive()
        and is used by the Gateway and resource nodes.
        """
        return self.receive(received_time)

    def get_time(self):
        """
        Return the current logical clock value.
        """
        return self.time