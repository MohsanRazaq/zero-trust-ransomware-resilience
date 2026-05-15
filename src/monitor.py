from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
from collections import deque
import time
import shutil
import os
def write_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message=f"{timestamp} {message}"
    print(log_message)
    with open("logs/activity.log",'a') as f:
        f.write(log_message +"\n")
       
recent_modifications = deque()
last_alert_time = 0


def backup_files(file_path):
    if not os.path.isfile(file_path):
        return
    filename=os.path.basename(file_path)
    backup_path=f'backup/{filename}'
    shutil.copy2(file_path,backup_path)
    write_log(f'[BACKUP]{file_path}->{backup_path}')
    
def detect_suspicious_activity():
    global last_alert_time
    current_time=time.time()
    while recent_modifications and current_time-recent_modifications[0]>10:
        recent_modifications.popleft()
    if len(recent_modifications)>5:
        if current_time - last_alert_time>10:
            write_log("[ALERT] Suspicious mass file modification detected!")
            last_alert_time=current_time
        ##----------------------------------------------
class MonitorHandler(FileSystemEventHandler):


    def on_modified(self, event):
        if event.is_directory:
            return
        recent_modifications.append(time.time())
        backup_files(event.src_path)
        write_log(f"[MODIFIED] {event.src_path}")
        detect_suspicious_activity()
    def on_created(self, event):
        if event.is_directory:
            return
        write_log(f"[CREATED]  {event.src_path}")

    def on_deleted(self, event):
        if event.is_directory:
            return
        write_log(f"[DELETED] {event.src_path}")
        
    def on_moved(self, event):
        if event.is_directory:
            return
        write_log(f"[MOVED] {event.src_path} to {event.dest_path}")
      
path = "protected"

event_handler = MonitorHandler()

observer = Observer()
observer.schedule(event_handler, path, recursive=True)

observer.start()

print("Monitoring started...")

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    observer.stop()

observer.join()