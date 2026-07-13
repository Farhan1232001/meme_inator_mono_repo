from django.core.management.base import BaseCommand
from apps.posts.infrastructure.models.post_model import PostModel

class Command(BaseCommand):
    help = "Deletes all posts"

    def handle(self, *args, **kwargs):
        count = PostModel.objects.count()
        PostModel.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"🗑️ Deleted {count} posts"))
