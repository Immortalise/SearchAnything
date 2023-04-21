import torch
  
from model import create_model
from data import init_db, insert_data, retrieve_data
from utils import encode_text
from process import process_pdf
from index import init_index, add_index, search_index

def run():
    tokenizer, model = create_model(model_name='google/flan-t5-large')
    
    index = init_index()
    db_conn = init_db()

    while True:
        input_text = input("Enter text: ")
        if input_text == "exit":
            db_conn.close()
            break

        elif input_text == "help":
            print("Enter text to search.\nType 'exit' to exit.\nType 'insert' to parse file.\nType 'search' to search file.")

        elif input_text == "insert":
            path = input("File path: ")
            process_pdf(path)

        elif input_text == "search":
            input_embedding = encode_text(tokenizer, model, input_text)
            indices, distances = search_index(index, input_embedding)
            retrieve_data(db_conn, indices, distances)


if __name__ == "__main__":
    run()




