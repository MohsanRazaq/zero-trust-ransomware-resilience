import os
import time
import random
import string
from pathlib import Path

TARGET_DIR = Path("protected")

def generate_random_string(length):
    letters = string.ascii_lowercase + " "
    return "".join(random.choice(letters) for _ in range(length))

def generate_high_entropy_bytes(length):
    return os.urandom(length)

def simulate_normal_user(num_files=30):
    print(f"[🌱 LAB] Simulating {num_files} normal user activities...")
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    for i in range(num_files):
        file_path = TARGET_DIR / f"user_doc_{i}.txt"
        with open(file_path, "w") as f:
            f.write(f"Log event sequence index {i}. " + generate_random_string(100))
        print(f"[🌱 LAB] Created normal document: {file_path}")
        time.sleep(0.1)

def simulate_attack_traffic(num_files=30):
    print(f"\n[💥 LAB] Simulating rapid, high-entropy attack sweep across {num_files} files...")
    for i in range(num_files):
        file_path = TARGET_DIR / f"encrypted_payload_{i}.locked"
        try:
            with open(file_path, "wb") as f:
                f.write(generate_high_entropy_bytes(512))
            print(f"[💥 LAB] Mass modification signature dropped: {file_path}")
        except PermissionError:
            print(f"[🛡️ SYSTEM DEFENSE] ACCESS DENIED! The file system locked down successfully.")
            break
        time.sleep(0.01)

if __name__ == "__main__":
    if TARGET_DIR.exists():
        for item in TARGET_DIR.iterdir():
            if item.is_file():
                try: item.unlink()
                except Exception: pass
    simulate_normal_user(num_files=35)
    print("\n--- Transitioning System State to Attack Scenario ---\n")
    time.sleep(1.5)
    simulate_attack_traffic(num_files=35)