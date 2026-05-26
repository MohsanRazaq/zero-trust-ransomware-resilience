import threading
import time, math
from collections import deque , Counter

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


def check_entropy_threashold(file_path):
    with open (file_path,'rb')as f:
        data=f.read()
        count_frequency=Counter(data)
    entropy_total=0
    for byte in count_frequency.values():
        probability=byte/len(data)
        if probability>0:    
            entropy_total+=probability*math.log2(probability)
    entropy=-(entropy_total)    
    return entropy

def detect_suspicious_activity(folder_path, entropy):
    global last_alert_time, is_locked

    current_time = time.time()

    with _lock:
        while recent_modifications and current_time - recent_modifications[0] > DETECTION_WINDOW_SECONDS:
            recent_modifications.popleft()

        if len(recent_modifications) > DETECTION_THRESHOLD and entropy > 7.5:
            if current_time - last_alert_time > ALERT_COOLDOWN_SECONDS:
                is_locked = True
                lock_access(folder_path)
                
                velocity = len(recent_modifications)
                write_log(f"[ALERT] Suspicious mass file modification detected! Entropy: {entropy:.2f}")
                
                # Updated to pass the entropy score and velocity count
                generate_threat_report(
                    "Mass File Modification",
                    folder_path,
                    "Folder Lockdown",
                    entropy,
                    velocity
                )
                last_alert_time = current_time


def detect_suspicious_extension(file_path):
    global is_locked
    for extension in SUSPICIOUS_EXTENSIONS:
        if file_path.endswith(extension):
            write_log(f"[ALERT] Suspicious extension detected: {file_path}")
            
            # Updated to pass baseline values (0.0 entropy, 1 file event velocity)
            generate_threat_report(
                "Suspicious Extension Detection",
                file_path,
                "Folder Lockdown",
                0.0,
                1
            )
            time.sleep(0.5)
            is_locked = True
            lock_access("protected")
            return True
    return False


def reset_locked_state():
    global is_locked
    is_locked = False