# apps/posts/management/commands/create_posts_for_user.py
from django.core.management.base import BaseCommand, CommandError
from apps.users.models import UserModel
from apps.posts.infrastructure.models.post_model import PostModel
from apps.posts.infrastructure.models.post_vote_model import PostVoteModel
from faker import Faker
from django.utils import timezone
from datetime import timedelta
import random
from uuid import uuid7

fake = Faker()


# # Create 10-20 posts per day for user 'johndoe' over the last 7 days, with default vote density 0.3
# python manage.py create_posts_for_user --username a --days 1 --min 1 --max 1

# # Create posts for user with ID, using fixed votes per user (10 votes each)
# python manage.py create_posts_for_user --user-id 123e4567-e89b-12d3-a456-426614174000 --days 14 --min 5 --max 15 --votes-per-user 10

# # Create posts but skip votes entirely
# python manage.py create_posts_for_user --username alice --days 30 --min 3 --max 8 --no-votes
class Command(BaseCommand):
    help = "Creates random posts for a specific user over the past N days, with optional votes from other users"

    def add_arguments(self, parser):
        # Target user specification (mutually exclusive)
        parser.add_argument('--username', type=str, help='Username of the target user')
        parser.add_argument('--user-id', type=str, help='UUID of the target user')

        # Post generation
        parser.add_argument('--days', type=int, default=30,
                            help='How many past days to simulate (default: 30)')
        parser.add_argument('--min', type=int, default=5,
                            help='Minimum posts per day (default: 5)')
        parser.add_argument('--max', type=int, default=20,
                            help='Maximum posts per day (default: 20)')

        # Vote generation (optional)
        parser.add_argument('--no-votes', action='store_true',
                            help='Skip creating votes on the posts')
        parser.add_argument('--vote-density', type=float, default=0.3,
                            help='Probability (0-1) that a random other user votes on each post (default: 0.3)')
        parser.add_argument('--votes-per-user', type=int, default=5,
                            help='Fixed number of votes per user (if vote-density not used)')

    def handle(self, *args, **options):
        # Validate user targeting
        username = options.get('username')
        user_id = options.get('user_id')
        if not username and not user_id:
            raise CommandError("You must specify either --username or --user-id")
        if username and user_id:
            raise CommandError("Cannot specify both --username and --user-id")

        # Find the target user
        target_user = self._get_target_user(username, user_id)
        if not target_user:
            raise CommandError(f"User not found: {username or user_id}")

        # Gather parameters
        days_back = options['days']
        min_posts = options['min']
        max_posts = options['max']
        no_votes = options['no_votes']
        vote_density = options['vote_density']
        votes_per_user = options['votes_per_user']

        # Get all other users for voting
        other_users = list(UserModel.objects.exclude(id=target_user.id))
        if no_votes:
            other_users = []  # no votes will be created

        # Phase 1: Create posts
        self.stdout.write(f"📝 Creating posts for user {target_user.user_name}...")
        all_posts = self._create_posts_for_user(target_user, days_back, min_posts, max_posts)
        total_posts = len(all_posts)
        self.stdout.write(self.style.SUCCESS(f"✅ Created {total_posts} posts"))

        # Phase 2: Create votes (if any)
        total_votes = 0
        if not no_votes and other_users and all_posts:
            self.stdout.write("\n👍 Creating votes from other users...")
            total_votes = self._create_votes_for_posts(all_posts, other_users, vote_density, votes_per_user)
            self.stdout.write(self.style.SUCCESS(f"✅ Created {total_votes} votes"))
        elif not no_votes and not other_users:
            self.stdout.write(self.style.WARNING("⚠️ No other users found – skipping vote creation"))

        # Phase 3: Display statistics
        self._display_statistics(target_user, total_posts, total_votes, len(other_users))

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------

    def _get_target_user(self, username, user_id):
        """Retrieve user by username or user_id."""
        try:
            if username:
                return UserModel.objects.get(user_name=username)
            else:
                return UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            return None

    def _create_posts_for_user(self, user, days_back, min_posts, max_posts):
        """Create posts for a given user over the specified days."""
        now = timezone.now()
        all_posts = []

        for days_ago in range(days_back):
            start_of_day = (now - timedelta(days=days_ago)).replace(hour=0, minute=0, second=0, microsecond=0)
            posts_today = random.randint(min_posts, max_posts)

            day_posts = []
            for _ in range(posts_today):
                created_on = start_of_day + timedelta(seconds=random.randint(0, 86399))
                width, height = random.choice([(1080, 1920), (1920, 1080)])
                seed = random.randint(1, 100000)

                post = PostModel.objects.create(
                    post_id=uuid7(),
                    author=user,
                    image_url=f'https://picsum.photos/seed/{seed}/{width}/{height}',
                    thumbnail_url=f'https://picsum.photos/seed/{seed}/300/300',
                    caption=fake.sentence(),
                    post_type=random.choice(['image', 'video']),
                    file_format=random.choice(['jpg', 'png', 'mp4']),
                    upvotes_count=0,
                    downvotes_count=0,
                    comments_count=random.randint(0, 100),
                    shares_count=random.randint(0, 50),
                    tags=fake.words(nb=5),
                    is_flagged=random.choice([True, False]),
                    is_deleted=False,
                    visibility=random.choice(['public', 'private', 'friends']),
                    created_on=created_on,
                )
                day_posts.append(post)

            all_posts.extend(day_posts)
            self.stdout.write(f"  Day {days_ago + 1}/{days_back}: Created {posts_today} posts")

        return all_posts

    def _create_votes_for_posts(self, posts, users, vote_density, votes_per_user):
        """Create votes on posts from the given users."""
        total_votes = 0

        if vote_density:
            # Each user votes on a percentage of posts
            for user in users:
                num_to_vote = int(len(posts) * vote_density)
                if num_to_vote == 0:
                    continue
                posts_to_vote = random.sample(posts, min(num_to_vote, len(posts)))
                for post in posts_to_vote:
                    # Already ensured user is not the author (users list excludes author)
                    vote_type = random.choices(
                        [PostVoteModel.VoteType.UPVOTE, PostVoteModel.VoteType.DOWNVOTE],
                        weights=[0.8, 0.2]
                    )[0]
                    try:
                        PostVoteModel.create_vote(post, user, vote_type)
                        total_votes += 1
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"  Failed to create vote: {e}"))
                self.stdout.write(f"  User {user.user_name}: Created {len(posts_to_vote)} votes")
        else:
            # Fixed votes per user
            for user in users:
                num_to_vote = min(votes_per_user, len(posts))
                posts_to_vote = random.sample(posts, num_to_vote)
                for post in posts_to_vote:
                    vote_type = random.choices(
                        [PostVoteModel.VoteType.UPVOTE, PostVoteModel.VoteType.DOWNVOTE],
                        weights=[0.8, 0.2]
                    )[0]
                    try:
                        PostVoteModel.create_vote(post, user, vote_type)
                        total_votes += 1
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"  Failed to create vote: {e}"))
                self.stdout.write(f"  User {user.user_name}: Created {len(posts_to_vote)} votes")

        return total_votes

    def _display_statistics(self, user, total_posts, total_votes, other_users_count):
        """Print summary statistics."""
        self.stdout.write("\n📊 Final Statistics:")
        self.stdout.write(f"  Target user: {user.user_name} (ID: {user.id})")
        self.stdout.write(f"  Total posts created: {total_posts}")
        self.stdout.write(f"  Total votes created: {total_votes}")
        if total_posts > 0:
            self.stdout.write(f"  Avg votes per post: {total_votes / total_posts:.2f}")
        if other_users_count > 0:
            self.stdout.write(f"  Voting users: {other_users_count}")
            self.stdout.write(f"  Avg votes per voting user: {total_votes / other_users_count:.2f}")
        else:
            self.stdout.write(f"  Voting users: none")

        if total_votes > 0:
            upvotes = PostVoteModel.objects.filter(vote_type='upvote').count()
            downvotes = PostVoteModel.objects.filter(vote_type='downvote').count()
            self.stdout.write(f"  Upvotes: {upvotes} ({upvotes/total_votes*100:.1f}%)")
            self.stdout.write(f"  Downvotes: {downvotes} ({downvotes/total_votes*100:.1f}%)")

        # Posts with votes
        posts_with_votes = PostModel.objects.filter(votes__isnull=False).count()
        self.stdout.write(f"  Posts with at least one vote: {posts_with_votes} ({posts_with_votes/total_posts*100:.1f}%)")