"""Deletes the shopwise database file."""

import shutil
import os

try:
    os.remove("shopwise.db")
except Exception as e:
    pass

try:
    os.remove("../shopwise.db")
except Exception as e:
    pass

print("Database deleted")
