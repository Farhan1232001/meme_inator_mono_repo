from django.core.management.base import BaseCommand, CommandError
from django.db import models
from apps.commentsections.infrastructure.models.comments_model import CommentModel
from apps.posts.infrastructure.models.post_model import PostModel
from apps.users.models import UserModel
from uuid import UUID


# # Delete comments from a specific post
# python manage.py delete_comments --post-id 550e8400-e29b-41d4-a716-446655440000

# # Delete all comments from all posts by username 'johndoe'
# python manage.py delete_comments --username a

# # Delete all comments (with confirmation)
# python manage.py delete_comments --all

# # Delete all comments older than 30 days (from all posts)
# python manage.py delete_comments --all --older-than-days 30 --force

# # Soft delete comments from a user, only top-level comments
# python manage.py delete_comments --username alice --max-level 0 --soft-delete

# # Dry run to see what would be deleted
# python manage.py delete_comments --username bob --dry-run

# # Delete comments newer than 7 days from a specific post
# python manage.py delete_comments --post-id 550e8400-e29b-41d4-a716-446655440000 --newer-than-days 7

# # Delete comments at depth 2 or deeper from all posts by a user
# python manage.py delete_comments --username charlie --min-level 2
class Command(BaseCommand):
    help = "Deletes comments for posts with flexible targeting options"

    def add_arguments(self, parser):
        # Target options (mutually exclusive groups)
        target_group = parser.add_mutually_exclusive_group(required=True)
        target_group.add_argument('--post-id', type=str, help='UUID of a specific post')
        target_group.add_argument('--username', type=str, help='Delete comments from all posts by this username')
        target_group.add_argument('--user-id', type=str, help='Delete comments from all posts by this user ID')
        target_group.add_argument('--all', action='store_true', help='Delete ALL comments from ALL posts (use with caution)')
        
        # Additional options
        parser.add_argument('--include-replies', action='store_true', 
                          help='Also delete replies (already included by cascade, but kept for clarity)')
        parser.add_argument('--dry-run', action='store_true', 
                          help='Show what would be deleted without actually deleting')
        parser.add_argument('--force', action='store_true', 
                          help='Skip confirmation prompt when deleting all comments')
        parser.add_argument('--older-than-days', type=int, 
                          help='Only delete comments older than this many days')
        parser.add_argument('--newer-than-days', type=int, 
                          help='Only delete comments newer than this many days')
        parser.add_argument('--min-level', type=int, 
                          help='Only delete comments at or above this depth level')
        parser.add_argument('--max-level', type=int, 
                          help='Only delete comments at or below this depth level')
        parser.add_argument('--soft-delete', action='store_true', 
                          help='Soft delete (set is_deleted=True) instead of hard delete')

    def handle(self, *args, **options):
        post_id = options.get('post_id')
        username = options.get('username')
        user_id = options.get('user_id')
        delete_all = options.get('all')
        dry_run = options.get('dry_run')
        force = options.get('force')
        older_than_days = options.get('older_than_days')
        newer_than_days = options.get('newer_than_days')
        min_level = options.get('min_level')
        max_level = options.get('max_level')
        soft_delete = options.get('soft_delete')
        
        # Get the base queryset of comments to delete
        comments_queryset = self._get_comments_queryset(
            post_id, username, user_id, delete_all,
            older_than_days, newer_than_days, min_level, max_level
        )
        
        if comments_queryset is None:
            return
        
        # Count comments to be deleted
        total_comments = comments_queryset.count()
        
        if total_comments == 0:
            self.stdout.write(self.style.WARNING("⚠️ No comments found matching the criteria."))
            return
        
        # Show what will be deleted
        self._show_deletion_preview(comments_queryset, total_comments, soft_delete)
        
        # Confirm deletion for dangerous operations
        if not self._confirm_deletion(delete_all, force, dry_run, total_comments):
            return
        
        # Perform deletion
        if dry_run:
            self.stdout.write(self.style.SUCCESS(f"✅ Dry run completed. Would have deleted {total_comments} comment(s)."))
            return
        
        if soft_delete:
            deleted_count = self._soft_delete_comments(comments_queryset)
            self.stdout.write(self.style.SUCCESS(f"🗑️ Soft deleted {deleted_count} comment(s)"))
        else:
            deleted_count, _ = comments_queryset.delete()
            self.stdout.write(self.style.SUCCESS(f"🗑️ Hard deleted {deleted_count} comment(s)"))
        
        # Optionally update post comment counts
        if not soft_delete and not delete_all:
            self._update_post_counts(comments_queryset)

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------

    def _get_comments_queryset(self, post_id, username, user_id, delete_all,
                               older_than_days, newer_than_days, min_level, max_level):
        """Build the comments queryset based on targeting options."""
        
        # Determine target posts first
        if delete_all:
            target_posts = None  # All posts
        elif post_id:
            try:
                post = PostModel.objects.get(post_id=post_id, is_deleted=False)
                target_posts = [post]
            except PostModel.DoesNotExist:
                raise CommandError(f"Post {post_id} not found")
        elif username:
            try:
                user = UserModel.objects.get(user_name=username)
                target_posts = list(PostModel.objects.filter(author=user, is_deleted=False))
                if not target_posts:
                    self.stdout.write(self.style.WARNING(f"⚠️ No posts found for user '{username}'"))
                    return None
            except UserModel.DoesNotExist:
                raise CommandError(f"User '{username}' not found")
        elif user_id:
            try:
                user_uuid = UUID(user_id)
                user = UserModel.objects.get(id=user_uuid)
                target_posts = list(PostModel.objects.filter(author=user, is_deleted=False))
                if not target_posts:
                    self.stdout.write(self.style.WARNING(f"⚠️ No posts found for user ID {user_id}"))
                    return None
            except (ValueError, UserModel.DoesNotExist):
                raise CommandError(f"User with ID {user_id} not found")
        else:
            return None
        
        # Build base queryset
        if target_posts is None:  # --all
            queryset = CommentModel.objects.all()
        else:
            queryset = CommentModel.objects.filter(post__in=target_posts)
        
        # Apply date filters
        from django.utils import timezone
        from datetime import timedelta
        
        if older_than_days:
            cutoff_date = timezone.now() - timedelta(days=older_than_days)
            queryset = queryset.filter(created_at__lt=cutoff_date)
        
        if newer_than_days:
            cutoff_date = timezone.now() - timedelta(days=newer_than_days)
            queryset = queryset.filter(created_at__gt=cutoff_date)
        
        # Apply level filters
        if min_level is not None:
            queryset = queryset.filter(level__gte=min_level)
        
        if max_level is not None:
            queryset = queryset.filter(level__lte=max_level)
        
        return queryset

    def _show_deletion_preview(self, queryset, total_comments, soft_delete):
        """Display preview of comments to be deleted."""
        self.stdout.write("\n📋 Deletion Preview:")
        self.stdout.write(f"  Total comments: {total_comments}")
        
        if total_comments > 0 and total_comments < 100:  # Show details for small sets
            sample = queryset[:10]
            self.stdout.write("\n  Sample comments:")
            for comment in sample:
                self.stdout.write(f"    - ID: {comment.public_id}, Post: {comment.post_id}, "
                                f"Author: {comment.author.user_name}, Level: {comment.level}, "
                                f"Created: {comment.created_at.date()}")
        
        # Show statistics
        if total_comments > 0:
            stats = queryset.aggregate(
                avg_level=models.Avg('level'),
                min_level=models.Min('level'),
                max_level=models.Max('level'),
                oldest=models.Min('created_at'),
                newest=models.Max('created_at')
            )
            self.stdout.write(f"\n  Statistics:")
            self.stdout.write(f"    Level range: {stats['min_level']} - {stats['max_level']} (avg: {stats['avg_level']:.1f})")
            self.stdout.write(f"    Date range: {stats['oldest'].date()} to {stats['newest'].date()}")
        
        action = "Soft delete" if soft_delete else "Hard delete"
        self.stdout.write(f"\n  Action: {action}")

    def _confirm_deletion(self, delete_all, force, dry_run, total_comments):
        """Confirm deletion for dangerous operations."""
        if dry_run:
            return True
        
        # Always confirm for --all unless --force is used
        if delete_all and not force:
            self.stdout.write(self.style.WARNING("\n⚠️  WARNING: You are about to delete ALL comments from ALL posts!"))
            confirm = input("Are you sure you want to proceed? Type 'yes' to continue: ")
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.WARNING("Deletion cancelled."))
                return False
        
        # Confirm if deleting more than 1000 comments
        if total_comments > 1000 and not force:
            confirm = input(f"\n⚠️  You are about to delete {total_comments} comments. Continue? (y/n): ")
            if confirm.lower() != 'y':
                self.stdout.write(self.style.WARNING("Deletion cancelled."))
                return False
        
        return True

    def _soft_delete_comments(self, queryset):
        """Soft delete comments by setting is_deleted=True."""
        updated_count = queryset.update(is_deleted=True, updated_at=timezone.now())
        return updated_count

    def _update_post_counts(self, queryset):
        """Update comment counts for affected posts."""
        from django.db.models import Count, Q
        
        # Get distinct posts from the deleted comments
        post_ids = queryset.values_list('post_id', flat=True).distinct()
        
        for post_id in post_ids:
            try:
                post = PostModel.objects.get(post_id=post_id)
                # Count non-deleted comments for this post
                new_count = CommentModel.objects.filter(
                    post=post, 
                    is_deleted=False
                ).count()
                if new_count != post.comments_count:
                    post.comments_count = new_count
                    post.save(update_fields=['comments_count'])
                    self.stdout.write(f"  Updated post {post_id} comment count to {new_count}")
            except PostModel.DoesNotExist:
                pass