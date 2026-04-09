import torch
device = "cuda" if torch.cuda.is_available() else "cpu"

import os
import sys
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pathlib import Path

# load model
def load_model():
    from transformers import AutoTokenizer, AutoModelForCausalLM
    
    script_dir = Path(__file__).parent.absolute()
    model_config_path = str((script_dir.parent / "model_config").as_posix())
    tokenizer = AutoTokenizer.from_pretrained(model_config_path, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(model_config_path, local_files_only=True).to(device)
    
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
        max_new_tokens=60,
        do_sample=True,
        temperature=0.7,
        top_p=0.95,
        pad_token_id=tokenizer.pad_token_id,
        repetition_penalty=1.1
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
    data = json.load(sys.stdin)
    
    output_list = []
    
    for _ in range(3):
        output = get_excuse(data["situation"], data["context"], data["seriousness"], data["length"])
        output_list.append(output)
        
    print(json.dumps(output_list))

        
    