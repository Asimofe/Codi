import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(load_in_8bit=True)

checkpoint = "Dang-gu/finetune_starcoder2"
device = "cuda"

# 모델과 토크나이저 로딩
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForCausalLM.from_pretrained(checkpoint, device_map="auto", quantization_config=quantization_config)

def generate_code(prompt: str, max_new_tokens: int = 256) -> str:
    inputs = tokenizer.encode(prompt, return_tensors="pt").to(device)
    outputs = model.generate(inputs, max_new_tokens=max_new_tokens)

    # eos_token_id = tokenizer.eos_token_id

    # outputs = model.generate(
    #     inputs, 
    #     max_new_tokens=256,
    #     eos_token_id=eos_token_id,  # Stop generation when EOS token is encountered
    #     early_stopping=True  # Optional: stop as soon as the model is confident enough
    # )

    generated_code = tokenizer.decode(outputs[0])

    # 코드 종료를 나타내는 구문에서 잘라내기
    #end_tokens = ["\n\n", "\n\n\n", "\n\n\n\n", "# End of code", "# End", "if __name__ == '__main__':"]
    #for end_token in end_tokens:
    #    if end_token in generated_code:
    #        generated_code = generated_code.split(end_token)[0] + end_token
    #        break

    return generated_code

def get_memory_footprint() -> float:
    return model.get_memory_footprint() / 1e6  # MB

