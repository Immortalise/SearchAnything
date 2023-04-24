import torch
import os  


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
    
    # Access specific hidden states, e.g., last layer's hidden state  
    last_layer_hidden_state = encoder_hidden_states[-1]
    embedding = torch.sum(last_layer_hidden_state.squeeze(0), dim=0).detach().numpy()
    
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