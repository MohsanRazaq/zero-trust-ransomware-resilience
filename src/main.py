import hashlib
import hmac
import os
import time

from watchdog.observers import Observer
from src.integrity_monitor import IntegrityHandler
from src.monitor import MonitorHandler
from src.constants import PROTECTED_DIR
from src.response import unlock_access

def _get_expected_key_hash() -> str:
    key = os.environ.get("RECOVERY_KEY", "")
    if not key:
        raise RuntimeError(
            "RECOVERY_KEY environment variable is not set. "
            "Run:  export RECOVERY_KEY='your-secret'  before starting."
        )
    return hashlib.sha256(key.encode()).hexdigest()

def _verify_key(user_input: str, expected_hash: str) -> bool:
    """
    Compare the user-supplied key against the stored hash using a
    constant-time comparison to prevent timing attacks.
    """
    input_hash = hashlib.sha256(user_input.encode()).hexdigest()
    return hmac.compare_digest(input_hash, expected_hash)

def main() -> None:
    expected_hash = _get_expected_key_hash()

    os.makedirs(PROTECTED_DIR, exist_ok=True)

    event_handler = MonitorHandler()
    integrity_handler = IntegrityHandler()
    
    observer = Observer()

    # Schedule both integrity tracking and behavioral ML monitoring
    observer.schedule(integrity_handler, PROTECTED_DIR, recursive=True)
    observer.schedule(event_handler, PROTECTED_DIR, recursive=True)
    
    observer.start()
    print("Monitoring started...")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[INFO] Monitoring paused by user.")

        attempts = 0
        max_attempts = 3

        while attempts < max_attempts:
            key_input = input("Enter recovery key: ").strip()
            attempts += 1

            if _verify_key(key_input, expected_hash):
                unlock_access(PROTECTED_DIR)
                break
            else:
                remaining = max_attempts - attempts
                if remaining:
                    print(f"[ERROR] Wrong key. {remaining} attempt(s) left.")
                else:
                    print("[ERROR] Too many failed attempts. Recovery aborted.")

    finally:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()