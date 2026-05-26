import os
import random
import time

# CONFIGURATION: Change this to the exact path of  test/protected directory
TARGET_DIR = "./protected" 

def generate_random_bytes(size_in_bytes):
    """Generates purely random data which has maximum Shannon Entropy (~8.0)."""
    return bytes(random.randint(0, 255) for _ in range(size_in_bytes))

def simulate_ransomware_attack(directory):
    print(f"[!] Starting Ransomware Simulation target: {directory}")
    
    # Ensure the target directory exists so we don't crash
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"[*] Created target directory: {directory}")

    # 1. Create 15 small dummy text files first to give the script targets
    print("[*] Preparing dummy files...")
    file_paths = []
    for i in range(15):
        file_path = os.path.join(directory, f"user_document_{i}.txt")
        with open(file_path, "w") as f:
            f.write("This is a normal, low-entropy text document containing standard prose.")
        file_paths.append(file_path)
    
    # Wait a brief moment to let the file system settle
    time.sleep(1)
    print("[*] Setup complete. Unleashing high-entropy rapid modification...")

    # 2. Rapidly overwrite the files with pure mathematical chaos
    for path in file_paths:
        try:
            print(f"[>] Encrypting/Overwriting: {path}")
            
            # Generate 1KB of maximum chaos (Entropy ~8.0)
            high_entropy_payload = generate_random_bytes(1024)
            
            # Overwrite the clean file in binary mode
            with open(path, "wb") as f:
                f.write(high_entropy_payload)
            
            # Sleep briefly to mimic a fast script loop, staying within your detection window
            time.sleep(0.05) 
            
        except PermissionError:
            print(f"\n[✓] SUCCESS: Permission Denied at {path}!")
            print("[✓] Validation confirmed: Your Zero-Trust System successfully locked the folder mid-attack!")
            return
        except Exception as e:
            print(f"\n[-] Script stopped due to system action: {e}")
            return

    print("\n[-] Simulation finished. If your folder didn't lock down, check your thresholds!")

if __name__ == "__main__":
    simulate_ransomware_attack(TARGET_DIR)