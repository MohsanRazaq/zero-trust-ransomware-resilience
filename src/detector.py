import time
from collections import deque
from logger import write_log
from response import lock_access
from reporter import generate_threat_report
recent_modifications = deque()

last_alert_time = 0

SUSPICIOUS_EXTENSIONS = [
    ".locked",
    ".encrypted",
    ".crypt",
    ".enc"
]


def detect_suspicious_activity(folder_path):

    global last_alert_time

    current_time = time.time()

    while recent_modifications and current_time - recent_modifications[0] > 10:

        recent_modifications.popleft()

    if len(recent_modifications) > 5:

        if current_time - last_alert_time > 10:

            lock_access(folder_path)

            write_log("[ALERT] Suspicious mass file modification detected!")

            last_alert_time = current_time


def detect_suspicious_extension(file_path):

    for extension in SUSPICIOUS_EXTENSIONS:

        if file_path.endswith(extension):

            write_log(f"[ALERT] Suspicious extension detected: {file_path}")
            generate_threat_report( 
            "Suspicious Extension Detection",
            file_path, 
            "Folder Lockdown"
            )

            time.sleep(0.5)

            lock_access("protected")

            return True

    return False