from django.core.management.base import BaseCommand, CommandError
from django.db import models
from apps.users.models import UserModel
from apps.posts.infrastructure.models.post_model import PostModel
from apps.commentsections.infrastructure.models.comments_model import CommentModel
from apps.commentsections.infrastructure.models.comment_vote_model import CommentVoteModel
from faker import Faker
from django.utils import timezone
from datetime import timedelta
import random
from uuid import UUID, uuid7

fake = Faker()

# Usage examples:
#   # All posts from last 30 days
#   python manage.py create_random_comments --days 30 --min 5 --max 15 --vote-density 0.3
#   # Specific post by UUID
#   python manage.py create_random_comments --post-id 550e8400-e29b-41d4-a716-446655440000 --min 10 --max 20
#   # Posts by specific username
#   python manage.py create_random_comments --username a --min 8 --max 12
#   # Posts by specific user ID
#   python manage.py create_random_comments --user-id 123e4567-e89b-12d3-a456-426614174000 --min 5 --max 10

class Command(BaseCommand):
    help = "Creates random comments and comment votes for posts"

    def add_arguments(self, parser):
        # Post targeting
        parser.add_argument('--post-id', type=str, help='UUID of a specific post to add comments to')
        parser.add_argument('--username', type=str, help='Filter posts by author username')
        parser.add_argument('--user-id', type=str, help='Filter posts by author user ID')
        
        # Comment generation
        parser.add_argument('--days', type=int, default=30, 
                          help='How many past days to consider for posts (ignored if --post-id is used)')
        parser.add_argument('--min', type=int, default=5, 
                          help='Minimum comments per post')
        parser.add_argument('--max', type=int, default=15, 
                          help='Maximum comments per post')
        parser.add_argument('--reply-probability', type=float, default=0.4, 
                          help='Probability that a comment will have replies (0-1)')
        parser.add_argument('--max-depth', type=int, default=3, 
                          help='Maximum depth of comment threads')
        
        # Vote generation
        parser.add_argument('--vote-density', type=float, default=0.3, 
                          help='Probability (0-1) that a user will vote on a comment. Default: 0.3')
        parser.add_argument('--votes-per-user', type=int, default=10, 
                          help='Maximum number of votes per user (if vote-density not used)')

    def handle(self, *args, **options):
        # Parse arguments
        post_id_str = options.get('post_id')
        username = options.get('username')
        user_id_str = options.get('user_id')
        days_back = options['days']
        min_comments = options['min']
        max_comments = options['max']
        reply_prob = options['reply_probability']
        max_depth = options['max_depth']
        vote_density = options['vote_density']
        votes_per_user = options['votes_per_user']

        # Validate conflicting targeting options
        if sum(bool(x) for x in [post_id_str, username, user_id_str]) > 1:
            raise CommandError("Only one of --post-id, --username, or --user-id can be used at a time.")

        # Get target posts
        target_posts = self._get_target_posts(
            post_id_str, username, user_id_str, days_back
        )
        if not target_posts:
            self.stdout.write(self.style.WARNING("⚠️ No posts found matching the criteria."))
            return

        # Get all users for comment authors and votes
        users = list(UserModel.objects.all())
        if not users:
            self.stdout.write(self.style.WARNING("⚠️ No users found. Create users first."))
            return

        # Phase 1: Create comments
        self.stdout.write("\n💬 Phase 1: Creating comments...")
        all_comments = self._create_comments_for_posts(
            target_posts, users, min_comments, max_comments, reply_prob, max_depth
        )
        total_comments = len(all_comments)
        self.stdout.write(self.style.SUCCESS(f"✅ Created {total_comments} comments"))

        # Phase 2: Create comment votes
        if not all_comments:
            self.stdout.write(self.style.WARNING("⚠️ No comments created, skipping votes."))
        else:
            self.stdout.write("\n👍 Phase 2: Creating comment votes...")
            total_votes = self._create_votes_for_comments(
                all_comments, users, vote_density, votes_per_user
            )
            self.stdout.write(self.style.SUCCESS(f"✅ Created {total_votes} comment votes"))

        # Phase 3: Update post comment counts
        self._update_post_counts(target_posts)

        # Phase 4: Display statistics
        self._display_statistics(target_posts, total_comments, total_votes, users)

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------

    def _get_target_posts(self, post_id_str, username, user_id_str, days_back):
        """Determine which posts to target based on arguments."""
        if post_id_str:
            try:
                post_uuid = UUID(post_id_str)
                posts = list(PostModel.objects.filter(post_id=post_uuid, is_deleted=False))
                if not posts:
                    raise CommandError(f"Post with ID {post_id_str} not found.")
                return posts
            except ValueError:
                raise CommandError(f"Invalid UUID format for post-id: {post_id_str}")

        if username:
            try:
                user = UserModel.objects.get(user_name=username)
                posts = list(PostModel.objects.filter(author=user, is_deleted=False))
                if not posts:
                    raise CommandError(f"No posts found for username '{username}'.")
                return posts
            except UserModel.DoesNotExist:
                raise CommandError(f"User '{username}' not found.")

        if user_id_str:
            try:
                user_uuid = UUID(user_id_str)
                user = UserModel.objects.get(id=user_uuid)
                posts = list(PostModel.objects.filter(author=user, is_deleted=False))
                if not posts:
                    raise CommandError(f"No posts found for user ID {user_id_str}.")
                return posts
            except (ValueError, UserModel.DoesNotExist):
                raise CommandError(f"User with ID {user_id_str} not found.")

        # No specific targeting: use date range
        cutoff = timezone.now() - timedelta(days=days_back)
        return list(PostModel.objects.filter(created_on__gte=cutoff, is_deleted=False))

    def _create_comments_for_posts(self, posts, users, min_comments, max_comments, reply_prob, max_depth):
        """Create comments for given posts and return list of all created comments."""
        all_comments = []

        def create_comment_recursive(post, parent_comment, current_depth, max_depth_allowed):
            if current_depth > max_depth_allowed:
                return None

            user = random.choice(users)
            comment = CommentModel.objects.create(
                post=post,
                author=user,
                content=fake.paragraph(nb_sentences=random.randint(1, 3)),
                parent=parent_comment,
                level=current_depth,
                is_deleted=False,
                is_flagged=random.random() < 0.05,  # 5% flagged
                reply_count=0,
                upvote_count=0,
                downvote_count=0
            )
            all_comments.append(comment)

            # Randomly add replies
            if current_depth < max_depth_allowed and random.random() < reply_prob:
                num_replies = random.randint(0, 3)
                for _ in range(num_replies):
                    reply = create_comment_recursive(post, comment, current_depth + 1, max_depth_allowed)
                    if reply:
                        comment.reply_count += 1
                if num_replies > 0:
                    comment.save(update_fields=['reply_count'])

            return comment

        for post in posts:
            num_comments = random.randint(min_comments, max_comments)
            for _ in range(num_comments):
                create_comment_recursive(post, None, 0, max_depth)

        return all_comments

    def _create_votes_for_comments(self, comments, users, vote_density, votes_per_user):
        """Create votes for comments using a comment‑centric bulk approach."""
        from django.db import connection
        from collections import defaultdict
        import random

        total_votes = 0
        vote_objects = []
        comment_vote_counts = defaultdict(int)

        # Determine how many votes each comment should get
        if vote_density:
            votes_per_comment = int(len(users) * vote_density)
            if votes_per_comment <= 0:
                return 0
        else:
            votes_per_comment = votes_per_user

        # For each comment, sample users and create vote objects
        self.stdout.write(f"  Generating {len(comments)} comments with ~{votes_per_comment} votes each...")
        
        for comment in comments:
            # Filter out the comment author
            eligible_users = [u for u in users if u.id != comment.author_id]
            if not eligible_users:
                continue
                
            if len(eligible_users) < votes_per_comment:
                selected_users = eligible_users
            else:
                selected_users = random.sample(eligible_users, votes_per_comment)

            for voter in selected_users:
                vote_type = random.choices(
                    [CommentVoteModel.VoteType.UPVOTE, CommentVoteModel.VoteType.DOWNVOTE],
                    weights=[0.8, 0.2]
                )[0]
                vote_objects.append(
                    CommentVoteModel(
                        comment=comment,
                        user=voter,
                        vote_type=vote_type
                    )
                )
                comment_vote_counts[comment.id] += 1
                total_votes += 1

        # Bulk insert votes
        if vote_objects:
            self.stdout.write(f"  Bulk inserting {len(vote_objects)} votes...")
            try:
                CommentVoteModel.objects.bulk_create(vote_objects, ignore_conflicts=True, batch_size=5000)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Bulk insert failed: {e}. Falling back to individual inserts."))
                for vo in vote_objects:
                    try:
                        vo.save()
                    except Exception:
                        pass

        # Update comment counters using a single query with proper IN clause formatting
        if comments:
            self.stdout.write("\n📊 Recalculating comment vote counts...")
            comment_ids = [comment.id for comment in comments]
            
            # Convert the list to a tuple for SQL IN clause
            # PostgreSQL requires the list to be formatted correctly
            placeholders = ','.join(['%s'] * len(comment_ids))
            
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    UPDATE commentsections_commentmodel
                    SET upvote_count = (
                        SELECT COUNT(*) FROM commentsections_commentvotemodel
                        WHERE comment_id = commentsections_commentmodel.id
                        AND vote_type = 'upvote'
                    ),
                    downvote_count = (
                        SELECT COUNT(*) FROM commentsections_commentvotemodel
                        WHERE comment_id = commentsections_commentmodel.id
                        AND vote_type = 'downvote'
                    )
                    WHERE id IN ({placeholders})
                """, comment_ids)

        return total_votes

    def _update_post_counts(self, posts):
        """Update comments_count on each post to match actual number of comments."""
        self.stdout.write("\n📊 Phase 3: Updating post comment counts...")
        for post in posts:
            actual = CommentModel.objects.filter(post=post, is_deleted=False).count()
            if actual != post.comments_count:
                post.comments_count = actual
                post.save(update_fields=['comments_count'])

    def _display_statistics(self, posts, total_comments, total_votes, users):
        """Display final statistics about created comments and votes."""
        self.stdout.write("\n📊 Final Statistics:")
        self.stdout.write(f"  Total posts processed: {len(posts)}")
        self.stdout.write(f"  Total comments created: {total_comments}")
        self.stdout.write(f"  Total comment votes created: {total_votes}")
        if total_comments > 0:
            self.stdout.write(f"  Avg comments per post: {total_comments / len(posts):.2f}")
        if users and total_votes > 0:
            self.stdout.write(f"  Avg votes per user: {total_votes / len(users):.2f}")

        if total_votes > 0:
            upvotes = CommentVoteModel.objects.filter(vote_type='upvote').count()
            downvotes = CommentVoteModel.objects.filter(vote_type='downvote').count()
            self.stdout.write(f"  Upvotes: {upvotes} ({upvotes/total_votes*100:.1f}%)")
            self.stdout.write(f"  Downvotes: {downvotes} ({downvotes/total_votes*100:.1f}%)")

            # Depth distribution
            depth_dist = CommentModel.objects.values('level').annotate(count=models.Count('id')).order_by('level')
            if depth_dist:
                self.stdout.write("\n  Comment depth distribution:")
                for item in depth_dist:
                    self.stdout.write(f"    Level {item['level']}: {item['count']} comments")

        # Comments with votes
        if total_comments > 0:
            posts_with_comments = PostModel.objects.filter(comments__isnull=False).distinct().count()
            self.stdout.write(f"\n  Posts with at least one comment: {posts_with_comments} ({posts_with_comments/len(posts)*100:.1f}%)")
            if total_votes > 0:
                comments_with_votes = CommentModel.objects.filter(votes__isnull=False).distinct().count()
                self.stdout.write(f"  Comments with at least one vote: {comments_with_votes} ({comments_with_votes/total_comments*100:.1f}%)")