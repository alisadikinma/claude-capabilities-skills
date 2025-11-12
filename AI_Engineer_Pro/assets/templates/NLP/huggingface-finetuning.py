"""
HuggingFace Model Fine-tuning
Complete script for fine-tuning transformers on custom data
"""

from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification,
    Trainer, 
    TrainingArguments,
    DataCollatorWithPadding
)
from datasets import load_dataset, Dataset
import torch
import numpy as np
from sklearn.metrics import accuracy_score, f1_score

# 1. Load and Prepare Data
def prepare_dataset(train_texts, train_labels, val_texts, val_labels):
    """Convert lists to HuggingFace Dataset"""
    train_data = {"text": train_texts, "label": train_labels}
    val_data = {"text": val_texts, "label": val_labels}
    
    train_dataset = Dataset.from_dict(train_data)
    val_dataset = Dataset.from_dict(val_data)
    
    return train_dataset, val_dataset

# 2. Tokenization
model_name = "bert-base-uncased"  # or "distilbert-base-uncased", "roberta-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)

def tokenize_function(examples):
    return tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
        max_length=512
    )

# Apply tokenization
tokenized_train = train_dataset.map(tokenize_function, batched=True)
tokenized_val = val_dataset.map(tokenize_function, batched=True)

# 3. Load Model
num_labels = 3  # Change to your number of classes
model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=num_labels
)

# 4. Training Arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
    load_best_model_at_end=True,
    metric_for_best_model="f1",
    push_to_hub=False,
    logging_dir='./logs',
    logging_steps=100,
    warmup_steps=500,
    fp16=True,  # Mixed precision training
)

# 5. Metrics
def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    
    accuracy = accuracy_score(labels, predictions)
    f1 = f1_score(labels, predictions, average='weighted')
    
    return {"accuracy": accuracy, "f1": f1}

# 6. Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_val,
    tokenizer=tokenizer,
    data_collator=DataCollatorWithPadding(tokenizer=tokenizer),
    compute_metrics=compute_metrics,
)

# 7. Train
trainer.train()

# 8. Evaluate
metrics = trainer.evaluate()
print(f"Validation Metrics: {metrics}")

# 9. Save Model
trainer.save_model("./fine_tuned_model")
tokenizer.save_pretrained("./fine_tuned_model")

# 10. Inference
from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="./fine_tuned_model",
    tokenizer=tokenizer,
    device=0 if torch.cuda.is_available() else -1
)

# Predict
texts = ["This component is defective", "Quality looks good"]
results = classifier(texts)
print(results)

# ========================================
# LoRA Fine-tuning (Parameter-Efficient)
# ========================================

from peft import LoraConfig, get_peft_model, TaskType

# LoRA configuration
lora_config = LoraConfig(
    task_type=TaskType.SEQ_CLS,
    r=16,  # Rank
    lora_alpha=32,
    lora_dropout=0.1,
    target_modules=["query", "value"]  # Which layers to apply LoRA
)

# Apply LoRA to model
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
model = get_peft_model(model, lora_config)

# Print trainable parameters
model.print_trainable_parameters()

# Train with LoRA (same Trainer as above)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_val,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

trainer.train()

# Save LoRA weights (much smaller than full model)
model.save_pretrained("./lora_model")

# ========================================
# For Text Generation (GPT, LLaMA)
# ========================================

from transformers import AutoModelForCausalLM, AutoTokenizer

# Load base model
base_model = "gpt2"  # or "meta-llama/Llama-2-7b-hf"
tokenizer = AutoTokenizer.from_pretrained(base_model)
model = AutoModelForCausalLM.from_pretrained(base_model)

# Add padding token
tokenizer.pad_token = tokenizer.eos_token

# Prepare text generation dataset
def tokenize_for_generation(examples):
    return tokenizer(
        examples["text"],
        truncation=True,
        max_length=512,
        padding="max_length"
    )

# Training for causal LM
training_args = TrainingArguments(
    output_dir="./gpt2_finetuned",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=5e-5,
    num_train_epochs=3,
    logging_steps=100,
    save_steps=500,
    fp16=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    tokenizer=tokenizer,
)

trainer.train()

# Generate text
from transformers import pipeline

generator = pipeline("text-generation", model="./gpt2_finetuned", tokenizer=tokenizer)
output = generator("The PCB component shows", max_length=50, num_return_sequences=1)
print(output)
