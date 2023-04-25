import numpy as np
import faiss
import os

from config import INDEX_PATH


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


    def search_index(self, query_embedding, k=5):
        distances, indices = self.index.search(query_embedding[np.newaxis, :], k)
        return indices, distances

  
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
