import os
import shutil

from constants import BACKUP_DIR, PROTECTED_DIR
from logger import write_log

is_restoring = False


def restore_backup() -> None:
    global is_restoring

    is_restoring = True
    write_log("[RECOVERY] Starting backup restoration process")

    try:
        os.makedirs(PROTECTED_DIR, exist_ok=True)

        for raw_filename in os.listdir(BACKUP_DIR):
            # --- PATH TRAVERSAL FIX ---
            # Always use basename so a malicious filename like
            # "../../etc/passwd" can never escape the target directory.
            safe_name = os.path.basename(raw_filename)

            backup_file_path = os.path.join(BACKUP_DIR, safe_name)
            dest_path = os.path.join(PROTECTED_DIR, safe_name)

            # Extra guard: confirm the resolved path stays inside PROTECTED_DIR
            resolved_dest = os.path.realpath(dest_path)
            resolved_root = os.path.realpath(PROTECTED_DIR)
            if not resolved_dest.startswith(resolved_root + os.sep):
                write_log(f"[ERROR] Skipping unsafe path: {raw_filename}")
                continue

            if not os.path.isfile(backup_file_path):
                continue

            # Backup files are 0o444; make them writable before copying
            try:
                os.chmod(backup_file_path, 0o644)
            except Exception:
                pass

            shutil.copy2(backup_file_path, dest_path)
            write_log(f"[RESTORED] {safe_name}")

        write_log("[SUCCESS] Backup restoration completed")

    except Exception as e:
        write_log(f"[ERROR] Recovery failed: {e}")

    finally:
        is_restoring = False
