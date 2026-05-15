# ============================================================
# Mini Zero Trust Ransomware Resilience System
# Version: 0.5-alpha
#
# Educational cybersecurity project demonstrating:
# - Real-time filesystem monitoring
# - Behavioral ransomware detection
# - Automated response actions
# - Backup resilience mechanisms
# - Secure recovery workflows
# ============================================================


# -----------------------------
# External Libraries
# -----------------------------
# watchdog  -> Real-time filesystem event monitoring
# deque     -> Efficient sliding-window event storage
# hashlib   -> Secure SHA256 hashing for authentication
# shutil    -> File backup/copy operations
# stat      -> Filesystem permission control
# -----------------------------

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
from collections import deque
import time
import hashlib
import sys
import stat
import shutil
import os


# ============================================================
# Logging System
# ============================================================
# Centralized logging utility used across the project.
#
# Responsibilities:
# - Timestamp all events
# - Print live monitoring output
# - Persist logs for forensic visibility
# ============================================================

def write_log(message):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_message = f"{timestamp} {message}"

    print(log_message)

    # Ensure logs directory exists before writing
    os.makedirs("logs", exist_ok=True)

    # Append logs instead of overwriting previous records
    with open("logs/activity.log", 'a') as f:
        f.write(log_message + "\n")


# ============================================================
# Detection State Storage
# ============================================================
# deque stores recent modification timestamps.
#
# Purpose:
# - Track burst file activity
# - Support sliding-window behavioral detection
# ============================================================

recent_modifications = deque()

# Cooldown timer to prevent alert flooding
last_alert_time = 0


# ============================================================
# Response Engine
# ============================================================
# Automatically restricts write access to the protected
# directory after suspicious activity is detected.
#
# This simulates ransomware containment behavior.
# ============================================================

def lock_access(folder_path):

    write_log(f'Attack Detected....Locking down Folder {folder_path}')

    try:

        # Windows-specific lockdown logic
        if sys.platform == 'win32':

            os.system(f'icacls"{folder_path}" /deny Everyone (OI)(CI)(W)')

        # Linux/Mac permission lockdown
        else:

            os.chmod(folder_path, stat.S_IREAD)

        write_log("[SUCCESS] Directory successfully placed into Read-Only mode.")

    except Exception as e:

        write_log(f"[ERROR] Failed to lock folder: {e}")


# ============================================================
# Authentication System
# ============================================================
# SHA256 hash representing the administrator recovery phrase.
#
# Plaintext passwords should NEVER be stored directly.
# ============================================================

STORED_PASSWORD_HASH = "88a8daa34c2a271d0fae2c52641372524cd05d1bc4859054c6a1eab06fc0d029"

#password = mohsan
# ============================================================
# Secure Recovery / Unlock System
# ============================================================
# Allows authorized administrative recovery after a lockdown.
#
# Workflow:
# 1. User enters recovery phrase
# 2. Phrase hashed using SHA256
# 3. Hash compared against stored reference
# 4. Directory permissions restored if verified
# ============================================================

def unlock_folder_securely(folder_path):

    print("\n" + "=" * 40)
    print("      SECURE DIRECTORY UNLOCK SYSTEM      ")
    print("=" * 40)

    # Request recovery phrase
    user_input = input("Enter the security phrase to unlock the folder: ")

    # Securely hash user input before comparison
    input_hash = hashlib.sha256(user_input.encode()).hexdigest()

    # Reject unauthorized access attempts
    if input_hash != STORED_PASSWORD_HASH:

        write_log("[SECURITY] Unauthorized unlock attempt! Access denied.")

        print("[ERROR] Invalid passphrase. Folder remains locked down.")

        return False

    write_log(f"[INFO] Verified authorization passphrase. Restoring access to '{folder_path}'...")

    try:

        # Windows unlock logic
        if sys.platform == "win32":

            os.system(f'icacls "{folder_path}" /remove:deny Everyone')

        # Linux/Mac permission restoration
        else:

            os.chmod(
                folder_path,
                stat.S_IRWXU |
                stat.S_IRGRP |
                stat.S_IXGRP |
                stat.S_IROTH |
                stat.S_IXOTH
            )

        write_log("[SUCCESS] Folder successfully unlocked and open for operations.")

        print("[SUCCESS] Directory is now accessible again.")

        return True

    except Exception as e:

        write_log(f"[ERROR] Decryption/Unlock system failed: {e}")

        return False


# ============================================================
# Backup Engine
# ============================================================
# Creates recovery copies of monitored files.
#
# Optimization:
# - Skip duplicate backups if file size unchanged
# ============================================================

def backup_files(file_path):

    # Ignore non-file events
    if not os.path.isfile(file_path):
        return

    filename = os.path.basename(file_path)

    os.makedirs('backup', exist_ok=True)

    backup_path = f'backup/{filename}'

    # Skip unnecessary backup operations
    if os.path.exists(backup_path):

        if os.path.getsize(file_path) == os.path.getsize(backup_path):
            return

    shutil.copy2(file_path, backup_path)

    write_log(f'[BACKUP] {file_path} -> {backup_path}')


# ============================================================
# Behavioral Detection Engine
# ============================================================
# Detects ransomware-like burst activity using:
# - modification thresholds
# - sliding time windows
# - alert cooldown suppression
# ============================================================

def detect_suspicious_activity(folder_path):

    global last_alert_time

    current_time = time.time()

    # Remove timestamps older than 10 seconds
    while recent_modifications and current_time - recent_modifications[0] > 10:

        recent_modifications.popleft()

    # Trigger alert if excessive modifications detected
    if len(recent_modifications) > 5:

        # Cooldown suppression prevents alert flooding
        if current_time - last_alert_time > 10:

            lock_access(folder_path)

            write_log("[ALERT] Suspicious mass file modification detected!")

            last_alert_time = current_time


# ============================================================
# Monitoring Agent
# ============================================================
# Handles filesystem events generated by watchdog.
#
# This acts as the project's real-time monitoring layer.
# ============================================================

class MonitorHandler(FileSystemEventHandler):


    def on_modified(self, event):

        # Ignore directory-level events
        if event.is_directory:
            return

        src_path = str(event.src_path)

        # Prevent recursive monitoring loops
        if "backup" in src_path or "logs" in src_path:
            return

        # Small delay improves event stability
        time.sleep(0.1)

        # Store modification timestamp
        recent_modifications.append(time.time())

        # Create recovery backup
        backup_files(event.src_path)

        # Log activity
        write_log(f"[MODIFIED] {event.src_path}")

        # Run behavioral analysis
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

        write_log(f"[MOVED] {event.src_path} to {event.dest_path}")


# ============================================================
# Monitoring Initialization
# ============================================================

path = "protected"

# Ensure protected directory exists
os.makedirs(path, exist_ok=True)

event_handler = MonitorHandler()

observer = Observer()

observer.schedule(event_handler, path, recursive=True)

observer.start()

print("Monitoring started...")


# ============================================================
# Main Runtime Loop
# ============================================================
# Keeps monitoring engine active continuously.
# ============================================================

try:

    while True:

        time.sleep(1)


except KeyboardInterrupt:

    print("\n[INFO] Monitoring paused by user.")

    # Optional administrative recovery workflow
    choice = input("Do you want to unlock the protected folder now? (yes/no): ").strip().lower()

    if choice in ['yes', 'y']:

        unlock_folder_securely("protected")


observer.join()