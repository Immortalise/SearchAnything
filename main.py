from watchdog.events import FileSystemEventHandler
import pickle
import os

from config import MONITORED_DIRS_PATH
from model import create_model
from data import init_db, insert_data, retrieve_data, get_file_paths
from utils import encode_text, filter_subdirectories, list_files_with_type
from process import process_file
from index import init_index, insert_index, search_index
from config import SUPPORTED_FILE_TYPE


class FileGPT(object):
    def __init__(self, model_name):
        self.tokenizer, self.model = create_model(model_name)
        self.index = init_index()
        self.db_conn = init_db()
        print("FileGPT v0.1")
        print("Type 'exit' to exit.\nType 'insert' to parse file.\nType 'search' to search file.")
    

    def insert(self, path):
        file_list = list_files_with_type(path)
        for file in file_list:
            file_path = file['path']
            file_type = file['type']
            if (file_type in SUPPORTED_FILE_TYPE) and (file_path not in get_file_paths(self.db_conn)):
                
                print("Processing file: ", file_path)

                line_list = process_file(file_path, self.tokenizer, self.model)
                insert_data(self.db_conn, line_list)
                insert_index(self.index, line_list)

    
    def search(self, input_text):
        input_embedding = encode_text(self.tokenizer, self.model, input_text)
        indices, distances = search_index(self.index, input_embedding)
        return retrieve_data(self.db_conn, indices)

    
    def close(self):
        self.db_conn.close()
        self.file_change_handler.close()


    def run(self):
        while True:
            input_text = input("Instruction: ")

            if input_text == "exit":
                self.close()
                break

            elif input_text == "insert":
                path = input("File path: ")
                self.insert(path)

            elif input_text == "search":
                input_text = input("Search text: ")
                result = self.search(input_text)
                print(result)

            else:
                print("Invalid instruction.")


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, filegpt: FileGPT):
        
        self.filegpt = filegpt

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
        # self.filegpt.delete(event.src_path)
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
    file_gpt = FileGPT("gpt2")
    file_gpt.run()




