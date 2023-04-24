import torch
  
from model import create_model
from data import init_db, insert_data, retrieve_data, get_file_paths
from utils import encode_text, list_files_with_type
from process import process_file
from index import init_index, insert_index, search_index
from config import SUPPORTED_FILE_TYPE

def run():
    tokenizer, model = create_model(model_name='google/flan-t5-large')
    
    index = init_index()
    db_conn = init_db()
    
    print("FileGPT v0.1")
    print("Type 'exit' to exit.\nType 'insert' to parse file.\nType 'search' to search file.")

    while True:
        input_text = input("Instruction: ")
        # input_text = "insert"

        if input_text == "exit":
            db_conn.close()
            break

        elif input_text == "insert":
            path = input("File path: ")

            file_list = list_files_with_type(path)
            for file in file_list:
                file_path = file['path']
                file_type = file['type']
                if (file_type in SUPPORTED_FILE_TYPE) and (file_path not in get_file_paths(db_conn)):
                    line_list = process_file(file_path, tokenizer, model)
                    insert_data(db_conn, line_list)
                    insert_index(index, line_list)


        elif input_text == "search":
            input_text = input("Search: ")
            input_embedding = encode_text(tokenizer, model, input_text)
            indices, distances = search_index(index, input_embedding)
            print(indices)
            print(distances)
            retrieve_data(db_conn, indices)


if __name__ == "__main__":
    run()




