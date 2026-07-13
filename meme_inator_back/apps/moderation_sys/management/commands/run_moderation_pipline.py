import json
from uuid import uuid7
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from apps.moderation_sys.application.orchestration.moderation_orchestration import ModerationOrchestration
from apps.moderation_sys.application.schemas.moderation_submission_request import ModerationSubmissionRequestSchema
from core.dependency_injections import di
from core.results import Ok, NotOk, Error


class Command(BaseCommand):
    help = """
    Run moderation pipeline on a JSON file of submissions.
    
    JSON file should contain an array of objects matching the ModerationSubmissionRequestSchema.
    Example:
    [
      {
        "content_id": "00000000-0000-0000-0000-000000000001",
        "author_id": "00000000-0000-0000-0000-000000000002",
        "policy_routing_key": "mod_sys:default:text",
        "content_type": "comment",
        "content_source": "request_body",
        "region": "us-west",
        "text_content": { "text": "Hello world" }
      }
    ]
    """
    
    DEFAULT_FILE_PATH = Path(
        "/Users/far/Desktop/thoughts/0_THOUGHTS/KnowledgeApplied/CodingPlayground/Meme-inator/"
        "meme_inator_mono_repo/meme_inator_back/apps/moderation_sys/management/"
        "content_to_moderate_test_submissions.json"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "file",
            nargs="?",
            type=str,
            help="Path to JSON file containing submissions (overrides hardcoded default)"
        )

    def handle(self, *args, **options):
        # Determine file path
        if options.get("file"):
            file_path = Path(options["file"])
        else:
            file_path = self.DEFAULT_FILE_PATH
            self.stdout.write(self.style.NOTICE(f"No file provided, using hardcoded default: {file_path}"))

        if not file_path.exists():
            raise CommandError(f"File not found: {file_path}")

        with open(file_path) as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise CommandError("JSON root must be an array of submissions")

        orchestrator: ModerationOrchestration = di.create_moderation_orchestration()

        results = []
        for idx, item in enumerate(data, 1):
            self.stdout.write(f"\n[{idx}/{len(data)}] Processing submission...")

            # Generate missing UUIDs
            if "content_id" not in item or item["content_id"] is None:
                item["content_id"] = str(uuid7())
            if "author_id" not in item or item["author_id"] is None:
                item["author_id"] = str(uuid7())

            try:
                # 1. Create validated schema
                submission = ModerationSubmissionRequestSchema(**item)

                # 2. Submit moderation case
                case_result = orchestrator.submit_moderation_case(submission)

                # ----- Proper Result handling -----
                if case_result.is_error():
                    self.stdout.write(self.style.ERROR(f"  ❌ Submit failed (Error): {case_result}"))
                    results.append({"submission": item, "success": False, "error": str(case_result)})
                    continue

                if case_result.is_not_ok():
                    self.stdout.write(self.style.ERROR(f"  ❌ Submit failed (NotOk): {case_result.message}"))
                    results.append({"submission": item, "success": False, "error": case_result.message})
                    continue

                # case_result is Ok[...]
                case = case_result.value
                self.stdout.write(self.style.SUCCESS(f"  ✅ Submitted case: {case.case_id}"))

                # 3. Process content (run moderation provider)
                process_result = orchestrator.process_content(case.case_id, case)

                if process_result.is_error():
                    self.stdout.write(self.style.ERROR(f"  ❌ Processing failed (Error): {process_result}"))
                    results.append({
                        "submission": item,
                        "case_id": str(case.case_id),
                        "success": False,
                        "error": str(process_result)
                    })
                    continue

                if process_result.is_not_ok():
                    self.stdout.write(self.style.ERROR(f"  ❌ Processing failed (NotOk): {process_result.message}"))
                    results.append({
                        "submission": item,
                        "case_id": str(case.case_id),
                        "success": False,
                        "error": process_result.message
                    })
                    continue

                self.stdout.write(self.style.SUCCESS(f"  ✅ Processed case: {case.case_id}"))

                # Success – record outcome
                decision_outcome = None
                confidence = None
                if hasattr(case, 'decision') and case.decision:
                    # case is a domain aggregate (ModerationCase) -> has decision.outcome.value
                    decision_outcome = case.decision.outcome.value
                    confidence = case.confidence_score.value if case.confidence_score else None
                elif hasattr(case, 'decision') and case.decision and hasattr(case.decision, 'outcome'):
                    # case might be a Django model – outcome is a string field
                    decision_outcome = case.decision.outcome
                    confidence = getattr(case, 'confidence_score', None)

                results.append({
                    "submission": item,
                    "case_id": str(case.case_id),
                    "success": True,
                    "decision": decision_outcome,
                    "confidence": confidence,
                })

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ❌ Exception: {e}"))
                results.append({"submission": item, "success": False, "error": str(e)})

        # Summary
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("SUMMARY"))
        self.stdout.write("=" * 60)
        successful = sum(1 for r in results if r["success"])
        self.stdout.write(f"Total: {len(results)}")
        self.stdout.write(f"Successful: {successful}")
        self.stdout.write(f"Failed: {len(results) - successful}")