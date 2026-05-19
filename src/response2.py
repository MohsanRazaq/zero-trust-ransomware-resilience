import os

from constants import SUSPICIOUS_EXTENSIONS
from logger import write_log


def lock_access(folderpath: str) -> None:
    # Validate that the protected target exists and is a real directory
    # before applying recursive containment operations.
    if not os.path.isdir(folderpath):
        write_log(f'[ISSUE] Folder: {folderpath} is missing. Returning back')
        return

    # Begin ransomware containment workflow by locking filesystem permissions.
    write_log(f'[ALERT] Securing Folder: {folderpath}')

    try:
        # Walk the directory tree bottom-up so child files/directories
        # are secured before parent directories become restricted.
        for root, dirs, files in os.walk(folderpath, topdown=False):

            write_log(f'[ALERT] Traversing Folder: {root}')

            # Convert healthy files into read-only mode
            # while preserving suspicious files as forensic evidence.
            for filename in files:
                filepath = os.path.join(root, filename)

                # Skip files already showing ransomware-style extensions.
                if any(filepath.lower().endswith(ext)
                       for ext in SUSPICIOUS_EXTENSIONS):
                    continue

                # Ensure the current object is a valid file
                # before modifying filesystem permissions.
                if os.path.isfile(filepath):
                    os.chmod(filepath, 0o444)

            # Lock nested directories recursively to prevent
            # further file creation or modification attempts.
            for dirname in dirs:
                dir_to_lock = os.path.join(root, dirname)
                os.chmod(dir_to_lock, 0o555)

        # Finally secure the root protected directory itself.
        os.chmod(folderpath, 0o555)

        write_log(f'[SUCCESS] Folder {folderpath} is now protected')

    except OSError as e:
        write_log(f'[WARNING] LOCKING FOLDER FAILED: {e}')
        print(f'LOCKING FOLDER ACCESS FAILED: {e}')


def unlock_access(folderpath: str) -> None:
    # Validate recovery target before attempting restoration.
    if not os.path.isdir(folderpath):
        write_log(f'[ISSUE] Folder: {folderpath} is missing. Cannot restore access')
        return

    write_log(f'[ALERT] Restoring Folder Access: {folderpath}')

    try:
        # Traverse directories recursively and restore
        # normal filesystem permissions required for recovery.
        for root, dirs, files in os.walk(folderpath):

            write_log(f'[ALERT] Traversing Folder: {root}')

            # Ensure current traversal node remains accessible
            # so deeper recursive traversal can continue safely.
            os.chmod(root, 0o755)

            # Restore normal directory permissions recursively.
            for dirname in dirs:
                dir_to_unlock = os.path.join(root, dirname)
                os.chmod(dir_to_unlock, 0o755)

            # Restore standard writable permissions to recovered files.
            for filename in files:
                filepath = os.path.join(root, filename)

                if os.path.isfile(filepath):
                    os.chmod(filepath, 0o644)

        write_log(f'[SUCCESS] Folder {folderpath} is now accessible')

    except OSError as e:
        write_log(f'[WARNING] UNLOCKING FOLDER FAILED: {e}')
        print(f'UNLOCKING FOLDER ACCESS FAILED: {e}')