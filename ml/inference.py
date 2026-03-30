import torch
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

model, tokenizer = None, None

# load model
def load_model():
    from transformers import AutoTokenizer, AutoModelForCausalLM
    model_config_path = os.path.join(os.getcwd(), "model_config")
    tokenizer = AutoTokenizer.from_pretrained(model_config_path)
    model = AutoModelForCausalLM.from_pretrained(model_config_path, device_map="auto")
    
    return tokenizer, model

# inference
def get_excuse(input_text: str, context: str, seriousness: bool, length: str):
    # format input 
    context = context + " excused needed: "
    text = "input: " + context + input_text + "\nserious: " + str(seriousness) + "\nlength: " + length
    
    tokenizer, model = load_model()
    tokenizer_params = {"padding": True, "truncation": True, "return_tensors": "pt", "batch_size": 16}
    
    # encoding 
    enc = tokenizer(text, **tokenizer_params)
    input_ids = enc["input_ids"].to(device)
    attention_mask = enc["attention_mask"].to(device)
    
    # this is needed i guess
    tokenizer.pad_token = tokenizer.eos_token
    model.config.pad_token_id = model.config.eos_token_id
    
    full_output = model.generate(
        input_ids=input_ids, 
        attention_mask=attention_mask, 
        max_new_tokens=50
    )
    
    # format output into readable string
    full_output = tokenizer.decode(full_output[0], skip_special_tokens=True)
    output = full_output.splitlines()[3]
    output = output.split("output: ")[1]
    
    return output

if __name__ == "__main__":
    output = get_excuse("I was late for my work", "Corporate", False, "short")
    
    print(output)
    