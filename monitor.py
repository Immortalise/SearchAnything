from config import MONITORED_DIRS_PATH
from utils import filter_subdirectories
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import pickle
import os


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self):
        
        if not os.path.exists(MONITORED_DIRS_PATH):
            self.monitored_dirs = set()
        else:
            with open(MONITORED_DIRS_PATH, 'rb') as file:
                self.monitored_dirs = pickle.load(file)
                    

    def on_created(self, event):  
        print(f"{'Directory' if event.is_directory else 'File'} added: {event.src_path}")  
        self.filegpt.insert(event.src_path)
  
    def on_deleted(self, event):
        print(f"{'Directory' if event.is_directory else 'File'} deleted: {event.src_path}")
        self.filegpt.delete(event.src_path)
        self.monitored_dirs.remove(event.src_path)
  
    def on_modified(self, event):  
        print(f"{'Directory' if event.is_directory else 'File'} modified: {event.src_path}")
        self.filegpt.delete(event.src_path)
        self.filegpt.insert(event.src_path)
  
    def on_moved(self, event):
        print(f"{'Directory' if event.is_directory else 'File'} moved from {event.src_path} to {event.dest_path}")
    
    def close(self):
        with open(MONITORED_DIRS_PATH, 'wb') as file:
            self.monitored_dirs = filter_subdirectories(self.monitored_dirs)
            pickle.dump(self.monitored_dirs, file)



if __name__ == "__main__":
    event_handler = FileChangeHandler()
    observer = Observer()

    for directory in event_handler.monitored_dirs:
        observer.schedule(event_handler, directory, recursive=True)

    observer.start()
    event_handler.close()
    observer.stop()
    observer.join()