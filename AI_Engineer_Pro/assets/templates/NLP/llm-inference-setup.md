# LLM Inference Optimization

Guide for fast, efficient LLM inference in production.

## vLLM (Fastest for LLaMA, Mistral, etc.)

```bash
pip install vllm
```

```python
from vllm import LLM, SamplingParams

# Initialize model
llm = LLM(
    model="meta-llama/Llama-2-7b-chat-hf",
    tensor_parallel_size=1,  # Number of GPUs
    dtype="float16",         # or "bfloat16"
    max_model_len=4096,
)

# Sampling parameters
sampling_params = SamplingParams(
    temperature=0.7,
    top_p=0.9,
    max_tokens=512,
)

# Batch inference (very fast)
prompts = [
    "Explain PCB defect detection:",
    "What causes solder bridges?",
]

outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    print(f"Prompt: {output.prompt}")
    print(f"Generated: {output.outputs[0].text}")
```

## Transformer with Optimizations

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "mistralai/Mistral-7B-Instruct-v0.2"

# Load with optimizations
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,      # FP16
    device_map="auto",              # Auto GPU allocation
    load_in_8bit=False,             # 8-bit quantization
    load_in_4bit=True,              # 4-bit quantization (QLoRA)
)

tokenizer = AutoTokenizer.from_pretrained(model_name)

# Generate
def generate_text(prompt, max_new_tokens=256):
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    
    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Usage
response = generate_text("Explain PCB inspection:")
print(response)
```

## ONNX Runtime (Cross-platform)

```bash
pip install optimum[onnxruntime-gpu]
```

```python
from optimum.onnxruntime import ORTModelForCausalLM
from transformers import AutoTokenizer

# Export to ONNX (one-time)
model = ORTModelForCausalLM.from_pretrained(
    "gpt2",
    export=True,
    provider="CUDAExecutionProvider"  # or "CPUExecutionProvider"
)

tokenizer = AutoTokenizer.from_pretrained("gpt2")

# Inference
inputs = tokenizer("Hello, my name is", return_tensors="pt")
outputs = model.generate(**inputs, max_length=50)
print(tokenizer.decode(outputs[0]))

# Save ONNX model
model.save_pretrained("./gpt2_onnx")
```

## Text Generation Inference (TGI) Server

```bash
# Run TGI server
docker run --gpus all --shm-size 1g -p 8080:80 \
  -v $PWD/data:/data \
  ghcr.io/huggingface/text-generation-inference:latest \
  --model-id meta-llama/Llama-2-7b-chat-hf \
  --num-shard 1
```

```python
# Client code
import requests

API_URL = "http://localhost:8080/generate"

def query(prompt):
    response = requests.post(
        API_URL,
        json={
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 256,
                "temperature": 0.7,
                "top_p": 0.9
            }
        }
    )
    return response.json()["generated_text"]

# Usage
result = query("Explain PCB defects:")
print(result)
```

## Streaming Responses

```python
from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer
from threading import Thread

model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def stream_generate(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    
    streamer = TextIteratorStreamer(tokenizer, skip_special_tokens=True)
    
    generation_kwargs = dict(
        inputs,
        streamer=streamer,
        max_new_tokens=256,
        temperature=0.7
    )
    
    thread = Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()
    
    generated_text = ""
    for new_text in streamer:
        generated_text += new_text
        print(new_text, end="", flush=True)
    
    thread.join()
    return generated_text

# Usage
stream_generate("Once upon a time")
```

## Batch Processing

```python
from transformers import pipeline

# Create pipeline
generator = pipeline(
    "text-generation",
    model="gpt2",
    device=0,
    batch_size=8  # Process 8 at once
)

# Batch inference
prompts = [f"Prompt {i}" for i in range(100)]

results = generator(
    prompts,
    max_length=50,
    do_sample=True,
    temperature=0.7
)

for i, result in enumerate(results):
    print(f"{i}: {result[0]['generated_text']}")
```

## Quantization for Smaller Models

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

# Load quantized model
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    quantization_config=bnb_config,
    device_map="auto"
)

# Model now uses ~4GB VRAM instead of ~14GB!
```

## Performance Comparison

| Method | Speed | Memory | Setup Complexity |
|--------|-------|--------|------------------|
| vLLM | ★★★★★ | Medium | Easy |
| TGI | ★★★★★ | Medium | Medium |
| Transformers FP16 | ★★★ | High | Easy |
| ONNX Runtime | ★★★★ | Low | Medium |
| 4-bit Quantization | ★★★ | Very Low | Easy |

**Recommendation**: Use **vLLM** for production LLM serving.
