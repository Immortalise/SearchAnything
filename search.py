import os
from sentence_transformers import SentenceTransformer

from config import DATA_DIR, SUPPORTED_FILE_TYPE, TEXT_EMBEDDING_MODELS, IMAGE_EMBEDDING_MODELS
from db import File_DB, Image_DB
from utils import encode_text, list_files_with_type
from process import process_file
from index import SemanticIndex, BM25Index, ExactMatchIndex


class Anything(object):
    def __init__(self, models=None):

        if models is None:
            models = ["sentence-transformers/all-mpnet-base-v2", "clip-ViT-B-32"]

        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)  
        
        self.dbs = self.load_dbs()
        self.models = self.load_models(models)
        self.indices = self.load_indices()

        print("Anything v0.2.0")
        print("Type 'exit' to exit.\n\
              Type 'insert' to parse file.\n\
              Type 'search' to search file.\n\
              Type 'search_bm25' to search file with bm25.\n\
              Type 'search_exact' to search file with exact match.\n\
              Type 'delete' to delete file.")
        
    def load_dbs(self):
        return {"file": File_DB(), "image": Image_DB()}

    def load_indices(self):
        indices = {}

        for data_type in self.dbs.keys():
            if data_type == "file":
                type_indices = {"semantic": SemanticIndex(dim=768), "bm25": BM25Index(self.dbs[data_type]), "exact": ExactMatchIndex(self.dbs[data_type])}
            elif data_type == "image":
                type_indices = {"semantic": SemanticIndex(dim=512), "bm25": BM25Index(self.dbs[data_type]), "exact": ExactMatchIndex(self.dbs[data_type])}
            
            indices[type] = type_indices
        
        return indices


    def load_models(self, model_names):
        for model_name in model_names:
            if model_name in TEXT_EMBEDDING_MODELS or model_name in IMAGE_EMBEDDING_MODELS:
                self.model = SentenceTransformer(model_name)
            else:
                raise ValueError("Model name not supported.")

   
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
            
            elif input_text == "semantic_search":
                input_text = input("Search text: ")
                self.semantic_search(input_text)
            
            elif input_text == "bm25_search":
                input_text = input("Search text: ")
                self.bm25_search(input_text)
            
            elif input_text == "exact_search":
                input_text = input("Search text: ")
                self.exact_search(input_text)

            else:
                print("Invalid instruction.")


    def insert(self, path):
        file_list = list_files_with_type(path)
        for file in file_list:
            file_path = file['path']
            file_type = file['type']
            db = self.dbs[file_type]
            type_indices = self.indices[file_type]

            if (file_type in SUPPORTED_FILE_TYPE) and (file_path not in db.get_existing_file_paths()):
                
                print("Processing file: ", file_path)

                line_list = process_file(file_path, file_type, self.model)
                inserted_ids = db.insert_data(line_list)
                for _, index in type_indices.items():
                    index.insert_index(line_list, inserted_ids)


    # def delete(self, path):
    #     is_dir = os.path.isdir(path)
        
    #     remaining_embeddings, remaining_ids = self.db.delete_data(path, is_directory=is_dir)
    #     self.index.rebuild_index(remaining_embeddings, remaining_ids)
    #     self.bm25_index.rebuild_index(remaining_embeddings, remaining_ids)
    #     self.exact_macth_index.rebuild_index(remaining_embeddings, remaining_ids)

    def semantic_search(self, data_type, input_text):

        query_embedding = encode_text(self.models["file"], input_text)
        data_idxs, distances = self.indices[data_type]["semantic"].search_index(query_embedding)
        columns, results = self.dbs[data_type].retrieve_data(data_idxs)
        
        return self._process_output(distances, columns, results)
    

    def bm25_search(self, data_type, input_text):
        data_idxs, distances = self.indices[data_type]["bm25"].search_index(input_text)
        columns, results = self.dbs[data_type].retrieve_data(data_idxs)
        
        return self._process_output(distances, columns, results)
    

    def exact_search(self, data_type, input_text):
        data_idxs, distances = self.indices[data_type]["exact"].search_index(input_text)
        columns, results = self.dbs[data_type].retrieve_data(data_idxs)

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
        for db in self.dbs.values():
            db.close()
        
        for type_indices in self.indices.values():
            for index in type_indices.values():
                index.close()



if __name__ == "__main__":
    Anything = Anything()
    Anything.run()





