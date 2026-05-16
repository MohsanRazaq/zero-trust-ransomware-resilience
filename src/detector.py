import threading
import time
from collections import deque

from constants import (
    SUSPICIOUS_EXTENSIONS,
    DETECTION_WINDOW_SECONDS,
    DETECTION_THRESHOLD,
    ALERT_COOLDOWN_SECONDS,
)
from logger import write_log
from reporter import generate_threat_report
from response import lock_access

recent_modifications = deque()
last_alert_time = 0.0
_lock = threading.Lock()
is_locked = False


def detect_suspicious_activity(folder_path):
    global last_alert_time, is_locked

    current_time = time.time()

    with _lock:
        while recent_modifications and current_time - recent_modifications[0] > DETECTION_WINDOW_SECONDS:
            recent_modifications.popleft()

        if len(recent_modifications) > DETECTION_THRESHOLD:
            if current_time - last_alert_time > ALERT_COOLDOWN_SECONDS:
                is_locked = True
                lock_access(folder_path)
                write_log("[ALERT] Suspicious mass file modification detected!")
                generate_threat_report(
                    "Mass File Modification",
                    folder_path,
                    "Folder Lockdown",
                )
                last_alert_time = current_time


def detect_suspicious_extension(file_path):
    global is_locked
    for extension in SUSPICIOUS_EXTENSIONS:
        if file_path.endswith(extension):
            write_log(f"[ALERT] Suspicious extension detected: {file_path}")
            generate_threat_report(
                "Suspicious Extension Detection",
                file_path,
                "Folder Lockdown",
            )
            time.sleep(0.5)
            is_locked = True
            lock_access("protected")
            return True
    return False


def reset_locked_state():
    global is_locked
    is_locked = False