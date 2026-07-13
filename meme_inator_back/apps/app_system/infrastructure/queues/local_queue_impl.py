from queue import Queue
from apps.app_system.infrastructure.queues.i_queue_client import IQueueClient

class LocalQueueImpl(IQueueClient):
    """Simple in-memory queue for dev/testing."""

    def __init__(self):
        self._queue = Queue()

    def enqueue(self, message):
        self._queue.put(message)

    def dequeue(self):
        if self._queue.empty():
            return None
        return self._queue.get()

    def acknowledge(self, message):
        # No-op for local queue
        pass
