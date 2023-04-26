import torch
import os


# def get_directory_state(path):  
#     directory_state = {}  
#     for root, dirs, files in os.walk(path):  
#         for file_name in files:  
#             file_path = os.path.join(root, file_name)  
#             directory_state[file_path] = os.path.getmtime(file_path)  
        
#         for dir_name in dirs:  
#             dir_path = os.path.join(root, dir_name)  
#             directory_state[dir_path] = os.path.getmtime(dir_path)

#     return directory_state  

  
# def compare_directory_states(old_state, new_state):  
#     added_items = set(new_state.keys()) - set(old_state.keys())  
#     deleted_items = set(old_state.keys()) - set(new_state.keys())  
#     modified_items = {item for item in new_state if item in old_state and new_state[item] != old_state[item]}  
  
#     def filter_items(items):  
#         filtered_items = set()  
#         for item in items:  
#             parent_dir = os.path.dirname(item)  
#             if parent_dir not in items:  
#                 filtered_items.add(item)  
#         return filtered_items  
  
#     filtered_added_items = filter_items(added_items)  
#     filtered_deleted_items = filter_items(deleted_items)  
#     filtered_modified_items = filter_items(modified_items)  
  
#     return filtered_added_items, filtered_deleted_items, filtered_modified_items  


def filter_subdirectories(directories):  
    filtered_dirs = set()  
  
    for dir1 in directories:  
        is_subdir = False  
        for dir2 in directories:  
            if dir1 != dir2 and os.path.commonpath([dir1, dir2]) == dir2:  
                is_subdir = True  
                break  
        if not is_subdir:  
            filtered_dirs.add(dir1)  
  
    return filtered_dirs  
  

def list_files_with_type(root_path):  
    result = []  
  
    if os.path.isfile(root_path):  
        file_type = os.path.splitext(root_path)[1][1:]  
        result.append({"path": root_path, "type": file_type})  
        return result  
  
    for dirpath, _, filenames in os.walk(root_path):  
        for filename in filenames:  
            filepath = os.path.join(dirpath, filename)  
            file_type = os.path.splitext(filepath)[1][1:]  
            file_info = {"path": filepath, "type": file_type}  
            result.append(file_info)  
  
    return result


def encode_text(tokenizer, model, input_text):

    input_ids = tokenizer.encode(input_text, return_tensors='pt')
  
    # Get hidden states from the model
    with torch.no_grad():
        _, encoder_hidden_states = model(input_ids=input_ids, decoder_input_ids=input_ids)


    last_layer_hidden_state = encoder_hidden_states[-1]

    # # Method 1. Sum up the last layer's hidden states and then normalize the result
    # embedding = torch.sum(last_layer_hidden_state.squeeze(0), dim=0)  

    # Method 2. select the last token's hidden state as the embedding)
    embedding = last_layer_hidden_state[-1][-1]


    embedding_l2 = torch.norm(embedding, p=2).detach().numpy()  
    embedding = embedding.detach().numpy()  
    embedding = embedding / embedding_l2  # Store the result in the 'embedding' variable  
    return embedding 


def summarize_text(tokenizer, model, input_text):

    prompts = "Summarize: "

    input_text = prompts + input_text

    input_ids = tokenizer.encode(input_text, return_tensors='pt')
  
    # Get hidden states from the model
    outputs, _ = model(input_ids=input_ids, decoder_input_ids=input_ids)
    outputs = model.generate(input_ids, max_length=20, early_stopping=True)
    outputs = tokenizer.decode(outputs[0])
    
    return outputs