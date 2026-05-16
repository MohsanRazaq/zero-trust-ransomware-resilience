import os
import shutil
from logger import write_log

is_restoring = False

def restore_backup():

    global is_restoring

    is_restoring = True

    write_log('[RECOVERY] Starting backup restoration process')

    try:

        os.makedirs('protected', exist_ok=True)

        for filename in os.listdir('backup'):

            backup_file_path = os.path.join('backup', filename)

            protected_file_path = os.path.join('protected', filename)
            if not os.path.isfile(backup_file_path):
                continue

            shutil.copy2(backup_file_path,protected_file_path
            )

            write_log(f'[RESTORED] {filename}')

        write_log("[SUCCESS] Backup restoration completed")

    except Exception as e:

        write_log(f"[ERROR] Recovery failed: {e}")

    is_restoring = False