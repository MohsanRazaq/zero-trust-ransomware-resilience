import os
from datetime import datetime

from constants import LOG_DIR


def write_log(message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"{timestamp} {message}"

    print(log_message)

    os.makedirs(LOG_DIR, exist_ok=True)

    with open(f"{LOG_DIR}/activity.log", "a") as f:
        f.write(log_message + "\n")
