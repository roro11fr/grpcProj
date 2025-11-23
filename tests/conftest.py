# tests/conftest.py
import os
import sys
from pathlib import Path

import pytest

# Rădăcina proiectului = folderul care conține `services/` și `gateway/`
REPO_ROOT = Path(__file__).resolve().parents[1]

# Candidati de adăugat în sys.path: (1) root curent, (2) root/grpcProj (dacă există)
candidates = [REPO_ROOT, REPO_ROOT / "grpcProj"]

for p in candidates:
    if (p / "services").exists() and str(p) not in sys.path:
        sys.path.insert(0, str(p))
        break

# Respectă și PYTHONPATH, dacă e setat
env_pp = os.environ.get("PYTHONPATH", "")
if env_pp and env_pp not in sys.path:
    sys.path.append(env_pp)


@pytest.fixture(scope="session")
def event_loop():
    import asyncio

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
