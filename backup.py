import os
import shutil
from datetime import datetime

from constants import BACKUP_DIR, MAX_BACKUP_VERSIONS
from logger import write_log


def _prune_old_versions(filename: str) -> None:
    """
    Keep only the MAX_BACKUP_VERSIONS most recent backups for a given base filename.
    Deletes the oldest ones when the limit is exceeded.
    """
    prefix=filename+'_'

    EXITED=sorted(f for f in os.listdir(BACKUP_DIR) if prefix.startswith(prefix))
    
    while len(EXITED)>=MAX_BACKUP_VERSIONS:
        oldest=os.path.join(BACKUP_DIR,EXITED.pop(0))
        try:
            
            os.chmod(oldest,0o644)
            os.remove(oldest)
            write_log(f'Alert: file removed')

        except Exception as e:
            write_log(f"[ERROR] Could not prune backup {oldest}: {e}")
            break

def backup_files(file_path: str) -> None:
    if not os.path.exists(file_path):
        return
    filename=os.path.basename(file_path)
    os.makedirs(BACKUP_DIR,exist_ok=True)
    _prune_old_versions(filename)
    
    Timestamps=datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    Backup_path=os.path.join(BACKUP_DIR,f'filename')