import numpy as np
import faiss
import os

from config import INDEX_PATH, BM25_INDEX_PATH, DOCID_LIST_PATH, CONTENT_LIST_PATH


from rank_bm25 import BM25Okapi
import numpy as np

import pickle

from transformers import AutoTokenizer

class Index(object):
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


import unittest  
import numpy as np  
import os  
  
class TestIndexClass(unittest.TestCase):  
  
    # def test_insert_index(self):  
    #     dim = 1024  
    #     index_obj = Index(dim=dim)  
    #     line_list = [  
    #         {'embedding': np.random.random(dim).astype('float32')},  
    #         {'embedding': np.random.random(dim).astype('float32')},  
    #     ]  
    #     inserted_ids = [1, 2]  
    #     index_obj.insert_index(line_list, inserted_ids)  
    #     self.assertEqual(index_obj.index.ntotal, 2)  
    
    # def test_search_index(self):  
    #     dim = 1024  
    #     index_obj = Index(dim=dim)  
    #     query_embedding = np.random.random(dim).astype('float32')  
    #     indices, distances = index_obj.search_index(query_embedding, k=1)  
    #     self.assertEqual(len(indices[0]), 1)  
    #     self.assertEqual(len(distances[0]), 1)  
    
    def test_remove_index(self):  
        dim = 1024  
        index_obj = Index(dim=dim)  
        line_list = [  
            {'embedding': np.random.random(dim).astype('float32')},  
            {'embedding': np.random.random(dim).astype('float32')},  
        ]  
        inserted_ids = [1, 2]  
        index_obj.insert_index(line_list, inserted_ids)  
    
        index_obj.remove_index([1])  
        self.assertEqual(index_obj.index.ntotal, 1)  
  
    # def test_close(self):  
    #     index_obj = Index()  
    #     index_obj.close()  
    #     self.assertTrue(os.path.exists(INDEX_PATH))  
  
if __name__ == "__main__":  
    INDEX_PATH = "test_index.index"  
    unittest.main()  
  
    # Clean up the test index file  
    if os.path.exists(INDEX_PATH):  
        os.remove(INDEX_PATH)  



# =============================================================================
# Exact Match
def kmp_search(query, corpus):
    n = len(query)
    m = len(corpus)
    lps = [0] * n
    j = 0
    matches = []
    compute_lps(query, n, lps)
    i = 0
    while i < m:
        if query[j] == corpus[i]:
            i += 1
            j += 1
        if j == n:
            matches.append(i-j)
            j = lps[j-1]
        elif i < m and query[j] != corpus[i]:
            if j != 0:
                j = lps[j-1]
            else:
                i += 1
    return matches

def compute_lps(query, n, lps):
    len = 0
    lps[0] = 0
    i = 1
    while i < n:
        if query[i] == query[len]:
            len += 1
            lps[i] = len
            i += 1
        else:
            if len != 0:
                len = lps[len-1]
            else:
                lps[i] = 0
                i += 1

class ExactMatchIndex():
    def __init__(self, data_base):
        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-multilingual-cased')
        if self.index_exists():
            self.load_index()
        else:
            full_data = data_base.retrieve_data_custom_query("SELECT * FROM file_data")
            self.docid_list = []
            self.content_list = []
            # id: 0, title: 1, file_path: 2, page: 3, author: 4, subject: 5, content: 6
            for doc in full_data[1]:
                docid, content = doc[0], doc[6]
                self.docid_list.append(docid)
                self.content_list.append(content)

    def insert_index(self, line_list, inserted_ids):
        self.content_list = self.content_list + [doc['content'] for doc in line_list]
        self.docid_list = self.docid_list + inserted_ids
    
    def rebuild_index(self, line_list, inserted_ids):
        self.content_list = [doc['content'] for doc in line_list]
        self.docid_list = inserted_ids
    
    def search_index(self, query, k=50):
        indices = []
        for idx, doc in enumerate(self.content_list):
            doc_matches = kmp_search(query, doc)
            if len(doc_matches) > 0:
                indices.append(self.docid_list[idx])
        return np.array(self.docid_list)[indices][:k], np.zeros(len(indices))[:k]

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
        if not self.index_exists():
            self.bm25 = BM25Okapi([self.tokenizer.tokenize(content) for content in self.content_list])
        
        # https://github.com/dorianbrown/rank_bm25/issues/14
    
    def insert_index(self, line_list, inserted_ids):
        super().insert_index(line_list, inserted_ids)
        self.bm25 = BM25Okapi([self.tokenizer.tokenize(content) for content in self.content_list])

    def rebuild_index(self, line_list, inserted_ids):
        super().rebuild_index(line_list, inserted_ids)
        self.bm25 = BM25Okapi([self.tokenizer.tokenize(content) for content in self.content_list])
        self.save_index()

    def search_index(self, query, k=50):
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