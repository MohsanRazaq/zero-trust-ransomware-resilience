import os

from constants import SUSPICIOUS_EXTENSIONS
from logger import write_log


def lock_access(folder_path: str) -> None:
    """
    Converts protected files into read-only mode
    to contain suspected ransomware activity.
    """
    write_log(f"[LOCKDOWN] Securing {folder_path}")

    try:
        os.chmod(folder_path, 0o555)

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            if os.path.isfile(file_path):
                # Leave already-encrypted files untouched (don't hide evidence)
                if any(file_path.endswith(ext) for ext in SUSPICIOUS_EXTENSIONS):
                    continue
                os.chmod(file_path, 0o444)

        write_log(f"[SUCCESS] {folder_path} is now protected")

    except PermissionError:
        write_log(f"[ERROR] lock_access failed")


def unlock_access(folder_path: str) -> None:
    write_log(f"[RECOVERY] Unlocking {folder_path}")

    try:
        os.chmod(folder_path, 0o755)

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            if os.path.isfile(file_path):
                os.chmod(file_path, 0o644)

        write_log(f"[SUCCESS] {folder_path} unlocked")

    except Exception as e:
        write_log(f"[ERROR] unlock_access failed: {e}")
