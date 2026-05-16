import hashlib
import hmac
import os
import time

from watchdog.observers import Observer

from constants import PROTECTED_DIR
from monitor import MonitorHandler
from response import unlock_access
from recovery import restore_backup


def _get_expected_key_hash() -> str:
    """
    Read the recovery key from the environment and return its SHA-256 hex digest.
    Set the environment variable before running:
        export RECOVERY_KEY="your-secret-here"
    Never hardcode the key in source code.
    """
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
    observer = Observer()
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
                restore_backup()
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
