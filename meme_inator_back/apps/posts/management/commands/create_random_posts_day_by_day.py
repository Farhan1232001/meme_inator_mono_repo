from django.core.management.base import BaseCommand
from apps.users.models import UserModel
from apps.posts.infrastructure.models.post_model import PostModel
from apps.posts.infrastructure.models.post_vote_model import PostVoteModel
from faker import Faker
from django.utils import timezone
from datetime import timedelta
import random
from uuid import uuid7

fake = Faker()

# python manage.py create_random_posts_day_by_day --days 7 --min 6 --max 6 --vote-density 0.3
# python manage.py delete_all_posts
class Command(BaseCommand):
    help = "Creates a random number of posts per day over the past N days, for all users, with random votes"

    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, default=30, help='How many past days to simulate')
        parser.add_argument('--min', type=int, default=5, help='Minimum posts per day')
        parser.add_argument('--max', type=int, default=20, help='Maximum posts per day')
        parser.add_argument('--vote-density', type=float, default=0.3, 
                          help='Probability (0-1) that a user will vote on a post. Default: 0.3')
        parser.add_argument('--votes-per-user', type=int, default=5, 
                          help='Maximum number of votes per user (if vote-density not used)')

    def handle(self, *args, **options):
        days_back = options['days']
        min_posts = options['min']
        max_posts = options['max']
        vote_density = options['vote_density']
        votes_per_user = options['votes_per_user']

        users = list(UserModel.objects.all())
        if not users:
            self.stdout.write(self.style.WARNING("⚠️ No users found. Create users first."))
            return

        total_posts_created = 0
        total_votes_created = 0
        now = timezone.now()
        all_posts = []  # Store created posts for vote generation

        # Phase 1: Create posts
        self.stdout.write("📝 Phase 1: Creating posts...")
        for days_ago in range(days_back):
            start_of_day = (now - timedelta(days=days_ago)).replace(hour=0, minute=0, second=0, microsecond=0)
            posts_today = random.randint(min_posts, max_posts)

            day_posts = []
            for _ in range(posts_today):
                user = random.choice(users)
                created_on = start_of_day + timedelta(seconds=random.randint(0, 86399))
                width, height = random.choice([(1080, 1920), (1920, 1080)])
                seed = random.randint(1, 100000)

                post = PostModel.objects.create(
                    post_id=uuid7(),
                    author_id=user.id,
                    image_url=f'https://picsum.photos/seed/{seed}/{width}/{height}',
                    thumbnail_url=f'https://picsum.photos/seed/{seed}/300/300',
                    caption=fake.sentence(),
                    post_type=random.choice(['image', 'video']),
                    file_format=random.choice(['jpg', 'png', 'mp4']),
                    upvotes_count=0,  # Start at 0, will be updated by votes
                    downvotes_count=0,  # Start at 0, will be updated by votes
                    comments_count=random.randint(0, 100),
                    shares_count=random.randint(0, 50),
                    tags=fake.words(nb=5),
                    is_flagged=random.choice([True, False]),
                    is_deleted=False,
                    visibility=random.choice(['public', 'private', 'friends']),
                    created_on=created_on,
                )
                
                day_posts.append(post)
                total_posts_created += 1
            
            all_posts.extend(day_posts)
            self.stdout.write(f"  Day {days_ago + 1}/{days_back}: Created {posts_today} posts")

        self.stdout.write(self.style.SUCCESS(f"✅ Created {total_posts_created} posts across {days_back} days"))

        # Phase 2: Create votes
        self.stdout.write("\n👍 Phase 2: Creating votes...")
        
        # Determine how many votes to create per user
        if vote_density:
            # Use density approach: each user votes on a percentage of posts
            for user in users:
                posts_to_vote_on = random.sample(all_posts, 
                    min(int(len(all_posts) * vote_density), len(all_posts)))
                
                for post in posts_to_vote_on:
                    # Don't allow users to vote on their own posts
                    if post.author_id == user.id:
                        continue
                    
                    # Randomly choose vote type (80% upvote, 20% downvote)
                    vote_type = random.choices(
                        [PostVoteModel.VoteType.UPVOTE, PostVoteModel.VoteType.DOWNVOTE],
                        weights=[0.8, 0.2]
                    )[0]
                    
                    try:
                        PostVoteModel.create_vote(post, user, vote_type)
                        total_votes_created += 1
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"  Failed to create vote: {e}"))
                
                self.stdout.write(f"  User {user.user_name}: Created {len(posts_to_vote_on)} votes")
        
        else:
            # Use fixed number of votes per user approach
            for user in users:
                # Randomly select posts for this user to vote on
                posts_to_vote_on = random.sample(all_posts, 
                    min(votes_per_user, len(all_posts)))
                
                for post in posts_to_vote_on:
                    # Don't allow users to vote on their own posts
                    if post.author_id == user.id:
                        continue
                    
                    # Randomly choose vote type (80% upvote, 20% downvote)
                    vote_type = random.choices(
                        [PostVoteModel.VoteType.UPVOTE, PostVoteModel.VoteType.DOWNVOTE],
                        weights=[0.8, 0.2]
                    )[0]
                    
                    try:
                        PostVoteModel.create_vote(post, user, vote_type)
                        total_votes_created += 1
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"  Failed to create vote: {e}"))
                
                self.stdout.write(f"  User {user.user_name}: Created {len(posts_to_vote_on)} votes")

        self.stdout.write(self.style.SUCCESS(f"✅ Created {total_votes_created} votes"))

        # Phase 3: Display statistics
        self.stdout.write("\n📊 Final Statistics:")
        self.stdout.write(f"  Total posts: {total_posts_created}")
        self.stdout.write(f"  Total votes: {total_votes_created}")
        self.stdout.write(f"  Avg votes per post: {total_votes_created / total_posts_created:.2f}")
        self.stdout.write(f"  Avg votes per user: {total_votes_created / len(users):.2f}")

        # Show vote distribution
        upvotes = PostVoteModel.objects.filter(vote_type='upvote').count()
        downvotes = PostVoteModel.objects.filter(vote_type='downvote').count()
        self.stdout.write(f"  Upvotes: {upvotes} ({upvotes/total_votes_created*100:.1f}%)" if total_votes_created > 0 else "  Upvotes: 0")
        self.stdout.write(f"  Downvotes: {downvotes} ({downvotes/total_votes_created*100:.1f}%)" if total_votes_created > 0 else "  Downvotes: 0")

        # Verify some posts have votes
        posts_with_votes = PostModel.objects.filter(votes__isnull=False).distinct().count()
        self.stdout.write(f"  Posts with at least one vote: {posts_with_votes} ({posts_with_votes/total_posts_created*100:.1f}%)")