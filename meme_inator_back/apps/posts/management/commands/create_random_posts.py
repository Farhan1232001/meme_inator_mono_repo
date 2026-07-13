from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from datetime import datetime, timedelta, timezone as dt_timezone
from faker import Faker
import random
from uuid7 import uuid7

from users.models import User
from posts.models import PostModel

fake = Faker()

class Command(BaseCommand):
    help = "Generate <count> random posts on the given <date> (YYYY-MM-DD), defaulting to today if omitted."

    def add_arguments(self, parser):
        parser.add_argument('--date', type=str, help="Target date for posts (YYYY-MM-DD)")
        parser.add_argument('--count', type=int, required=True, help="Number of posts to generate")

    def handle(self, *args, **options):
        date_str = options.get('date')
        count = options['count']

        if date_str:
            try:
                target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                raise CommandError(f"Invalid date '{date_str}'. Use YYYY-MM-DD.")
        else:
            target_date = timezone.now().date()

        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.WARNING("⚠️ No users found. Create users first."))
            return

        midnight = datetime.combine(target_date, datetime.min.time(), tzinfo=dt_timezone.utc)

        for _ in range(count):
            user = random.choice(users)
            created_on = midnight + timedelta(seconds=random.randint(0, 86399))
            width, height = random.choice([(1080, 1920), (1920, 1080)])
            seed = random.randint(1, 100000)

            PostModel.objects.create(
                post_id=uuid7(),
                author_id=user.id,
                image_url=f'https://picsum.photos/seed/{seed}/{width}/{height}',
                thumbnail_url=f'https://picsum.photos/seed/{seed}/300/300',
                caption=fake.sentence(),
                post_type=random.choice(['image', 'video']),
                file_format=random.choice(['jpg', 'png', 'mp4']),
                upvotes_count=random.randint(0, 1000),
                downvotes_count=random.randint(0, 200),
                comments_count=random.randint(0, 100),
                shares_count=random.randint(0, 50),
                tags=fake.words(nb=5),
                is_flagged=random.choice([True, False]),
                is_deleted=False,
                visibility=random.choice(['public', 'private', 'friends']),
                created_on=created_on,
            )

        self.stdout.write(self.style.SUCCESS(f"✅ Created {count} random posts on {target_date}"))
