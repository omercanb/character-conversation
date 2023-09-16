from datasets import load_dataset, Features, Value
from transformers import AutoModelForCausalLM, AutoTokenizer, DataCollatorWithPadding, TrainingArguments, Trainer, DataCollatorForLanguageModeling, GPT2LMHeadModel
from peft import LoraConfig, PeftConfig, PeftModel, get_peft_model, prepare_model_for_kbit_training

path = "jokerdata.csv"
dataset = load_dataset("csv", data_files=path)

tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")
model.save_pretrained("gpt2 local")
tokenizer.pad_token = tokenizer.eos_token

# model.gradient_checkpointing_enable()
# model = prepare_model_for_kbit_training(model)
# config = LoraConfig(
#     r=16,
#     lora_alpha=32,
#     target_modules=["query_key_value"],
#     lora_dropout=0.05,
#     bias="none",
#     task_type="CAUSAL_LM"
# )

# model = get_peft_model(model, config)

def get_full_prompt(prompt_response_pair):
    return f"""
    <Human>: {prompt_response_pair['prompt']}
    <Joker>: {prompt_response_pair['response']}
    """.strip()

def generate_and_tokenize_dataset(data_point):
    return tokenizer(data_point['prompt'],data_point['response'] , truncation=True)

tokenized_dataset = dataset.map(generate_and_tokenize_dataset, batched = True)
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

training_args = TrainingArguments(
      per_device_train_batch_size=1,
      gradient_accumulation_steps=4,
      num_train_epochs=1,
      learning_rate=2e-4,
      save_total_limit=3,
      logging_steps=1,
      output_dir="experiments",
      optim="adamw_hf",
      lr_scheduler_type="cosine",
      warmup_ratio=0.05,
)

trainer = Trainer(
    model,
    training_args,
    train_dataset=tokenized_dataset["train"],
    tokenizer=tokenizer,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
)

trainer.train()

trainer.save_model('test_model')