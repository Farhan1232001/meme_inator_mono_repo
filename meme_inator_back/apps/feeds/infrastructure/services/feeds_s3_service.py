class FeedsS3Service:
    """
    Abstraction over S3 (or whichever object storage you use).
    The hydrator will call get_public_url_or_signed_url to turn storage keys into accessible URLs.
    """

    def __init__(self, *, bucket_name: str, aws_client=None):
        self.bucket_name = bucket_name
        self._client = aws_client

    def get_public_url_or_signed_url(self, storage_key: str, expires_in_seconds: int = 3600) -> str:
        """
        Return a publicly accessible URL if the object is public, otherwise return a signed URL.

        Implementation may check object ACL or generate a signed URL using boto3.
        """
        raise NotImplementedError
