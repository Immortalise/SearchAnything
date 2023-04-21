import torch

def encode_text(tokenizer, model, input_text):

    input_ids = tokenizer.encode(input_text, return_tensors='pt')
  
    # Get hidden states from the model
    outputs, encoder_hidden_states = model(input_ids=input_ids, decoder_input_ids=input_ids)
    
    # Access specific hidden states, e.g., last layer's hidden state  
    last_layer_hidden_state = encoder_hidden_states[-1]
    embedding = torch.sum(last_layer_hidden_state.squeeze(0), dim=0)
    
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