import numpy as np
import faiss
import os
from rank_bm25 import BM25Okapi
import pickle
from transformers import AutoTokenizer

from config import INDEX_PATH, BM25_INDEX_PATH, DOCID_LIST_PATH, CONTENT_LIST_PATH


class SemanticIndex(object):
    def __init__(self, dim=1024):
        self.dim = dim
        if os.path.exists(INDEX_PATH):  
            self.index = faiss.read_index(INDEX_PATH)
        else:  
            index_flat_l2 = faiss.IndexFlatL2(dim)  
            self.index = faiss.IndexIDMap(index_flat_l2)


    def insert_index(self, line_list, inserted_ids):

        embeddings = np.vstack([line['embedding'] for line in line_list])
        inserted_ids_array = np.array(inserted_ids)  
        self.index.add_with_ids(embeddings, inserted_ids_array)  

        # to prevent potential collasping, we choose to save the index for each operation
        faiss.write_index(self.index, INDEX_PATH)


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
        faiss.write_index(self.index, INDEX_PATH)


    def close(self):
        faiss.write_index(self.index, INDEX_PATH)  



# =============================================================================
# Exact Match
class ExactMatchIndex():
    def __init__(self, data_base):
        if self.index_exists():
            self.load_index()
        else:
            full_data = data_base.retrieve_data_custom_query("SELECT id, content FROM file_data")
            self.docid_list = []
            self.content_list = []
            for doc in full_data[1]:
                docid, content = doc[0], doc[1]
                self.docid_list.append(docid)
                self.content_list.append(content.lower())
    
    def insert_index(self, line_list, inserted_ids, save_index=True):
        self.content_list = self.content_list + [doc['content'].lower() for doc in line_list]
        self.docid_list = self.docid_list + inserted_ids
        if save_index:
            self.save_index()
    
    def rebuild_index(self, line_list, inserted_ids, save_index=True):
        self.content_list = [doc['content'].lower() for doc in line_list]
        self.docid_list = inserted_ids
        if save_index:
            self.save_index()
    
    def search_index(self, query, k=50):
        indices = []
        query = query.lower()
        for idx, doc in enumerate(self.content_list):
            if query in doc:
                indices.append(self.docid_list[idx])
        return np.array(indices)[:k], np.zeros(len(indices))[:k]

    def save_index(self):
        with open(DOCID_LIST_PATH, "wb") as f:
            pickle.dump(self.docid_list, f)
        with open(CONTENT_LIST_PATH, "wb") as f:
            pickle.dump(self.content_list, f)

    def load_index(self):
        with open(DOCID_LIST_PATH, "rb") as f:
            self.docid_list = pickle.load(f)
        with open(CONTENT_LIST_PATH, "rb") as f:
            self.content_list = pickle.load(f)
    
    def index_exists(self):
        return os.path.exists(DOCID_LIST_PATH) and os.path.exists(CONTENT_LIST_PATH)
    
    def close(self):
        self.save_index()

# =============================================================================

# =============================================================================
# BM25 Search

class BM25Index(ExactMatchIndex):
    def __init__(self, data_base):
        super().__init__(data_base)
        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-multilingual-cased')
        if not self.index_exists():
            if len(self.content_list) == 0:
                self.bm25 = None
            else:
                self.bm25 = BM25Okapi([self.tokenizer.tokenize(content) for content in self.content_list])
        
        # https://github.com/dorianbrown/rank_bm25/issues/14
    
    def insert_index(self, line_list, inserted_ids, save_index=True):
        super().insert_index(line_list, inserted_ids, save_index=False)
        self.bm25 = BM25Okapi([self.tokenizer.tokenize(content) for content in self.content_list])
        if save_index:
            self.save_index()

    def rebuild_index(self, line_list, inserted_ids, save_index=True):
        super().rebuild_index(line_list, inserted_ids, save_index=False)
        self.bm25 = BM25Okapi([self.tokenizer.tokenize(content) for content in self.content_list])
        if save_index:
            self.save_index()

    def search_index(self, query, k=50):
        query = query.lower()
        doc_scores = -1 * self.bm25.get_scores(self.tokenizer.tokenize(query))
        sorted_indices = np.argsort(doc_scores)
        return np.array(self.docid_list)[sorted_indices][:k], np.array(doc_scores)[sorted_indices][:k]

    def save_index(self):
        super().save_index()
        with open(BM25_INDEX_PATH, "wb") as f:
            pickle.dump(self.bm25, f)

    def load_index(self):
        super().load_index()
        with open(BM25_INDEX_PATH, "rb") as f:
            self.bm25 = pickle.load(f)
    
    def index_exists(self):
        return os.path.exists(DOCID_LIST_PATH) and os.path.exists(CONTENT_LIST_PATH) and os.path.exists(BM25_INDEX_PATH)

# =============================================================================