"""Deletes the shopwise database file."""

import shutil
from pathlib import Path

parent = Path(__file__).parent 

db_path = parent/"shopwise.db"

if db_path.exists():
    print(f"Deleting the database file: {db_path}")
    db_path.unlink()


