"""
Django management command to create random friendships between users.

This script models friendships as a graph where:
- Users are nodes (vertices)
- Friendships are edges (connections)

Graph Theory Concepts:
---------------------
When modeling friendships, we treat the user base as a graph G = (V, E) where:
- V = set of all users (nodes)
- E = set of friendships (edges)

In this implementation, friendships are symmetric (mutual). When User A is friends 
with User B, we create TWO directed edges:
    Edge 1: A → B
    Edge 2: B → A

This creates a complete directed graph representation of an undirected friendship.

Triangular Numbers:
------------------
The triangular number sequence (Tₙ) represents the number of edges in a complete 
graph (Kₙ) where every node connects to every other node exactly once.

Formula: Tₙ = n x (n-1) / 2

Triangular number sequence examples:
    n=2: T₂ = 2x1/2 = 1 friendship
    n=3: T₃ = 3x2/2 = 3 friendships
    n=4: T₄ = 4x3/2 = 6 friendships
    n=5: T₅ = 5x4/2 = 10 friendships

Why triangular numbers matter for friendships:
    - If you have 5 users, you can have at most 10 unique friendship pairs
    - Each unique pair is stored as 2 directed records in the database
    - This creates a complete undirected graph (K₅) with 10 edges

Maximum Possible Friendships Calculation:
----------------------------------------
For an undirected friendship graph, the maximum number of unique friendships is:
    max_undirected = n x (n-1) / 2

For example, with 100 users:
    max_undirected = 100 x 99 / 2 = 4,950 possible friendships

This formula counts each friendship pair only once, regardless of whether it's
stored as one record (undirected) or two records (directed) in the database.

Note on Directed vs Undirected:
    - Undirected friendships (conceptual): count = n x (n-1) / 2
    - Directed records (database storage): count = n x (n-1)
    - Our maximum is based on UNDIRECTED friendships because each friendship
      is a unique relationship between two users, not a directional connection

The script uses the triangular number formula to determine the absolute maximum
number of friendships possible given the current user count.

Usage Examples:
--------------
# Create 100 friendships with default settings
python manage.py create_random_friendships --count 100

# Create 50 friendships with verbose output
python manage.py create_random_friendships --count 50 --verbose

# Try to create 500 friendships with more attempts
python manage.py create_random_friendships --count 500 --max-attempts 5000

# Create friendships with progress indicator (default)
python manage.py create_random_friendships --count 200
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import IntegrityError
import random
from uuid import uuid7

from apps.users.infrastructure.models.user_model import UserModel
from apps.users.infrastructure.models.friendship_model import FriendshipModel


class Command(BaseCommand):
    """
    Creates random symmetric friendships between existing users.
    
    This command implements a graph-based approach to friendship creation:
    - Users are treated as nodes in a graph
    - Friendships are edges that connect nodes
    - Each friendship is bidirectional (mutual)
    - The script avoids duplicate friendships by tracking existing connections
    """
    
    help = "Creates random symmetric friendships between existing users."

    def add_arguments(self, parser):
        """
        Add command-line arguments for configuring friendship creation.
        
        Arguments:
            --count: Number of friendships to create (default: 50)
            --max-attempts: Maximum random selection attempts before giving up
            --verbose: Display detailed information about each operation
        """
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Number of friendships to create (default: 50)'
        )
        parser.add_argument(
            '--max-attempts',
            type=int,
            default=1000,
            help='Maximum attempts to find unique user pairs (default: 1000)'
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed output including skipped friendships'
        )

    def calculate_max_friendships(self, user_count):
        """
        Calculate the maximum number of possible friendships using triangular numbers.
        
        This implements the triangular number formula: n x (n-1) / 2
        
        Graph theory context:
            - For a graph with n nodes (users)
            - A complete graph (Kₙ) has exactly n x (n-1) / 2 edges
            - Each edge represents a unique friendship pair
            
        Mathematical derivation:
            - Each user can be friends with (n-1) other users
            - Summing over all users: n x (n-1)
            - But this counts each friendship twice (once from each endpoint)
            - Therefore divide by 2: n x (n-1) / 2
            
        Example:
            With 100 users: 100 x 99 / 2 = 4,950 possible friendships
            
        Returns:
            int: Maximum number of unique friendships possible
        """
        return user_count * (user_count - 1) // 2

    def handle(self, *args, **options):
        """
        Main command handler that orchestrates the friendship creation process.
        
        Process:
            1. Validate user count (need at least 2 users)
            2. Calculate maximum possible friendships using triangular numbers
            3. Load existing friendships to avoid duplicates
            4. Randomly select user pairs until target count is reached
            5. Create bidirectional friendship records for each unique pair
            6. Display statistics about the created friendships
        """
        count = options['count']
        max_attempts = options['max_attempts']
        verbose = options['verbose']
        
        # Step 1: Fetch all active users (nodes in the friendship graph)
        users = list(UserModel.objects.filter(is_soft_deleted=False))
        user_ids = [user.id for user in users]
        user_count = len(user_ids)
        
        self.stdout.write(f"Found {user_count} active users")
        
        # Step 2: Validate we have enough nodes to create edges
        if user_count < 2:
            self.stdout.write(self.style.ERROR(
                f"❌ Need at least 2 users to create friendships. Found {user_count} users."
            ))
            return
        
        # Step 3: Calculate maximum possible friendships using triangular number formula
        # This represents the maximum number of edges possible in the friendship graph
        max_possible = self.calculate_max_friendships(user_count)
        self.stdout.write(f"Maximum possible friendships (complete graph K_{user_count}): {max_possible}")
        
        # Step 4: Adjust requested count if it exceeds theoretical maximum
        if count > max_possible:
            self.stdout.write(self.style.WARNING(
                f"⚠️ Requested {count} friendships but only {max_possible} possible. "
                f"Will create as many as possible."
            ))
            count = max_possible
        
        created_count = 0
        skipped_count = 0
        attempt_count = 0
        
        # Step 5: Track existing friendships (edges) to prevent duplicates
        existing_pairs = set()
        
        # Load existing edges from the database
        existing_friendships = FriendshipModel.objects.filter(
            is_soft_deleted=False
        ).values_list('user_id', 'friend_id')
        
        for user_id, friend_id in existing_friendships:
            existing_pairs.add((user_id, friend_id))
        
        self.stdout.write(f"Found {len(existing_pairs)} existing active friendships")
        
        # Step 6: Main loop - create random friendships until target is reached
        # We use a graph-based approach: randomly select nodes and connect them with edges
        while created_count < count and attempt_count < max_attempts:
            attempt_count += 1
            
            # Randomly select two distinct nodes (users) from the graph
            if len(user_ids) < 2:
                break
                
            user_a, user_b = random.sample(user_ids, 2)
            
            # Check if an edge already exists between these nodes (in either direction)
            pair_key = (user_a, user_b)
            reverse_key = (user_b, user_a)
            
            if pair_key in existing_pairs or reverse_key in existing_pairs:
                if verbose:
                    self.stdout.write(f"  Skipping: Edge already exists between {user_a} and {user_b}")
                skipped_count += 1
                continue
            
            # Step 7: Create bidirectional friendship edges
            # Since friendships are symmetric (undirected), we create two directed edges
            # This maintains the property that if A is friends with B, then B is friends with A
            try:
                friendship1 = FriendshipModel(
                    id=uuid7(),
                    user_id=user_a,
                    friend_id=user_b,
                    started_at=timezone.now(),
                    is_soft_deleted=False
                )
                friendship2 = FriendshipModel(
                    id=uuid7(),
                    user_id=user_b,
                    friend_id=user_a,
                    started_at=timezone.now(),
                    is_soft_deleted=False
                )
                
                # Add both edges to the graph
                friendship1.save()
                friendship2.save()
                
                # Update our edge tracking set
                existing_pairs.add(pair_key)
                existing_pairs.add(reverse_key)
                
                created_count += 1
                
                if verbose:
                    self.stdout.write(f"  ✅ Created edge {created_count}/{count}: {user_a} <-> {user_b}")
                else:
                    # Progress indicator every 10 edges
                    if created_count % 10 == 0:
                        self.stdout.write(f"  Progress: {created_count}/{count} edges created")
                        
            except IntegrityError as e:
                self.stdout.write(self.style.WARNING(
                    f"  Integrity error for edge {user_a} <-> {user_b}: {e}"
                ))
                skipped_count += 1
                continue
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"  Unexpected error for edge {user_a} <-> {user_b}: {e}"
                ))
                skipped_count += 1
                continue
        
        # Step 8: Display final graph statistics
        self.stdout.write("\n" + "="*50)
        self.stdout.write(self.style.SUCCESS(f"✅ Successfully created {created_count} friendships"))
        
        if skipped_count > 0:
            self.stdout.write(self.style.WARNING(f"⚠️ Skipped {skipped_count} attempts"))
        
        if attempt_count >= max_attempts and created_count < count:
            self.stdout.write(self.style.WARNING(
                f"⚠️ Reached maximum attempts ({max_attempts}) without creating all {count} friendships. "
                f"Consider reducing --count or adding more users."
            ))
        
        # Display graph statistics
        total_friendships = FriendshipModel.objects.filter(is_soft_deleted=False).count()
        self.stdout.write(f"📊 Total active edges in friendship graph: {total_friendships}")
        
        # Show node with highest degree (most connections)
        from django.db.models import Count
        top_user = UserModel.objects.filter(
            friendships__is_soft_deleted=False
        ).annotate(
            friend_count=Count('friendships')
        ).order_by('-friend_count').first()
        
        if top_user:
            self.stdout.write(
                f"👥 Node with highest degree: {top_user.user_name} "
                f"(connected to {top_user.friend_count} other nodes)"
            )