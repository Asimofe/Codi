import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

checkpoint = "Leecm/finetune_starcoder2"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
device = "cuda"

# for fp16 use `torch_dtype=torch.float16` instead
model = AutoModelForCausalLM.from_pretrained(checkpoint, device_map="auto", torch_dtype=torch.float16)

code_to_debug = "def access_element(list, index):\n    return list[index]\nmy_list = [1, 2, 3]\nprint(access_element(my_list, 5))"

prompt = (
            "Here is a Python function with an error:\n\n"
            f"{code_to_debug}\n\n"
            "Fix the above code and provide the corrected version within the following markers:\n"
        )
#f"Here is a Python function with an error:\n\n{code_to_debug}\n\nFix the code."
inputs = tokenizer.encode(prompt, return_tensors="pt").to(device)
outputs = model.generate(inputs, max_new_tokens=256)
print(tokenizer.decode(outputs[0]))
# Using eos_token_id to stop generation when encountering the end-of-sequence token


# generated_code = tokenizer.decode(outputs[0], skip_special_tokens=True)


# print(generated_code)


# eos_token_id = tokenizer.eos_token_id

# outputs = model.generate(
#     inputs, 
#     max_new_tokens=256,
#     eos_token_id=eos_token_id,  # Stop generation when EOS token is encountered
#     early_stopping=True  # Optional: stop as soon as the model is confident enough
# )