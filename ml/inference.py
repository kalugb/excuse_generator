import torch
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# load model
def load_model():
    from transformers import AutoTokenizer, AutoModelForCausalLM
    model_config_path = os.path.join(os.getcwd(), "model_config")
    tokenizer = AutoTokenizer.from_pretrained(model_config_path)
    model = AutoModelForCausalLM.from_pretrained(model_config_path, device_map=None).to(device)
    
    return model, tokenizer

model, tokenizer = load_model()

# inference
def get_excuse(input_text: str, context: str, seriousness: bool, length: str):
    # format input 
    text = (
        f"input: {input_text}\n"
        f"context: {context}\n"
        f"serious: {str(seriousness)}\n"
        f"length: {length}\n"
    )
    
    tokenizer_params = {"padding": True, "truncation": True, "return_tensors": "pt"}
    
    # encoding 
    enc = tokenizer(text, **tokenizer_params)
    input_ids = enc["input_ids"].to(device)
    attention_mask = enc["attention_mask"].to(device)
    
    full_output = model.generate(
        input_ids=input_ids, 
        attention_mask=attention_mask, 
        max_new_tokens=40,
        do_sample=True,
        temperature=0.9,
        top_p=0.9,
        pad_token_id=tokenizer.pad_token_id
    )
    
    # format output into readable string
    full_output = tokenizer.decode(full_output[0], skip_special_tokens=True)
    full_output = full_output.splitlines()
    
    output = ""
    for out in full_output:
        if "output" in out:
            output = out.split("output: ")[1]
            break
    
    return output

if __name__ == "__main__":
    output_num = 3
    
    input_text = "Late for government meeting"
    context = "government"
    seriousness = True
    length = "long"
    
    for i in range(output_num):
        output = get_excuse(input_text, context, seriousness, length)
        print(f"Excuse {i + 1}: {output}")
        
    