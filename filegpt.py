import os
from sentence_transformers import SentenceTransformer

from config import DATA_DIR, SUPPORTED_FILE_TYPE
from database import DataBase
from utils import encode_text, list_files_with_type
from process import process_file
from index import Index, BM25Index, ExactMatchIndex
from config import SUPPORTED_FILE_TYPE    


class FileGPT(object):
    def __init__(self, model_name):

        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
                  
        self.model = SentenceTransformer(model_name)
        self.index = Index(dim=768)
        self.db = DataBase()
        self.bm25_index = BM25Index(self.db)
        self.exact_macth_index = ExactMatchIndex(self.db)
        print("FileGPT v0.1")
        print("Type 'exit' to exit.\nType 'insert' to parse file.\nType 'search' to search file.\nType 'search_bm25' to search file with bm25.\nType 'search_exact' to search file with exact match.\nType 'delete' to delete file.")

   
    def run(self):
        while True:
            input_text = input("Instruction: ")

            if input_text == "exit":
                self.close()
                break

            elif input_text == "insert":
                path = input("File path: ")
                self.insert(path)

            elif input_text == "delete":
                path = input("File path: ")
                self.delete(path)
            
            elif input_text == "search":
                input_text = input("Search text: ")
                self.search(input_text)
            
            elif input_text == "search_bm25":
                input_text = input("Search text: ")
                self.search_bm25(input_text)
            
            elif input_text == "search_exact":
                input_text = input("Search text: ")
                self.search_exact(input_text)

            else:
                print("Invalid instruction.")


    def insert(self, path):
        file_list = list_files_with_type(path)
        for file in file_list:
            file_path = file['path']
            file_type = file['type']
            if (file_type in SUPPORTED_FILE_TYPE) and (file_path not in self.db.get_existing_file_paths()):
                
                print("Processing file: ", file_path)

                line_list = process_file(file_path, file_type, self.model)
                inserted_ids = self.db.insert_data(line_list)
                self.index.insert_index(line_list, inserted_ids)
                self.bm25_index.insert_index(line_list, inserted_ids)
                self.exact_macth_index.insert_index(line_list, inserted_ids)

    def delete(self, path):
        is_dir = os.path.isdir(path)
        remaining_embeddings, remaining_ids = self.db.delete_data(path, is_directory=is_dir)
        self.index.rebuild_index(remaining_embeddings, remaining_ids)
        self.bm25_index.rebuild_index(remaining_embeddings, remaining_ids)
        self.exact_macth_index.rebuild_index(remaining_embeddings, remaining_ids)

    def search(self, input_text):
        query_embedding = encode_text(self.model, input_text)
        indices, distances = self.index.search_index(query_embedding)
        columns, results = self.db.retrieve_data(indices)
        
        return self._process_output(distances, columns, results)

    def search_bm25(self, input_text):
        indices, distances = self.bm25_index.search_index(input_text)
        columns, results = self.db.retrieve_data(indices)
        return self._process_output(distances, columns, results)
    
    def search_exact(self, input_text):
        indices, distances = self.exact_macth_index.search_index(input_text)
        columns, results = self.db.retrieve_data(indices)
        return self._process_output(distances, columns, results)
    
    def _process_output(self, distances, columns, raw_results):
        dict_list = []
        for distance, raw_result in zip(distances, raw_results):
            d = {}
            d['distance'] = distance
            for column, result in zip(columns, raw_result):
                d[column] = result
            
            dict_list.append(d)

        combined_dict = {}  
    
        for d in dict_list:  
            file_path = d["file_path"]  
    
            if file_path not in combined_dict.keys():  
                combined_dict[file_path] = {  
                    "min_distance": float("inf"),
                    "content": [],  
                    "distance": [],  
                    "page": [],  
                }  

            combined_dict[file_path]["min_distance"] = min(combined_dict[file_path]["min_distance"], d["distance"])
            combined_dict[file_path]["content"].append(d["content"])  
            combined_dict[file_path]["page"].append(d["page"])
            combined_dict[file_path]["distance"].append(d["distance"])  

        sorted_list = sorted(combined_dict.items(), key=lambda x: x[1]["min_distance"])  

        return sorted_list 
    
    def close(self):
        self.db.close()
        self.index.close()
        self.bm25_index.close()
        self.exact_macth_index.close()


if __name__ == "__main__":
    filegpt = FileGPT("sentence-transformers/all-mpnet-base-v2")
    filegpt.run()





