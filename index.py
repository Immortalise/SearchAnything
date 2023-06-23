import numpy as np
import faiss
import os
from rank_bm25 import BM25Okapi
import pickle
from transformers import AutoTokenizer

from config import INDEX_PATH, BM25_INDEX_PATH, DOCID_LIST_PATH, CONTENT_LIST_PATH


class SemanticIndex(object):
    def __init__(self, dim=1024, data_type=None):
        self.dim = dim
        self.data_type = data_type
        self.index_path = INDEX_PATH[self.data_type]["semantic"]

        if os.path.exists(self.index_path):  
            self.index = faiss.read_index(self.index_path)
        else:  
            index_flat_l2 = faiss.IndexFlatL2(dim)  
            self.index = faiss.IndexIDMap(index_flat_l2)


    def insert_index(self, data_list, inserted_ids):

        embeddings = np.vstack([line['embedding'] for line in data_list])
        inserted_ids_array = np.array(inserted_ids)  
        self.index.add_with_ids(embeddings, inserted_ids_array)  

        # to prevent potential collasping, we choose to save the index for each operation
        faiss.write_index(self.index, self.index_path)


    def search_index(self, query_embedding, k=50):
        distances, indices = self.index.search(query_embedding[np.newaxis, :], k)
        return indices[0], distances[0]

  
    def rebuild_index(self, line_list, inserted_ids):
        # for faiss repo, removing index is not supported
        # so we need to rebuild the index

        index_flat_l2 = faiss.IndexFlatL2(self.dim)  
        self.index = faiss.IndexIDMap(index_flat_l2)
        self.insert_index(line_list, inserted_ids)

        # to prevent potential collasping, we choose to save the index for each operation
        faiss.write_index(self.index, self.index_path)


    def close(self):
        faiss.write_index(self.index, self.index_path)