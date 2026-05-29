import os
import time
from pathlib import Path

TARGET_DIR = "protected"

def run_mock_ransomware():
    print("[💥 ATTACK] Booting ransomware simulator payload...")
    time.sleep(1)
    
    target_path = Path(TARGET_DIR)
    if not target_path.exists():
        print(f"[❌ ERROR] Target directory '{TARGET_DIR}' does not exist! Run your detector script first to setup traps.")
        return

    # 1. Gather all files and directories inside the target space
    # Real ransomware lists files sequentially to encrypt everything
    all_items = sorted(os.listdir(target_path))
    
    print(f"[💥 ATTACK] Scanned directory tree. Found contents: {all_items}")
    time.sleep(1)

    # 2. Iterate through the target items alphabetically
    for item in all_items:
        full_path = target_path / item
        
        # If it's a directory, look inside for a file to encrypt
        if full_path.is_dir():
            sub_files = sorted(os.listdir(full_path))
            if sub_files:
                target_file = full_path / sub_files[0]
            else:
                continue
        else:
            target_file = full_path

        # 3. Execution: Attempt to overwrite the file contents with encrypted noise
        print(f"[💥 ATTACK] Target locked! Attempting to encrypt: {target_file}")
        try:
            with open(target_file, "w") as f:
                # Writing high-entropy data noise to simulate cryptographic mutation
                f.write("XY7z!@#9mK$pL9QW==_ENCRYPTED_BY_MOCK_RANSOMWARE")
            print(f"[💥 ATTACK] Successfully encrypted: {target_file}")
        except PermissionError:
            print(f"[🛡️ SYSTEM DEFENSE] ACCESS DENIED! The file system locked down successfully.")
            break
        except Exception as e:
            print(f"[❌ ERROR] Attack interrupted: {e}")
            break
            
        # Small delay to watch the terminal output stream clear
        time.sleep(0.5)

if __name__ == "__main__":
    run_mock_ransomware()