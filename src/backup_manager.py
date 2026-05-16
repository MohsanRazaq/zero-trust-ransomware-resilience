import os
import shutil
from datetime import datetime

from constants import BACKUP_DIR, MAX_BACKUP_VERSIONS
from logger import write_log


def _prune_old_versions(filename: str) -> None:
    """
    Keep only the MAX_BACKUP_VERSIONS most recent backups for a given base filename.
    Deletes the oldest ones when the limit is exceeded.
    """
    prefix = filename + "_"
    existing = sorted(
        f for f in os.listdir(BACKUP_DIR) if f.startswith(prefix)
    )

    while len(existing) >= MAX_BACKUP_VERSIONS:
        oldest = os.path.join(BACKUP_DIR, existing.pop(0))
        try:
            os.chmod(oldest, 0o644)   # make writable before deleting
            os.remove(oldest)
            write_log(f"[BACKUP] Pruned old version: {oldest}")
        except Exception as e:
            write_log(f"[ERROR] Could not prune backup {oldest}: {e}")
            break


def backup_files(file_path: str) -> None:
    if not os.path.isfile(file_path):
        return

    filename = os.path.basename(file_path)
    os.makedirs(BACKUP_DIR, exist_ok=True)

    _prune_old_versions(filename)

    # Use microseconds so two rapid saves never produce the same backup filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    backup_path = os.path.join(BACKUP_DIR, f"{filename}_{timestamp}")

    # If a file with this exact name already exists and is read-only (from a
    # previous run), make it writable first so shutil.copy2 can overwrite it.
    if os.path.exists(backup_path):
        os.chmod(backup_path, 0o644)

    shutil.copy2(file_path, backup_path)

    # Lock the backup read-only AFTER the copy succeeds
    os.chmod(backup_path, 0o444)

    write_log(f"[BACKUP] {file_path} -> {backup_path}")