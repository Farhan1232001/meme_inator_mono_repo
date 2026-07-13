# apps/moderation_sys/models/content_model.py

# TODO: Delete this file. I decided to contain a loose-reference in ModeratonCase that references
# actual "ContentToModerate" across django app. So for example, a reference to django posts app pointing to PostModel. 

# import uuid
# from django.db import models

# from apps.moderation_sys.infrastructure.models.content_blob_model import ContentBlobModel

# class ContentTypeChoices(models.TextChoices):
#     IMG = "image"
#     VIDEO = "video"
#     TEXT = "text"



# # TODO: rename to ModerableContentModel which implies it may or may not have been moderated. Actually get rid of it. Better to loose-reference  model model (like PostModel) from Moderaton case
# # Create ModerationGateway in posts app, which then conenects to moderation_sys, from infra to infra layer. 
# class ContentToModerateModel(models.Model):
#     """Single responsibility: Track what needs moderation"""
#     id = models.UUIDField(primary_key=True, default=uuid.uuid7)
#     author_id = models.UUIDField()
#     policy_routing_key = models.CharField(max_length=255, db_index=True)
#     content_type = models.CharField(max_length=32, choices=ContentTypeChoices.choices)
    
#     # Reference to content, don't store it here
#     content_blob = models.ForeignKey(ContentBlobModel, on_delete=models.PROTECT)
    
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     region = models.CharField(
#         max_length=32,
#         null=True,
#         blank=True,
#     )
