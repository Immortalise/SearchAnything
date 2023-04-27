import torch   


def create_model(model_name='google/flan-t5-large'):
    if model_name == 'google/flan-t5-large':
        from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config  
        class T5WithHiddenStates(T5ForConditionalGeneration):  
            def forward(self, *args, **kwargs):  
                outputs = super().forward(*args, **kwargs)  
                encoder_hidden_states = outputs.encoder_hidden_states  
                return outputs, encoder_hidden_states 

        tokenizer = T5Tokenizer.from_pretrained(model_name)  
        config = T5Config.from_pretrained(model_name, output_hidden_states=True)  
        model = T5WithHiddenStates.from_pretrained(model_name, config=config) 
        
    elif model_name == 'sentence-transformers/all-mpnet-base-v2':
        from sentence_transformers import SentenceTransformer

        tokenizer = None
        model = SentenceTransformer(model_name)

    
    return tokenizer, model
  