from django.db import models
from meme_inator_back import settings


class ProfileModel(models.Model):
    # --- Core identity ---
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        db_index=True,
    )

    # --- Profile appearance ---
    # TODO: convert _url to _key and make custom S3KeyField(models.CharField)
    description = models.TextField(null=True, blank=True)
    background_color = models.CharField(max_length=32, null=True, blank=True)
    profile_pic_url = models.URLField(null=True, blank=True)
    profile_header_img_url = models.URLField(null=True, blank=True)
    bg_img = models.URLField(null=True, blank=True)
    profile_theme_music_url = models.URLField()

    # --- Presence messages ---
    is_online_msg = models.CharField(max_length=255, null=True, blank=True)
    is_offline_msg = models.CharField(max_length=255, null=True, blank=True)

    # --- Counters ---
    upload_count = models.PositiveIntegerField(default=0)
    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    friends_count = models.PositiveIntegerField(default=0)
    likes_given = models.PositiveIntegerField(default=0)
    dislikes_given = models.PositiveIntegerField(default=0)
    posts_uploaded = models.PositiveIntegerField(default=0)
    comments_posted = models.PositiveIntegerField(default=0)

    # --- Timestamps ---
    last_updated = models.DateTimeField(auto_now=True)

    # ------------------------------------------------------------------
    # Behaviors / Domain accessors (not implemented by request)
    # ------------------------------------------------------------------

    def counts(self):
        """
        Returns ProfileCountsEntity
        """
        raise NotImplementedError

    def timestamps(self):
        """
        Returns ProfileTimestampsEntity
        """
        raise NotImplementedError

    def media(self):
        """
        Returns ProfileMediaEntity
        """
        raise NotImplementedError

    def presence(self):
        """
        Returns ProfilePresenceEntity
        """
        raise NotImplementedError

    def method(self, type_):
        """
        Generic behavior method as defined in the entity
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return f"Profile(user_id={self.user_id})"
