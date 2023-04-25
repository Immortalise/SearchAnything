from utils import *
import sys 
import time
from watchdog.observers import Observer

import faiss
import numpy as np
xb = np.random.random((10, 128)).astype('float32')
index = faiss.IndexFlatL2(xb.shape[1]) 
ids = np.arange(xb.shape[0])
# index.add_with_ids(xb, ids)  # this will crash, because IndexFlatL2 does not support add_with_ids
index2 = faiss.IndexIDMap(index)
index2.add_with_ids(xb, ids) # works, the vectors are stored in the underlying index