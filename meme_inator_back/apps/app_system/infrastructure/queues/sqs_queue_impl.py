import boto3
from apps.app_system.infrastructure.queues.i_queue_client import IQueueClient

class SQSQueueImpl(IQueueClient):
    """
    Stub implementation for AWS SQS.
    Requires AWS credentials configured in your environment.
    """

    def __init__(self, queue_url: str):
        self._queue_url = queue_url
        self._client = boto3.client("sqs")

    def enqueue(self, message):
        self._client.send_message(
            QueueUrl=self._queue_url,
            MessageBody=str(message)
        )

    def dequeue(self):
        resp = self._client.receive_message(
            QueueUrl=self._queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=1
        )
        messages = resp.get("Messages", [])
        return messages[0] if messages else None

    def acknowledge(self, message):
        if not message:
            return
        receipt = message.get("ReceiptHandle")
        if receipt:
            self._client.delete_message(
                QueueUrl=self._queue_url,
                ReceiptHandle=receipt
            )
