import numpy as np
import faiss
import os
from rank_bm25 import BM25Okapi
import pickle
from transformers import AutoTokenizer
import sqlite3
import numpy as np
import torch
from sentence_transformers import util

from config import INDEX_PATH, BM25_INDEX_PATH, DOCID_LIST_PATH, CONTENT_LIST_PATH


class SemanticIndex():
    def __init__(self, db_path):
        self.db_path = db_path
        
    def search_index(self, query_embedding, data_type):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        if data_type == "text":
            cur.execute(f'SELECT id, file_path, content, embedding FROM {data_type}_data ORDER BY id')
            results = cur.fetchall()

            data = {}
            embeddings = []

            for res in results:
                id, file_path, content, embedding = res
                embedding_np = np.frombuffer(embedding, dtype=np.float32)
                embeddings.append(embedding_np)
                data[(id, file_path, content)] = embedding_np

            embeddings_np = np.vstack(embeddings)
            img_emb = torch.from_numpy(embeddings_np)
            
            from sentence_transformers import util
            cos_scores = util.cos_sim(query_embedding, img_emb)
            
            cos_scores = cos_scores.numpy().flatten()
            path_score_pairs = [(path, content, score) for ((id, path, content), score) in zip(data.keys(), cos_scores)]
            
            path_score_pairs.sort(key=lambda x: x[2], reverse=True)

            return path_score_pairs

        elif data_type == "image":
            cur.execute(f'SELECT id, file_path, embedding FROM {data_type}_data ORDER BY id')
            results = cur.fetchall()

            data = {}
            embeddings = []

            for res in results:
                id, file_path, embedding = res
                embedding_np = np.frombuffer(embedding, dtype=np.float32)
                embeddings.append(embedding_np)
                data[(id, file_path)] = embedding_np

            embeddings_np = np.vstack(embeddings)
            img_emb = torch.from_numpy(embeddings_np)
            
            from sentence_transformers import util
            cos_scores = util.cos_sim(query_embedding, img_emb)
            
            cos_scores = cos_scores.numpy().flatten()
            path_score_pairs = [(path, score) for ((id, path), score) in zip(data.keys(), cos_scores)]
            
            path_score_pairs.sort(key=lambda x: x[1], reverse=True)

            return path_score_pairs


    def close(self):
        pass


# class SemanticIndex(object):
#     def __init__(self, dim=1024, data_type=None):
#         self.dim = dim
#         self.data_type = data_type
#         self.index_path = INDEX_PATH[self.data_type]["semantic"]

#         if os.path.exists(self.index_path):  
#             self.index = faiss.read_index(self.index_path)
#         else:  
#             index_flat_l2 = faiss.IndexFlatL2(dim)  
#             self.index = faiss.IndexIDMap(index_flat_l2)


#     def insert_index(self, data_list, inserted_ids):

#         embeddings = np.vstack([data['embedding'] for data in data_list])
#         inserted_ids_array = np.array(inserted_ids)  
#         self.index.add_with_ids(embeddings, inserted_ids_array)  

#         # to prevent potential collasping, we choose to save the index for each operation
#         faiss.write_index(self.index, self.index_path)


#     def search_index(self, query_embedding, k=50):
#         distances, indices = self.index.search(query_embedding[np.newaxis, :], k)
#         return indices[0], distances[0]

  
#     def rebuild_index(self, line_list, inserted_ids):
#         # for faiss repo, removing index is not supported
#         # so we need to rebuild the index

#         index_flat_l2 = faiss.IndexFlatL2(self.dim)  
#         self.index = faiss.IndexIDMap(index_flat_l2)
#         self.insert_index(line_list, inserted_ids)

#         # to prevent potential collasping, we choose to save the index for each operation
#         faiss.write_index(self.index, self.index_path)


#     def close(self):
#         faiss.write_index(self.index, self.index_path)