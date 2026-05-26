import time

from watchdog.events import FileSystemEventHandler

import detector
from backup_manager import backup_files
from constants import BACKUP_DIR, LOG_DIR
from logger import write_log
from recovery import is_restoring
from detector import check_entropy_threashold

class MonitorHandler(FileSystemEventHandler):

    def on_modified(self, event):
        # Read is_locked via the module, not a stale imported copy
        if detector.is_locked or is_restoring:
            return

        if event.is_directory:
            return

        src_path = str(event.src_path)

        if any(d in src_path for d in (BACKUP_DIR, LOG_DIR, "_2026-")):
            return

        time.sleep(0.1)

        # Re-check after sleep — lockdown may have fired on another thread
        if detector.is_locked:
            return

        with detector._lock:
            detector.recent_modifications.append(time.time())
        score=check_entropy_threashold(src_path)
    

        backup_files(src_path)
        write_log(f"[MODIFIED] {src_path} (Entropy: {score:.2f})")
        detector.detect_suspicious_activity("protected", score)

    def on_created(self, event):
        if event.is_directory:
            return
        write_log(f"[CREATED] {event.src_path}")

    def on_deleted(self, event):
        if event.is_directory:
            return
        write_log(f"[DELETED] {event.src_path}")

    def on_moved(self, event):
        if event.is_directory:
            return
        write_log(f"[MOVED] {event.src_path} -> {event.dest_path}")
        detector.detect_suspicious_extension(event.dest_path)