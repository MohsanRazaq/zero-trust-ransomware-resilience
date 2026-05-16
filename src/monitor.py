import time
from watchdog.events import FileSystemEventHandler

from logger import write_log
from detector import (
    recent_modifications,
    detect_suspicious_activity,
    detect_suspicious_extension
)
from backup_manager import backup_files
from recovery import is_restoring


class MonitorHandler(FileSystemEventHandler):


    def on_modified(self, event):

        if is_restoring:
            return

        if event.is_directory:
            return

        src_path = str(event.src_path)

        if (
            "backup" in src_path
            or "logs" in src_path
            or "_2026-" in src_path
        ):
            return

        time.sleep(0.1)

        recent_modifications.append(time.time())

        backup_files(event.src_path)

        write_log(f"[MODIFIED] {event.src_path}")

        detect_suspicious_activity('protected')


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

        write_log(
            f"[MOVED] {event.src_path} to {event.dest_path}"
        )

        detect_suspicious_extension(event.dest_path)