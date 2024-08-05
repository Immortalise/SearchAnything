import os
import sys
import subprocess
import requests
import re
from pathlib import Path
import numpy as np

from config import __version__, TEXT_TYPES, IMAGE_TYPES


def check_for_updates():
    response = requests.get(f"https://github.com/Immortalise/Anything/releases/latest")
    latest_version = re.search(r"releases/tag/v([\d.]+)", response.url).group(1)
  
    if latest_version != __version__:
        print(f"Update available!\nCurrent version: {__version__}\nLatest version: {latest_version}\nPlease visit https://github.com/{user}/{repo}/releases/latest to get the latest version.")
    else:
        print("You are using the latest version.")

  
def update_and_restart():
    try:
        subprocess.check_call(["git", "pull"])
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        print(f"Update error: {str(e)}")
        sys.exit(1)

# def get_directory_state(path):  
#     directory_state = {}  
#     for root, dirs, files in os.walk(path):  
#         for file_name in files:  
#             file_path = os.path.join(root, file_name)  
#             directory_state[file_path] = os.path.getmtime(file_path)  
        
#         for dir_name in dirs:  
#             dir_path = os.path.join(root, dir_name)  
#             directory_state[dir_path] = os.path.getmtime(dir_path)

#     return directory_state  

  
# def compare_directory_states(old_state, new_state):  
#     added_items = set(new_state.keys()) - set(old_state.keys())  
#     deleted_items = set(old_state.keys()) - set(new_state.keys())  
#     modified_items = {item for item in new_state if item in old_state and new_state[item] != old_state[item]}  
  
#     def filter_items(items):  
#         filtered_items = set()  
#         for item in items:  
#             parent_dir = os.path.dirname(item)  
#             if parent_dir not in items:  
#                 filtered_items.add(item)  
#         return filtered_items  
  
#     filtered_added_items = filter_items(added_items)  
#     filtered_deleted_items = filter_items(deleted_items)  
#     filtered_modified_items = filter_items(modified_items)  
  
#     return filtered_added_items, filtered_deleted_items, filtered_modified_items  


def filter_subdirectories(directories):
    filtered_dirs = set()
  
    for dir1 in directories:
        is_subdir = False
        for dir2 in directories:
            if dir1 != dir2 and os.path.commonpath([dir1, dir2]) == dir2:
                is_subdir = True
                break
        if not is_subdir:
            filtered_dirs.add(dir1)
  
    return filtered_dirs


def parse_data_type(suffix):
    return "image" if suffix in IMAGE_TYPES else "text" if suffix in TEXT_TYPES else "N/A"


def list_files(root_path):
    results = []
    root_path = Path(root_path)
    
    if root_path.is_file():
        paths = [root_path]
    else:
        paths = root_path.rglob('*')
    
    for path in paths:
        suffix = path.suffix[1:]
        data_type = parse_data_type(suffix)
        
        if data_type != "N/A":
            results.append({"path": str(path), "suffix": suffix, "type": data_type})
    
    return results

# Retrieve a single file's information instead of for files in a folder
# An alternative version of above function 'list_files'
def verify_file(file_path):
    results = None
    file_path = Path(file_path)
    
    suffix = file_path.suffix[1:]
    data_type = parse_data_type(suffix)
    
    if data_type != "N/A":
        results = {"path": str(file_path), "suffix": suffix, "type": data_type}
    
    return results
    

def encode_text(model, input_text):
    embedding = model.encode(input_text)

    embedding_l2 = np.linalg.norm(embedding)
    embedding = embedding / embedding_l2

    return embedding


def encode_image(model, input_image):
    embedding = model.encode(input_image)

    embedding_l2 = np.linalg.norm(embedding)
    embedding = embedding / embedding_l2

    return embedding