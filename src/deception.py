import os
import sys
from pathlib import Path

# New Flat Design: A high-priority direct tripwire file
CANARY_FILE_NAME = "_000_sys_backup_manifest.txt"

def deploy_honey_tokens(tar_dir):
    protected_path = Path(tar_dir)
    protected_path.mkdir(parents=True, exist_ok=True)
    
    # Place the trap file directly inside 'protected/'
    CANARY_FILE = protected_path / CANARY_FILE_NAME
    
    # Write the file if it DOES NOT exist yet
    if not CANARY_FILE.exists():
        try:
            with open(CANARY_FILE, 'w') as f:
                f.write("SYS_CONFIGURATION_MANIFEST: Do not modify or delete. Baseline index tracking tokens.")
            
            # Hide the file from standard terminal listings/views
            if sys.platform == "win32":
                import ctypes
                ctypes.windll.kernel32.SetFileAttributesW(str(CANARY_FILE), 2)
        except Exception as e:
            print(f"[WARN] Could not safely configure trap attributes: {e}")
        
    print(f"[INFO] Deception Honeytoken successfully armed at: {CANARY_FILE}")
    return str(CANARY_FILE)


def is_honeytoken_breached(modified_path):
    """
    Returns True if the modified file path hits our direct tripwire token.
    """
    # Look for the exact filename string anywhere in the event path
    return "_000_sys_backup_manifest" in str(modified_path)