import time
from watchdog.events import FileSystemEventHandler

import detector
from reporter import generate_threat_report
from backup_manager import backup_files
from constants import BACKUP_DIR, LOG_DIR
from logger import write_log
from recovery import is_restoring
from detector import check_entropy_threashold
class MonitorHandler(FileSystemEventHandler):

    def on_modified(self, event):
        # 1. Swift Safety Exit Conditions
        if detector.is_locked or is_restoring:
            return

        if event.is_directory:
            return

        src_path = str(event.src_path)

        # Exclude administrative data log paths
        if any(d in src_path for d in (BACKUP_DIR, LOG_DIR, "_2026-")):
            return

        time.sleep(0.1)

        try:
            with detector._lock:
                detector.recent_modifications.append(time.time())
            
            score = check_entropy_threashold(src_path)
            backup_files(src_path)
            write_log(f"[MODIFIED] {src_path} (Entropy: {score:.2f})")
            
            # Fetch features for ML model query
            velocity = len(detector.recent_modifications)
            
            # =========================================================================
            from ml_detector import predict_malicious_intent
            
            is_attack_detected = predict_malicious_intent(velocity, score)
            
            if is_attack_detected:
                write_log(f"[CRITICAL] ML Engine classified activity behavior as MALICIOUS!")
                detector.is_locked = True
                detector.THREAT_SCORE = 100
                
                from response import lock_access
                lock_access("protected")
                
                generate_threat_report(
                    "Machine Learning Random Forest Detection",
                    src_path,
                    "Automated Zero-Trust Isolation Lock",
                    score,
                    velocity,
                    detector.THREAT_SCORE
                )
                return  # Drop execution instantly to protect remaining assets
            # =========================================================================
            
            # Fallback static calculations if ML says clean but metrics are borderline
            detector.detect_suspicious_activity("protected", score)
            
        except (PermissionError, FileNotFoundError, OSError):
            # Gracefully manage multi-thread file system lock constraints without crashing
            pass

    def on_created(self, event):
        if detector.is_locked or is_restoring:
            return
        if event.is_directory:
            return
        write_log(f"[CREATED] {event.src_path}")

    def on_deleted(self, event):
        if detector.is_locked or is_restoring:
            return
        if event.is_directory:
            return
        write_log(f"[DELETED] {event.src_path}")

    def on_moved(self, event):
        if detector.is_locked or is_restoring:
            return
        if event.is_directory:
            return
        write_log(f"[MOVED] {event.src_path} -> {event.dest_path}")
        detector.detect_suspicious_extension(event.dest_path)