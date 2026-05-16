import os
import shutil
from datetime import datetime
from logger import write_log

def backup_files(file_path):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Ignore non-file events
    if not os.path.isfile(file_path):
        return

    filename = os.path.basename(file_path)

    os.makedirs('backup', exist_ok=True)

    backup_path = os.path.join(
        'backup',f'{filename}_{timestamp}'
    )

    shutil.copy2(file_path, backup_path)

    write_log(f'[BACKUP] {file_path} -> {backup_path}')