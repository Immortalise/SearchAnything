from utils import *
import sys 
import time
from watchdog.observers import Observer

# print(list_files_with_type("./"))




# # Example usage  
# directories = {"files", "files/pdfs", "files/txt"}  
  
  
# print(filtered_directories) 


event_handler = FileChangeHandler()
# event_handler.monitored_dirs.add("./")
print(event_handler.monitored_dirs)
# filtered_directories = event_handler.monitored_dirs
# observer = Observer()
  
# for directory in filtered_directories:
#     observer.schedule(event_handler, directory, recursive=True)
  
# observer.start()
  
# try:  
#     while True:  
#         time.sleep(1)  
# except KeyboardInterrupt:  
#     observer.stop()  
# observer.join()
event_handler.close()