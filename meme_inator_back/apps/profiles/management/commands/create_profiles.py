# you can save this as create_profiles_for_users.py or as a Django management command

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.users.infrastructure.models.user_model import UserModel
from apps.profiles.infrastructure.models.profile_model import ProfileModel
from faker import Faker
import random
from datetime import datetime

fake = Faker()

class Command(BaseCommand):
    help = 'Creates profiles for all users that dont have one'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without actually creating',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Get all users
        all_users = UserModel.objects.all()
        self.stdout.write(f"Total users found: {all_users.count()}")
        
        users_without_profile = []
        for user in all_users:
            try:
                # Check if profile exists - adjust based on your actual relation
                # This might be user.profile or ProfileModel.objects.get(user=user)
                profile_exists = ProfileModel.objects.filter(user=user).exists()
                if not profile_exists:
                    users_without_profile.append(user)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Error checking user {user.id}: {e}"))
        
        self.stdout.write(f"Users without profiles: {len(users_without_profile)}")
        
        if dry_run:
            self.stdout.write(self.style.SUCCESS("DRY RUN - Would create profiles for:"))
            for user in users_without_profile:
                self.stdout.write(f"  - {user.username} (ID: {user.id})")
            return
        
        # Create profiles
        created_count = 0
        for user in users_without_profile:
            try:
                with transaction.atomic():
                    profile = self._create_profile_for_user(user)
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"✅ Created profile for {user.username}")
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"❌ Failed to create profile for {user.username}: {e}")
                )
        
        self.stdout.write(
            self.style.SUCCESS(f"\n✅ Done! Created {created_count} profiles")
        )
    
    def _create_profile_for_user(self, user):
        """Create a single profile for a user with dummy data"""
        
        # Generate random seeds for images
        seed_profile = random.randint(1, 10000)
        seed_header = random.randint(1, 10000)
        seed_background = random.randint(1, 10000)
        
        # Create profile based on your ProfileModel structure
        # Adjust field names to match your actual ProfileModel
        profile = ProfileModel.objects.create(
            user=user,
            
            # Profile appearance
            profile_pic_url=f"https://picsum.photos/seed/{seed_profile}/400/400",
            profile_header_img_url=f"https://picsum.photos/seed/{seed_header}/1200/400",
            bg_img=f"https://picsum.photos/seed/{seed_background}/800/600",
            background_color=fake.hex_color(),
            description=fake.sentence(nb_words=15),
            
            # Music - using a reliable public audio file
            profile_theme_music_url='https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3',
            
            # Presence messages
            is_online_msg=random.choice(['online', 'available', 'here']),
            is_offline_msg=random.choice(['offline', 'away', 'be right back']),
            
            # Counters - mostly zero initially
            upload_count=0,
            followers_count=random.randint(0, 100),
            following_count=random.randint(0, 100),
            friends_count=random.randint(0, 50),
            likes_given=random.randint(0, 500),
            posts_uploaded=0,
            comments_posted=random.randint(0, 200),
            dislikes_given=random.randint(0, 100),
            
            # Timestamp
            last_updated=datetime.now(),
        )
        
        return profile