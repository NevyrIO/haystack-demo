# preloads transformer models for quicker app start

from transformers import (
    T5Tokenizer, 
    T5ForConditionalGeneration
)

def load_text_model(model_name):
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    return model, tokenizer

load_text_model("google/flan-t5-small")
