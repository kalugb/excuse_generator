import numpy as np

import os

import torch
from torch.utils.data import TensorDataset, DataLoader
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import get_peft_model, LoraConfig

from get_dataset import get_formatted_dataset

# change the login secret code to your own
from huggingface_hub import login
login("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")

# define using models
model_name = "google/gemma-3-1b-it"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")

# lora config to make training lighter and faster
lora_config = LoraConfig(
    r=8,    
    target_modules=["q_proj", "v_proj", "o_proj"],
    lora_alpha=16,
    lora_dropout=0.2,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config).to(device)

tokenizer_params = {
    "max_length": 64,
    "padding": True,
    "return_tensors": "pt",
    "truncation": True
}

# get train and val data
data = get_formatted_dataset()
total_data = len(data)
total_train_data = int(total_data * 0.9)
train_data = data[:total_train_data] 
val_data = data[total_train_data:]

# tokenize and dataloader 
inputs = tokenizer(train_data, **tokenizer_params)
input_ids = inputs["input_ids"].to(device)
attention_mask = inputs["attention_mask"].to(device)
dataset = TensorDataset(input_ids, attention_mask, input_ids)
dataloader = DataLoader(dataset, batch_size=16, shuffle=True)

# parameters
lr = 5e-4
weight_decay = 0.05
optim = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
epochs = 5

# train
model.train()
for epoch in range(epochs):
    print(f"At epoch {epoch + 1}")
    total_loss = 0
    for input_ids, attention_mask, _ in dataloader:
        optim.zero_grad()
        
        output = model(
            input_ids=input_ids, 
            attention_mask=attention_mask, 
            labels=input_ids
        )
        loss = output.loss
            
        loss.backward()
        optim.step()
            
        total_loss += loss.item()
        
    print(f"Epoch loss: {total_loss / len(dataloader)}")
    
# validation
model.eval()
val_enc = tokenizer(val_data, **tokenizer_params)
val_input_ids = val_enc["input_ids"].to(device)
val_attention_mask = val_enc["attention_mask"].to(device)

val_dataset = TensorDataset(val_input_ids, val_attention_mask, val_input_ids)
val_dataloader = DataLoader(val_dataset, batch_size=16, shuffle=False)

with torch.inference_mode():
    total_loss = 0
    for input_ids, attention_mask, _ in val_dataloader:           
        output = model(
            input_ids=input_ids, 
            attention_mask=attention_mask, 
            labels=input_ids
        )
        
        total_loss += output.loss.item()
        
    val_loss = total_loss / len(val_dataloader)
    print(f"Validation loss: {val_loss}")
        
# save model
model_config_path = os.path.join(os.getcwd(), "model_config")
model.save_pretrained(model_config_path)
tokenizer.save_pretrained(model_config_path)
