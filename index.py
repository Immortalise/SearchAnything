import numpy as np
import faiss
import os

from config import INDEX_PATH


def init_index(dim=1024):
    if os.path.exists(INDEX_PATH):
        index = faiss.read_index(INDEX_PATH)    
    else:
        index = faiss.IndexFlatL2(dim)
        faiss.write_index(index, INDEX_PATH)

    return index


def add_index(index, embedding_matrix):
    index.add(embedding_matrix)
    faiss.write_index(index, INDEX_PATH)
    return index


def search_index(index, query_embedding, k=5):
    distances, indices = index.search(query_embedding[np.newaxis, :], k)
    return indices, distances


