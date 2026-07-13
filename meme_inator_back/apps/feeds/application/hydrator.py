from typing import List, Optional
from urllib.parse import urlparse

from apps.posts.domain.entities.post_entity import PostEntity


class PostHydrator:
    """
    Hydrator turns storage facing data into client-ready data. 
    Here, S3 object keys are hydrated to become usable URLS. 
    
    
    Assumes FeedsS3Service interface
      class FeedsS3Service:
        def get_public_url_or_signed_url(self, storage_key: str) -> str:
            ...
    Converts PostEntity storage keys into client-ready URLs.

    Responsibilities:
      - Resolve imageURL / thumbnailURL S3 keys into usable URLs
      - Return new PostEntity objects (no in-place mutation)
      - Remain storage-agnostic except for delegated S3 calls
    """

    def __init__(self, s3_service):
        """
        :param s3_service: implements
            get_public_url_or_signed_url(storage_key: str) -> str
        """
        self._s3 = s3_service

    def hydrate(self, posts: List[PostEntity]) -> List[PostEntity]:
        """
        Hydrate a list of PostEntity objects.

        Rules:
          - If a URL already looks like a real URL, leave it untouched
          - If a storage key is missing or empty, skip hydration
          - Always return new PostEntity instances
        """
        hydrated_posts: List[PostEntity] = []

        for post in posts:
            post.set_image_url(
                self._hydrate_url(post.imageURL)
            )
            post.set_thumbnail_url(
                self._hydrate_url(post.thumbnailURL)
            )
            hydrated_posts.append(post)
        return hydrated_posts

    # -----------------------
    # Internal helpers
    # -----------------------
    def _hydrate_url(self, value: Optional[str]) -> Optional[str]:
        """
        Convert a storage key into a usable URL.

        Returns:
          - None if value is None
          - original value if already a URL
          - resolved URL if value is a storage key
        """
        if not value:
            return value

        if self._looks_like_url(value):
            return value

        return self._s3.get_public_url_or_signed_url(value)

    @staticmethod
    def _looks_like_url(value: str) -> bool:
        """
        Check if a string already appears to be a valid URL.
        """
        try:
            parsed = urlparse(value)
            return bool(parsed.scheme and parsed.netloc)
        except Exception:
            return False
