# core/secrets.py
from pathlib import Path
from typing import List
# Module simple has utils for reading secrets
# Secrets are read in settings.py
def read_secret(path: str) -> str:
    return Path(path).read_text().strip()
