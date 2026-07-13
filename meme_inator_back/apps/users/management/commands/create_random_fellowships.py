"""
Django management command to create random uni-directional follow relationships (fellowships).

Graph Theory Context:
    - Users are nodes.
    - Each fellowship is a directed edge from follower → followed.
    - Maximum possible edges in a complete directed graph without self-loops: n x (n-1)

Example:
    With 100 users: 100 x 99 = 9,900 possible fellowships.

Usage Examples:
    # Create 500 fellowships
    python manage.py create_random_fellowships --count 500

    # Create 2000 fellowships with verbose output
    python manage.py create_random_fellowships --count 2000 --verbose

    # Try to create 10000 fellowships with more attempts
    python manage.py create_random_fellowships --count 10000 --max-attempts 20000

    # Control batch size for bulk creation
    python manage.py create_random_fellowships --count 5000 --batch-size 200
"""

from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction
import random
import time
from uuid import uuid7
from django.utils import timezone

from apps.users.infrastructure.models.user_model import UserModel
from apps.users.infrastructure.models.fellowship_model import FellowshipModel


class Command(BaseCommand):
    help = "Creates random uni-directional follow relationships (fellowships)."

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=100,
            help='Number of fellowships to create (default: 100)'
        )
        parser.add_argument(
            '--max-attempts',
            type=int,
            default=5000,
            help='Maximum random selection attempts before giving up (default: 5000)'
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed output including skipped attempts'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=100,
            help='Number of fellowships to create in each batch (default: 100)'
        )

    def calculate_max_fellowships(self, user_count):
        """Maximum directed edges without self-loops = n x (n-1)"""
        return user_count * (user_count - 1)

    def handle(self, *args, **options):
        count = options['count']
        max_attempts = options['max_attempts']
        verbose = options['verbose']
        batch_size = options['batch_size']

        # Fetch all active users (nodes)
        users = list(UserModel.objects.filter(is_soft_deleted=False))
        user_ids = [user.id for user in users]
        user_count = len(user_ids)

        self.stdout.write(f"Found {user_count} active users")

        if user_count < 2:
            self.stdout.write(self.style.ERROR(
                "Need at least 2 users to create fellowships."
            ))
            return

        # Theoretical maximum
        max_possible = self.calculate_max_fellowships(user_count)
        self.stdout.write(f"Maximum possible fellowships: {max_possible}")

        if count > max_possible:
            self.stdout.write(self.style.WARNING(
                f"Requested {count} fellowships but only {max_possible} possible. "
                f"Will create as many as possible."
            ))
            count = max_possible

        # Track existing edges (active only)
        existing_edges = set()
        existing_fellowships = FellowshipModel.objects.filter(
            is_soft_deleted=False
        ).values_list('user_id', 'followed_user_id')
        for user_id, followed_id in existing_fellowships:
            existing_edges.add((user_id, followed_id))

        self.stdout.write(f"Found {len(existing_edges)} existing active fellowships")

        created_count = 0
        skipped_count = 0
        attempt_count = 0

        # We'll use bulk creation for performance
        fellowship_batch = []
        start_time = time.time()

        while created_count < count and attempt_count < max_attempts:
            attempt_count += 1

            # Select two distinct users
            follower, followed = random.sample(user_ids, 2)

            # Skip if edge already exists or if it's a self-follow (already prevented by sample)
            if (follower, followed) in existing_edges:
                if verbose:
                    self.stdout.write(f"  Skipping: {follower} already follows {followed}")
                skipped_count += 1
                continue

            # Create the fellowship (directed edge)
            fellowship = FellowshipModel(
                id=uuid7(),
                user_id=follower,
                followed_user_id=followed,
                started_at=timezone.now(),
                is_soft_deleted=False
            )
            fellowship_batch.append(fellowship)
            existing_edges.add((follower, followed))  # mark as used

            # Batch insert
            if len(fellowship_batch) >= batch_size:
                try:
                    with transaction.atomic():
                        FellowshipModel.objects.bulk_create(
                            fellowship_batch,
                            batch_size=batch_size,
                            ignore_conflicts=False
                        )
                        created_count += len(fellowship_batch)
                        if verbose:
                            self.stdout.write(f"  Created batch of {len(fellowship_batch)} fellowships")
                        else:
                            if created_count % 100 == 0:
                                self.stdout.write(f"  Progress: {created_count}/{count} fellowships created")
                except IntegrityError as e:
                    self.stdout.write(self.style.WARNING(
                        f"  Integrity error in batch: {e}. Falling back to individual creation."
                    ))
                    # Fallback: create each fellowship individually
                    for f in fellowship_batch:
                        try:
                            with transaction.atomic():
                                f.save()
                                created_count += 1
                        except IntegrityError:
                            if verbose:
                                self.stdout.write(f"  Skipping duplicate: {f.user_id} follows {f.followed_user_id}")
                            skipped_count += 1
                finally:
                    fellowship_batch = []

        # Insert remaining fellowships
        if fellowship_batch:
            try:
                with transaction.atomic():
                    FellowshipModel.objects.bulk_create(
                        fellowship_batch,
                        batch_size=batch_size,
                        ignore_conflicts=False
                    )
                    created_count += len(fellowship_batch)
            except IntegrityError:
                # Fallback for leftover batch
                for f in fellowship_batch:
                    try:
                        with transaction.atomic():
                            f.save()
                            created_count += 1
                    except IntegrityError:
                        if verbose:
                            self.stdout.write(f"  Skipping duplicate: {f.user_id} follows {f.followed_user_id}")
                        skipped_count += 1

        elapsed_time = time.time() - start_time

        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS(
            f"✅ Successfully created {created_count} fellowships in {elapsed_time:.2f} seconds"
        ))
        if skipped_count > 0:
            self.stdout.write(self.style.WARNING(f"⚠️ Skipped {skipped_count} attempts"))

        if attempt_count >= max_attempts and created_count < count:
            self.stdout.write(self.style.WARNING(
                f"⚠️ Reached max attempts ({max_attempts}) before creating all {count} fellowships."
            ))

        # Statistics
        total = FellowshipModel.objects.filter(is_soft_deleted=False).count()
        self.stdout.write(f"📊 Total active fellowships now: {total}")

        # Optional: show user with most followers/following
        from django.db.models import Count
        top_followed = UserModel.objects.filter(
            followers__is_soft_deleted=False
        ).annotate(
            follower_count=Count('followers')
        ).order_by('-follower_count').first()
        if top_followed:
            self.stdout.write(
                f"👑 Most followed: {top_followed.user_name} "
                f"(followed by {top_followed.follower_count} users)"
            )