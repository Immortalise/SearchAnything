from config import MONITORED_DIRS_PATH
from utils import filter_subdirectories
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import pickle
import os
import threading
from config import CHANGE_FILES


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.change_files = CHANGE_FILES
        self.file_lock = threading.Lock()
        
        if not os.path.exists(MONITORED_DIRS_PATH):
            self.monitored_dirs = set()
        else:
            with open(MONITORED_DIRS_PATH, 'rb') as file:
                self.monitored_dirs = pickle.load(file)
    

    def write_change(self, change):  
            with self.file_lock:  
                with open(self.changes_file, "a") as file:  
                    file.write(change + "\n") 


    def on_created(self, event):  
        change = "add: {event.src_path}"
        self.write_change(change)


    def on_deleted(self, event):
        change = "delete: {event.src_path}"
        self.write_change(change)


    def on_modified(self, event):  
        change = "modify: {event.src_path}"
        self.write_change(change)
  

    def on_moved(self, event):
        change = "move from {event.src_path} to {event.dest_path}"
        self.write_change(change)


    def close(self):
        with open(MONITORED_DIRS_PATH, 'wb') as file:
            self.monitored_dirs = filter_subdirectories(self.monitored_dirs)
            pickle.dump(self.monitored_dirs, file)



def monitor_dirs():
    event_handler = FileChangeHandler()
    observer = Observer()

    for directory in event_handler.monitored_dirs:
        observer.schedule(event_handler, directory, recursive=True)

    observer.start()
    event_handler.close()
    observer.stop()
    observer.join()

  
def backend_monitor():
    monitor_thread = threading.Thread(target=monitor_dirs)  
    monitor_thread.start()