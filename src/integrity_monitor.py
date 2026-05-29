import hashlib
from pathlib import Path
from watchdog.events import FileSystemEventHandler

from logger import write_log


# Stores last known hash state of monitored files
tracked_hashes = {}
THREAT_SCORE=0

def get_hash(filepath):
    """
    Generate SHA-256 hash of file contents.

    Returns:
        str | None
    """
    try:
        with open(filepath, "rb") as f:
            return hashlib.file_digest(f, "sha256").hexdigest()

    except (FileNotFoundError, PermissionError):
        return None

def get_score(score:int)->int:
    return score
class IntegrityHandler(FileSystemEventHandler):

    def process_hash_change(self, src: str, event_type: str) -> None:
        """
        Compare previous known file hash against current hash state.
        """

        new_hash = get_hash(src)

        if new_hash is None:
            return

        old_hash = tracked_hashes.get(src)

        # Detect actual content modification
        if new_hash != old_hash:

            get_score(20)
            write_log(
                f'[{event_type}] {src}\n'
                f'Old Hash: {old_hash}\n'
                f'New Hash: {new_hash}'
            )

            # Update known file state
            tracked_hashes[src] = new_hash

        else:
            write_log(f'[INFO] File touched without content modification: {src}')
            print(f'[INFO] File touched without content modification: {src}')

    def on_created(self, event):

        if event.is_directory:
            return

        src = str(event.src_path)

        self.process_hash_change(src, "CREATED")

    def on_modified(self, event):

        if event.is_directory:
            return

        src = str(event.src_path)

        self.process_hash_change(src, "MODIFIED")

    def on_deleted(self, event):

        if event.is_directory:
            return

        src = str(event.src_path)

        write_log(f'[DELETED] {src}')
        print(f'[DELETED] {src}')

        get_score(20)
        # Remove deleted file from tracked state
        tracked_hashes.pop(src, None)

    def on_moved(self, event):

        if event.is_directory:
            return

        src = str(event.src_path)
        dest = str(event.dest_path)

        # Get previous known state BEFORE migration
        old_hash = tracked_hashes.get(src)

        # Get current hash from new location
        new_hash = get_hash(dest)

        get_score(20)
        write_log(
            f'[MOVED] {src} -> {dest}\n'
            f'Old Hash: {old_hash}\n'
            f'New Hash: {new_hash}'
        )

        print(
            f'[MOVED] {src} -> {dest}\n'
            f'Old Hash: {old_hash}\n'
            f'New Hash: {new_hash}'
        )

        # Remove old identity
        tracked_hashes.pop(src, None)

        # Register new identity
        if new_hash:
            tracked_hashes[dest] = new_hash