"""
Django management command to create random users with bulk creation optimization.

This script has been optimized for performance when creating large numbers of users.
Key optimizations include:
- Pre-hashing passwords (hash once, reuse for all users)
- Bulk creation using Django's bulk_create (reduces database round trips)
- Transaction batching (groups operations for better performance)

Business logic:
- Each created user automatically gets a corresponding ProfileModel instance.
- The profile can be used to store user-specific data such as posts, media, counters, etc.

Changelog (Optimizations):
-------------------------
v2.0 - Performance improvements:
    - Password hashing is now done once using make_password() instead of per-user
    - Users are created in batches using bulk_create (default batch size 100)
    - Each batch is wrapped in a transaction.atomic() for efficiency
    - Added --batch-size argument for tuning
    - Reduced overhead from individual save() calls and signal processing

v2.1 - Feature addition:
    - Profiles are now automatically created for each user in bulk
    - Profiles are linked via OneToOneField and created in the same transaction
    - Profile data includes random descriptions and default values
    - Documentation updated to reflect profile creation

v2.2 - Bug fix:
    - Fixed required field `profile_theme_music_url` - now set to a default URL
    - Added random generation for all profile fields (profile_pic_url, header, etc.)
    - Improved error handling and fallback logic
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import transaction
from faker import Faker
import random
import time
from uuid import uuid7

fake = Faker()
User = get_user_model()

# Import ProfileModel – adjust import path to match your project
from apps.profiles.infrastructure.models.profile_model import ProfileModel

# Default URL for profile theme music (public audio file)
DEFAULT_MUSIC_URL = 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'

### Usage ###
# Default user password is testpass123
#
# Create 20 users with random generated usernames (default)
# python manage.py create_random_users --count 20
#
# Create 20 users with sequential simple usernames (user_000, user_001, etc.)
# python manage.py create_random_users --count 20 --simple
#
# Override password for users
# python manage.py create_random_users --count 5 --password 'securepass'
#
# Combine options: 50 users, simple usernames, custom password
# python manage.py create_random_users --count 50 --simple --password 'mypass123'
#
# Control batch size (default 100) for bulk creation:
# python manage.py create_random_users --count 1000 --batch-size 200
class Command(BaseCommand):
    help = "Creates random users with fake data (optimized for bulk creation)."

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of users to create (default: 10)'
        )
        parser.add_argument(
            '--password',
            type=str,
            default='testpass123',
            help='Default password for all created users (default: testpass123)'
        )
        parser.add_argument(
            '--simple',
            action='store_true',
            help='Use simple sequential usernames (user_000, user_001, etc.) instead of random names'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=100,
            help='Number of users to create in each batch (default: 100)'
        )

    def handle(self, *args, **options):
        count = options['count']
        default_password = options['password']
        use_simple = options['simple']
        batch_size = options['batch_size']
        
        start_time = time.time()
        self.stdout.write(f"Creating {count} random users...")
        
        if use_simple:
            self.stdout.write("Using simple sequential usernames (user_XXX format)")
        
        # Step 1: Pre-hash the password once (major performance gain)
        hashed_password = make_password(default_password)
        
        # Step 2: Determine starting number for simple usernames if needed
        next_number = 0
        if use_simple:
            existing_numbers = set()
            # Find all existing usernames that match the pattern "user_XXX"
            existing_users = User.objects.filter(user_name__regex=r'^user_\d+$')
            for user in existing_users:
                try:
                    num = int(user.user_name.split('_')[1])
                    existing_numbers.add(num)
                except (IndexError, ValueError):
                    pass
            # Find the next available number
            while next_number in existing_numbers:
                next_number += 1
        
        # Step 3: Prepare all users in a list (no saving yet)
        users_to_create = []
        created_count = 0
        
        for i in range(count):
            if use_simple:
                username = f"user_{next_number:03d}"
                email = f"{username}@example.com"
                next_number += 1
            else:
                # Generate unique username and email
                username = f"{fake.user_name()}_{uuid7().hex[:8]}"
                email = f"{fake.user_name()}_{uuid7().hex[:8]}@example.com"
            
            # Generate random boolean fields
            is_online = random.choices([True, False], weights=[99, 1])[0]
            is_verified = random.choices([True, False], weights=[1, 99])[0]
            is_banned = random.choices([True, False], weights=[1, 99])[0]
            
            # Create User instance (not saved yet)
            user = User(
                id=uuid7(),
                user_name=username,
                email=email,
                password=hashed_password,  # Use pre-hashed password
                is_online=is_online,
                is_verified=is_verified,
                is_banned=is_banned,
            )
            users_to_create.append(user)
            
            # Batch creation when batch size reached or last user
            if len(users_to_create) >= batch_size or i == count - 1:
                try:
                    with transaction.atomic():
                        # 1. Create users
                        created_users = User.objects.bulk_create(
                            users_to_create,
                            batch_size=batch_size,
                            ignore_conflicts=False
                        )
                        created_count += len(created_users)
                        
                        # 2. Create profiles for these users
                        profiles_to_create = []
                        for user_obj in created_users:
                            profile = self._create_profile_instance(user_obj)
                            profiles_to_create.append(profile)
                        
                        # Bulk create profiles
                        if profiles_to_create:
                            ProfileModel.objects.bulk_create(
                                profiles_to_create,
                                batch_size=batch_size
                            )
                        
                        self.stdout.write(f"  Created batch of {len(created_users)} users with profiles (total users: {created_count})")
                        
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"  Batch creation failed: {e}"))
                    # Fallback: create users individually with their profiles
                    for user in users_to_create:
                        try:
                            with transaction.atomic():
                                user.save()
                                # Create profile for this user
                                profile = self._create_profile_instance(user)
                                profile.save()
                                created_count += 1
                                self.stdout.write(f"    Created user {user.user_name} with profile")
                        except Exception as ind_error:
                            self.stdout.write(self.style.ERROR(
                                f"  Failed to create user {user.user_name} with profile: {ind_error}"
                            ))
                finally:
                    # Clear batch list for next iteration
                    users_to_create = []
        
        elapsed_time = time.time() - start_time
        
        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Successfully created {created_count} users with profiles "
                f"in {elapsed_time:.2f} seconds "
                f"({created_count / elapsed_time:.1f} users/second)"
            )
        )

    def _create_profile_instance(self, user):
        """Create a ProfileModel instance with random dummy data."""
        # Generate random image seeds
        seed_profile = random.randint(1, 10000)
        seed_header = random.randint(1, 10000)
        seed_background = random.randint(1, 10000)
        
        # Create profile with required fields (especially profile_theme_music_url)
        profile = ProfileModel(
            user=user,
            description=fake.sentence(nb_words=15) if random.random() > 0.5 else None,
            background_color=fake.hex_color() if random.random() > 0.3 else None,
            profile_pic_url=f"https://picsum.photos/seed/{seed_profile}/400/400",
            profile_header_img_url=f"https://picsum.photos/seed/{seed_header}/1200/400",
            bg_img=f"https://picsum.photos/seed/{seed_background}/800/600",
            profile_theme_music_url=DEFAULT_MUSIC_URL,  # Required field, always set
            is_online_msg=random.choice(['online', 'available', 'here']) if random.random() > 0.5 else None,
            is_offline_msg=random.choice(['offline', 'away', 'be right back']) if random.random() > 0.5 else None,
            upload_count=0,
            followers_count=random.randint(0, 100),
            following_count=random.randint(0, 100),
            friends_count=random.randint(0, 50),
            likes_given=random.randint(0, 500),
            dislikes_given=random.randint(0, 100),
            posts_uploaded=0,
            comments_posted=random.randint(0, 200),
        )
        return profile