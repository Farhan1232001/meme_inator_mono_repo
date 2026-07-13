# management/commands/sync_policies.py
from django.core.management.base import BaseCommand
from pathlib import Path

from apps.moderation_sys.infrastructure.repositories.django_policy_definition_repository import DjangoPolicyDefinitionRepository
from apps.moderation_sys.infrastructure.services.yaml_policy_loader import YamlPolicyLoader

# python manage.py sync_policies
class Command(BaseCommand):
    """
    Syncs policies directories filled with PolicyDefinitions in Yaml files, with policies in database. 
    """
    def handle(self, *args, **options):
        repo = DjangoPolicyDefinitionRepository()
        loader = YamlPolicyLoader(repo)
        count = loader.sync_directory(Path("/Users/far/Desktop/thoughts/0_THOUGHTS/KnowledgeApplied/CodingPlayground/Meme-inator/meme_inator_mono_repo/meme_inator_back/apps/moderation_sys/policies"))
        self.stdout.write(f"Synced {count} policies")
