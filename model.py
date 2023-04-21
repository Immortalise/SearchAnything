from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config  
import torch  
  
class T5WithHiddenStates(T5ForConditionalGeneration):  
    def forward(self, *args, **kwargs):  
        outputs = super().forward(*args, **kwargs)  
        encoder_hidden_states = outputs.encoder_hidden_states  
        return outputs, encoder_hidden_states  


def create_model(model_name='google/flan-t5-large'):
    if model_name == 'google/flan-t5-large':
        tokenizer = T5Tokenizer.from_pretrained(model_name)  
        config = T5Config.from_pretrained(model_name, output_hidden_states=True)  
        model = T5WithHiddenStates.from_pretrained(model_name, config=config) 
    
    return tokenizer, model
  