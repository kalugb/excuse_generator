import torch
from transformers import AutoTokenizer

print(torch.version.cuda)
print(torch.cuda.is_available())

device = "cuda" if torch.cuda.is_available() else "cpu"

x = torch.randn(1000, 1000, device=device, dtype=torch.float16)
y = torch.randn(1000, 1000, device=device, dtype=torch.float16)
z = x @ y
print(z.device)