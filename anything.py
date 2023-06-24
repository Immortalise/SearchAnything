import os
from sentence_transformers import SentenceTransformer

from config import DATA_DIR, DB_PATH, TEXT_EMBEDDING_MODELS, IMAGE_EMBEDDING_MODELS
from database import Text_DB, Image_DB
from utils import encode_text, encode_image, list_files
from process import process_file
from index import SemanticIndex


class Anything(object):
    def __init__(self, models=None):

        if models is None:
            default_models = ["sentence-transformers/all-mpnet-base-v2", "clip-ViT-B-32"]

        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)  
        
        self.dbs = self.load_dbs()
        self.models = self.load_models(default_models)
        # self.indices = self.load_indices()
        self.index = self.load_index()

        

        print("Anything v1.0")
        print("Type 'exit' to exit.\n\
              Type 'insert' to parse file.\n\
              Type 'search' to search file.\n\
              Type 'delete' to delete file.")
        
    def load_dbs(self):
        return {"text": Text_DB(), "image": Image_DB()}


    def load_index(self):
        index = {"semantic": SemanticIndex(DB_PATH)}     
        return index


    # def load_indices(self):
    #     indices = {}

    #     for data_type in self.dbs.keys():
    #         if data_type == "text":
    #             type_indices = {"semantic": SemanticIndex(dim=768, data_type=data_type)}
    #         elif data_type == "image":
    #             type_indices = {"semantic": SemanticIndex(dim=512, data_type=data_type)}
            
    #         indices[data_type] = type_indices
        
    #     return indices


    def load_models(self, model_names):
        models = {}
        for model_name in model_names:
            if model_name in TEXT_EMBEDDING_MODELS:
                print("Adding text embedding model")
                models["text"] = SentenceTransformer(model_name)
            elif model_name in IMAGE_EMBEDDING_MODELS:
                print("Adding image embedding model")
                models["image"] = SentenceTransformer(model_name)
            else:
                raise ValueError("Model name not supported.")
        
        return models
   
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
                data_type = input("Search images or texts? Type 'image' or 'text': ")
                input_text = input("Search text: ")
                results = self.semantic_search(data_type, input_text)
                print(results)

            else:
                print("Invalid instruction.")


    def insert(self, path):
        file_list = list_files(path)
        for file in file_list:
            file_path = file['path']
            suffix = file['suffix']
            data_type = file['type']
            db = self.dbs[data_type]
            # type_indices = self.indices[data_type]

            if file_path not in db.get_existing_file_paths(data_type):
                
                print("Processing file: ", file_path, suffix, self.models[data_type])
                
                data_list = process_file(file_path, suffix, self.models[data_type])
                inserted_ids = db.insert_data(data_list, data_type)
                # print(data_list)
                # print(inserted_ids)
                # for _, index in type_indices.items():
                #     index.insert_index(data_list, inserted_ids)


    # def delete(self, path):
    #     is_dir = os.path.isdir(path)
        
    #     remaining_embeddings, remaining_ids = self.db.delete_data(path, is_directory=is_dir)
    #     self.index.rebuild_index(remaining_embeddings, remaining_ids)
    #     self.bm25_index.rebuild_index(remaining_embeddings, remaining_ids)
    #     self.exact_macth_index.rebuild_index(remaining_embeddings, remaining_ids)


    def semantic_search(self, data_type, input_text):
        if data_type == "text":
            encode_func = encode_text
        else:
            encode_func = encode_image

        print(self.models[data_type], input_text)

        query_embedding = encode_func(self.models[data_type], input_text)

        print("query embed: ", type(query_embedding), query_embedding.shape)

        results = self.index["semantic"].search_index(query_embedding, data_type)
        return results



        # data_idxs, distances = self.indices[data_type]["semantic"].search_index(query_embedding)
        # column_names, results = self.dbs[data_type].retrieve_data(data_type, data_idxs)
        # if data_type == "text":
        #     return self._process_text_results(distances, column_names, results)
        # elif data_type == "image":
        #     return self._process_image_results(distances, column_names, results)
    

    def _process_text_results(self, distances, column_names, raw_results):
        dict_list = []
        for distance, raw_result in zip(distances, raw_results):
            d = {}
            d['distance'] = distance
            for column_name, result in zip(column_names, raw_result):
                d[column_name] = result
            
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

    def _process_image_results(self, distances, column_names, raw_results):

        combined_dict = {}
        for dist, raw_result in zip(distances, raw_results):
            for d, column_name in zip(raw_result, column_names):
                if column_name == "file_path":
                    combined_dict[d] = dist
        
        sorted_list = sorted(combined_dict.items(), key=lambda x: x[1])
        return sorted_list
    
    def close(self):
        for db in self.dbs.values():
            db.close()
        
        # for type_indices in self.indices.values():
        #     for index in type_indices.values():
        #         index.close()



if __name__ == "__main__":
    Anything = Anything()
    Anything.run()





