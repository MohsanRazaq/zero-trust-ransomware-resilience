from datetime import datetime
import os

def write_log(message):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_message = f"{timestamp} {message}"

    print(log_message)

    # Ensure logs directory exists before writing
    os.makedirs("logs", exist_ok=True)

    # Append logs instead of overwriting previous records
    with open("logs/activity.log", 'a') as f:
        f.write(log_message + "\n")
