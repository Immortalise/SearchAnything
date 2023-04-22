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


def insert_index(index, line_list):

    embeddings = np.vstack([ np.frombuffer(line['embedding'], dtype=np.float32) for line in line_list])
    index.add(embeddings)
    faiss.write_index(index, INDEX_PATH)
    return index


def search_index(index, query_embedding, k=5):
    print(index.ntotal)
    distances, indices = index.search(query_embedding[np.newaxis, :], k)
    return indices, distances


