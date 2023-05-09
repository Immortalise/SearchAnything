# from utils import *
# import sys 
# import time
# from watchdog.observers import Observer

# import faiss
# import numpy as np
# xb = np.random.random((10, 128)).astype('float32')
# index = faiss.IndexFlatL2(xb.shape[1]) 
# ids = np.arange(xb.shape[0])
# # index.add_with_ids(xb, ids)  # this will crash, because IndexFlatL2 does not support add_with_ids
# index2 = faiss.IndexIDMap(index)
# index2.add_with_ids(xb, ids) # works, the vectors are stored in the underlying index

# def _process_output(distances, columns, raw_results):
#     dict_list = []
#     for distance, raw_result in zip(distances, raw_results):
#         d = {}
#         d['distance'] = distance
#         for column, result in zip(columns, raw_result):
#             d[column] = result
        
#         dict_list.append(d)
    
#     combined_dict = {}  

#     for d in dict_list:  
#         file_path = d["file_path"]  

#         if file_path not in combined_dict:  
#             combined_dict[file_path] = {  
#                 "content": [],  
#                 "distance": float('inf'),  
#                 "page": [],  
#             }  

#         combined_dict[file_path]["distance"] = min(combined_dict[file_path]["distance"], d["distance"])
#         combined_dict[file_path]["content"].append(d["content"])  
#         combined_dict[file_path]["page"].append(d["page"])  

#     sorted_list = sorted(combined_dict.items(), key=lambda x: x[1]["distance"])  

#     return sorted_list 
  
# # 示例输入数据  
# distances = [0.5, 0.2, 0.8, 0.3]  
# columns = ["file_path", "content", "page"]  
# raw_results = [  
#     ["file1.txt", "内容1", 1],  
#     ["file2.txt", "内容2", 2],  
#     ["file3.txt", "内容3", 1],  
#     ["file4.txt", "内容4", 3],  
# ]  
  
# # 调用函数  
# result = _process_output(distances, columns, raw_results)  
# print(result) 

import easyocr
reader = easyocr.Reader(['ch_sim','en'])

result = reader.readtext('test1.png', detail=0)
print(result)