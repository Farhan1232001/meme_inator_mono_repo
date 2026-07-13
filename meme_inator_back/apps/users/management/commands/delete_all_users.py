"""
Django management command to delete all users from the database.

This script safely removes all user accounts and their associated data.
Use with caution as this operation cannot be undone.

Features:
- Counts users before deletion (with confirmation)
- Uses transaction.atomic() for safe rollback on error
- Respects CASCADE relationships (profiles, posts, etc. will be deleted)
- Provides dry-run option to preview without deleting
- Shows progress during deletion

Usage:
    # Preview how many users will be deleted (dry run)
    python manage.py delete_all_users --dry-run
    
    # Delete all users with confirmation prompt
    python manage.py delete_all_users
    
    # Delete all users without confirmation (automated scripts)
    python manage.py delete_all_users --no-input
    
    # Force deletion without any prompts (dangerous)
    python manage.py delete_all_users --force
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
import time

User = get_user_model()


class Command(BaseCommand):
    help = "Deletes all users from the database (including their profiles and related data)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview how many users will be deleted without actually deleting them'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Skip confirmation prompts (use with extreme caution)'
        )
        parser.add_argument(
            '--no-input',
            action='store_true',
            help='Skip interactive confirmation (uses default yes for automation)'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        force = options['force']
        no_input = options['no_input']
        
        # Count total users
        total_users = User.objects.count()
        
        if total_users == 0:
            self.stdout.write(self.style.SUCCESS("✅ No users found in database. Nothing to delete."))
            return
        
        # Display warning with count
        self.stdout.write(self.style.WARNING("=" * 60))
        self.stdout.write(self.style.WARNING("⚠️  DANGER: This will delete ALL users from the database!"))
        self.stdout.write(self.style.WARNING("=" * 60))
        self.stdout.write(f"\n📊 Found {total_users} user(s) in the database.\n")
        
        if dry_run:
            self.stdout.write(self.style.NOTICE("🔍 DRY RUN MODE - No changes will be made"))
            self.stdout.write(f"\nWould delete {total_users} user(s) including:\n")
            
            # Show sample of users to be deleted
            sample_users = User.objects.all()[:5]
            for user in sample_users:
                self.stdout.write(f"  • {user.user_name} (ID: {user.id})")
            
            if total_users > 5:
                self.stdout.write(f"  • ... and {total_users - 5} more user(s)")
            
            self.stdout.write("\n\n✅ Dry run completed. No changes were made.")
            return
        
        # Handle confirmation
        confirmed = False
        
        if force:
            confirmed = True
            self.stdout.write(self.style.WARNING("⚠️  FORCE MODE: Deleting all users without confirmation..."))
        elif no_input:
            confirmed = True
            self.stdout.write(self.style.NOTICE("🤖 No-input mode: Proceeding with deletion..."))
        else:
            # Interactive confirmation
            self.stdout.write(self.style.ERROR("🚨 THIS ACTION CANNOT BE UNDONE! 🚨"))
            confirm = input(f"\nType 'DELETE ALL USERS' to confirm deletion of {total_users} user(s): ")
            
            if confirm == "DELETE ALL USERS":
                confirmed = True
                self.stdout.write(self.style.NOTICE("\nConfirmation received. Proceeding with deletion..."))
            else:
                self.stdout.write(self.style.ERROR("\n❌ Confirmation failed. No changes were made."))
                return
        
        if not confirmed:
            return
        
        # Perform deletion with transaction for safety
        start_time = time.time()
        
        try:
            with transaction.atomic():
                # Get count before deletion (for progress reporting)
                users_to_delete = User.objects.all()
                
                self.stdout.write(f"🗑️  Deleting {total_users} user(s) and their associated data...")
                
                # Optional: Show progress by deleting in batches
                batch_size = 100
                deleted_count = 0
                
                # Get all user IDs
                user_ids = list(users_to_delete.values_list('id', flat=True))
                
                # Delete in batches to show progress
                for i in range(0, len(user_ids), batch_size):
                    batch_ids = user_ids[i:i + batch_size]
                    batch_deleted, _ = User.objects.filter(id__in=batch_ids).delete()
                    deleted_count += batch_deleted
                    self.stdout.write(f"  Progress: {deleted_count}/{total_users} users deleted")
                
                elapsed_time = time.time() - start_time
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f"\n✅ Successfully deleted {deleted_count} user(s) "
                        f"in {elapsed_time:.2f} seconds"
                    )
                )
                
                # Verify deletion
                remaining_users = User.objects.count()
                if remaining_users == 0:
                    self.stdout.write(self.style.SUCCESS("✨ Database is now empty of users."))
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"⚠️  {remaining_users} user(s) still remain. "
                            f"Something might have gone wrong."
                        )
                    )
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error during deletion: {e}"))
            self.stdout.write(self.style.ERROR("Transaction rolled back. No changes were made."))
            raise