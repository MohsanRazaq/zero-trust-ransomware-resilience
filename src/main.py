import os
import time

from watchdog.observers import Observer

from monitor import MonitorHandler
from response import unlock_access
from recovery import restore_backup


# Protected directory path
path = "protected"

# Ensure protected folder exists
os.makedirs(path, exist_ok=True)

# Initialize monitoring handler
event_handler = MonitorHandler()

# Create observer
observer = Observer()

# Connect observer to protected folder
observer.schedule(event_handler, path, recursive=True)

# Start monitoring engine
observer.start()

print("Monitoring started...")


try:

    while True:

        time.sleep(1)


except KeyboardInterrupt:

    print("\n[INFO] Monitoring paused by user.")

    choice = input("Enter Key: ").strip().lower()

    if choice == "mohsan":

        unlock_access(path)

        restore_backup()

observer.join()