# moderation_sys/management/commands/process_pending_moderation.py

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from typing import Optional
from uuid import UUID
import logging

from apps.moderation_sys.application.orchestration.moderation_orchestration import ModerationOrchestration
from apps.moderation_sys.domain.enums.moderation_enums import CaseStatusEnum
from core.dependency_injections import di
from core.results import Result

logger = logging.getLogger(__name__)

# TODO: LLM GENERATED!!! Check Code

class Command(BaseCommand):
    help = """
    Process pending moderation cases (downstream batch pipeline).
    
    This internal tool materializes pending moderation decisions by:
    1. Fetching cases in PENDING or FLAGGED status
    2. Running them through the moderation pipeline
    3. Updating their status based on provider results
    
    Aligns with data engineering batch processing patterns.
    """
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--case-id',
            type=str,
            help='Process a specific case by UUID (for debugging)'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=100,
            help='Number of cases to process in batch (default: 100)'
        )
        parser.add_argument(
            '--status',
            type=str,
            default='PENDING',
            choices=['PENDING', 'FLAGGED', 'ALL'],
            help='Filter cases by status (default: PENDING)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview what would be processed without executing'
        )
        parser.add_argument(
            '--provider',
            type=str,
            default=None,
            help='Force a specific moderation provider (for testing)'
        )
        parser.add_argument(
            '--max-failures',
            type=int,
            default=5,
            help='Stop batch processing after N failures (default: 5)'
        )
    
    def handle(self, *args, **options):
        """Execute the downstream batch processing pipeline."""
        
        # Initialize orchestrator (same as API uses)
        orchestrator: ModerationOrchestration = di.create_moderation_orchestration()
        
        # Single case mode (for debugging/fixes)
        if options['case_id']:
            self._process_single_case(orchestrator, options['case_id'])
            return
        
        # Batch processing mode
        self._process_batch_pipeline(orchestrator, options)
    
    def _process_single_case(self, orchestrator: ModerationOrchestration, case_id_str: str):
        """Process a single case for debugging or manual intervention."""
        try:
            case_id = UUID(case_id_str)
        except ValueError:
            raise CommandError(f"Invalid UUID format: {case_id_str}")
        
        self.stdout.write(f"Processing single case: {case_id}")
        
        result = orchestrator.process_content(case_id)
        
        if result.is_error:
            raise CommandError(f"Processing failed: {result.error}")
        
        self.stdout.write(
            self.style.SUCCESS(f"Successfully processed case {case_id}")
        )
    
    def _process_batch_pipeline(self, orchestrator: ModerationOrchestration, options: dict):
        """Execute batch processing pipeline for pending cases."""
        
        batch_size = options['batch_size']
        status_filter = options['status']
        dry_run = options['dry_run']
        max_failures = options['max_failures']
        
        self.stdout.write(
            self.style.NOTICE(
                f"🚀 Starting downstream batch pipeline:\n"
                f"   - Status filter: {status_filter}\n"
                f"   - Batch size: {batch_size}\n"
                f"   - Dry run: {dry_run}\n"
                f"   - Max failures: {max_failures}"
            )
        )
        
        # Fetch pending cases (you'll need to implement this in orchestrator)
        pending_cases = orchestrator.get_pending_cases(
            batch_size=batch_size,
            status=status_filter
        )
        
        if not pending_cases:
            self.stdout.write(self.style.SUCCESS("✅ No pending cases to process"))
            return
        
        self.stdout.write(f"📋 Found {len(pending_cases)} cases to process")
        
        if dry_run:
            self._display_dry_run_preview(pending_cases)
            return
        
        # Execute batch pipeline
        results = self._execute_batch_pipeline(
            orchestrator, 
            pending_cases, 
            max_failures
        )
        
        # Display summary
        self._display_batch_summary(results)
    
    def _display_dry_run_preview(self, cases):
        """Show what would be processed without actually doing it."""
        self.stdout.write("\n📋 DRY RUN - Would process:")
        for case in cases[:20]:  # Show first 20
            self.stdout.write(
                f"  - {case.case_id} | {case.content_type} | "
                f"Status: {case.status} | Created: {case.created_at.date()}"
            )
        
        if len(cases) > 20:
            self.stdout.write(f"  ... and {len(cases) - 20} more cases")
    
    def _execute_batch_pipeline(self, orchestrator, cases, max_failures):
        """Execute the actual batch processing pipeline."""
        
        results = {
            'success': [],
            'failed': [],
            'skipped': [],
            'failure_count': 0
        }
        
        for idx, case in enumerate(cases, 1):
            self.stdout.write(
                f"Processing [{idx}/{len(cases)}]: {case.case_id}...",
                ending=''
            )
            
            # Check circuit breaker
            if results['failure_count'] >= max_failures:
                self.stdout.write(
                    self.style.WARNING(
                        f"\n⚠️  Stopping batch: Max failures ({max_failures}) reached"
                    )
                )
                break
            
            # Process the case
            result = orchestrator.process_content(case.case_id)
            
            if result.is_error:
                results['failed'].append({
                    'case_id': case.case_id,
                    'error': str(result.error)
                })
                results['failure_count'] += 1
                self.stdout.write(self.style.ERROR(f" ❌ Failed"))
                logger.error(f"Failed to process {case.case_id}: {result.error}")
            else:
                results['success'].append(case.case_id)
                self.stdout.write(self.style.SUCCESS(f" ✅ Success"))
        
        return results
    
    def _display_batch_summary(self, results):
        """Display batch processing summary."""
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("📊 BATCH PIPELINE SUMMARY"))
        self.stdout.write("=" * 60)
        self.stdout.write(f"✅ Successful: {len(results['success'])}")
        self.stdout.write(f"❌ Failed: {len(results['failed'])}")
        
        if results['failed']:
            self.stdout.write("\n⚠️  Failed cases:")
            for failed in results['failed'][:10]:
                self.stdout.write(f"  - {failed['case_id']}: {failed['error'][:100]}")
            if len(results['failed']) > 10:
                self.stdout.write(f"  ... and {len(results['failed']) - 10} more")
        
        self.stdout.write("=" * 60)