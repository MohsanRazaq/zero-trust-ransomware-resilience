from src.integrity_monitor import get_score
from src.constants import BACKUP_DIR, LOG_DIR
from src.logger import write_log

import threading
import time, math
from collections import deque , Counter
from constants import (
    SUSPICIOUS_EXTENSIONS,
    DETECTION_WINDOW_SECONDS,
    DETECTION_THRESHOLD,
    ENTROPY_SCORE_THREASHOLD,
    ALERT_COOLDOWN_SECONDS
)
from reporter import generate_threat_report
from response import lock_access

recent_modifications = deque()
last_alert_time = 0.0
_lock = threading.Lock()
is_locked = False

# Establish the baseline metric score from integrity monitor
INITIAL_INTEGRITY_SCORE = get_score(20)  
THREAT_SCORE = INITIAL_INTEGRITY_SCORE

def check_entropy_threashold(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
        count_frequency = Counter(data)
    
    if not data:
        return 0.0
        
    entropy_total = 0
    for byte in count_frequency.values():
        probability = byte / len(data)
        if probability > 0:    
            entropy_total += probability * math.log2(probability)
    return -(entropy_total)


def detect_suspicious_activity(folder_path, entropy):
    
    global THREAT_SCORE, last_alert_time, is_locked
    if is_honeytoken_breached(folder_path):
        with _lock:
            THREAT_SCORE=150
            is_locked=True
            write_log(f"[CRITICAL] HONEYTOKEN TRAP BREACHED AT: {folder_path}! Instant isolation triggered.")
            lock_access(folder_path)
            
            
        generate_threat_report(
                "Deception Trap Honeytoken Breach",
                folder_path,
                "Instant Automated Folder Lockdown",
                entropy,
                1,
                THREAT_SCORE
            )
        return
    
    
    #--------------------------------------------------------------------------------------
        # Bring all variables to be modified into global scope safely

    current_time = time.time()

    # Keep all read/write state checks inside the Mutex Lock to avoid Race Conditions
    with _lock:
        # 1. Prune stale timestamps outside the  tracking timeline window
        while recent_modifications and current_time - recent_modifications[0] > DETECTION_WINDOW_SECONDS:
            recent_modifications.popleft()

        # 2. Local State Risk Accumulator Evaluation (Reset baseline each evaluation loop)
        current_event_risk = INITIAL_INTEGRITY_SCORE
        
        if entropy > ENTROPY_SCORE_THREASHOLD:
            current_event_risk += 40 
            
        if len(recent_modifications) > DETECTION_THRESHOLD:
            current_event_risk += 30

        THREAT_SCORE = current_event_risk

        # 3. Mitigation Execution Strategy Check
        if THREAT_SCORE > 50:    
            if current_time - last_alert_time > ALERT_COOLDOWN_SECONDS:
                is_locked = True
                lock_access(folder_path)
            
                velocity = len(recent_modifications)
                write_log(f"[ALERT] Security Engine Active Isolation! Entropy: {entropy:.2f} Calculated Risk Score: {THREAT_SCORE:.2f}")
                
                generate_threat_report(
                    "Mass File Modification",
                    folder_path,
                    "Folder Lockdown",
                    entropy,
                    velocity,
                    THREAT_SCORE
                )
                last_alert_time = current_time
        else:
            # Slow metric decay loop if baseline activity is normal
            if THREAT_SCORE > INITIAL_INTEGRITY_SCORE:
                THREAT_SCORE -= 5

def detect_suspicious_extension(file_path):
    global THREAT_SCORE, is_locked
    for extension in SUSPICIOUS_EXTENSIONS:
        if file_path.endswith(extension):
            with _lock:
                THREAT_SCORE += 100
            
            write_log(f"[ALERT] Suspicious extension signature match: {file_path}")
            
            generate_threat_report(
                "Suspicious Extension Detection",
                file_path,
                "Folder Lockdown",
                0.0,
                1,
                THREAT_SCORE
            )
            time.sleep(0.5)
            is_locked = True
            lock_access("protected")
            return True
    return False

def reset_locked_state():
    global is_locked, THREAT_SCORE
    is_locked = False
    with _lock:
        THREAT_SCORE = INITIAL_INTEGRITY_SCORE