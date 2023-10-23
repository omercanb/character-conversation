from datasets import load_dataset, Features, Value
from transformers import AutoModelForCausalLM, AutoTokenizer, DataCollatorWithPadding, TrainingArguments, Trainer, DataCollatorForLanguageModeling, GPT2LMHeadModel
from peft import LoraConfig, PeftConfig, PeftModel, get_peft_model, prepare_model_for_kbit_training
import os
import sys

class MovieDialogueTrainer:

    def __init__(self, data_path, character, movie):
        self.data_path = data_path
        self.character = character
        self.movie = movie

    def prepeare_trainer(self):

        self.tokenizer = AutoTokenizer.from_pretrained("gpt2")
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = AutoModelForCausalLM.from_pretrained("gpt2")

        self.dataset = load_dataset("csv", data_files=self.data_path)
        self.tokenized_dataset = self.generate_tokenized_dataset()

        self.data_collator = DataCollatorForLanguageModeling(self.tokenizer, mlm=False)

        self.training_args = TrainingArguments(
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

    def train_save_model(self):
        if self.model_exists():
            print("Model already exists at:")
            print(self.get_save_path())
            return
        self.prepeare_trainer()
        self.train()
        self.save()


    def model_exists(self):
        return os.path.exists(self.get_save_path())

    def get_full_prompt(self, prompt_response_pair):
        return f"""
        <Human>: {prompt_response_pair['prompt']}
        <{self.character}]>: {prompt_response_pair['response']}
        """.strip()

    def generate_and_tokenize_prompt(self, data_point):
        full_prompt = self.get_full_prompt(data_point)
        tokenized_prompt = self.tokenizer(full_prompt, truncation=True, padding=True)
        return tokenized_prompt
        return self.tokenizer(data_point['prompt'],data_point['response'] , truncation=True)
    
    def generate_tokenized_dataset(self):
        return self.dataset.map(self.generate_and_tokenize_prompt)
    
    def train(self):
        print("Starting training")
        self.trainer = Trainer(
            self.model,
            self.training_args,
            train_dataset=self.tokenized_dataset["train"],
            tokenizer=self.tokenizer,
            data_collator=DataCollatorForLanguageModeling(self.tokenizer, mlm=False),
        )
        self.trainer.train()
        print("Training successful completed.")

    def save(self):
        save_path = self.get_save_directory()
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        path = self.get_save_path()
        self.trainer.save_model(path)
        print("Model sucessfully saved at: ")
        print(path)

    def get_save_directory(self):
        return "models" + os.sep + "finetuned" + os.sep + "movies" + os.sep + self.movie + os.sep
    
    def get_save_path(self):
        save_path = self.get_save_directory()
        character_for_filename = "".join(self.character.lower().split())
        filename = character_for_filename + "model"
        # path = save_path + filename
        path = save_path + self.character
        return path


    
        
def test():
    character = "shrek"
    path = character + "data.csv"
    dataset = load_dataset("csv", data_files=path)

    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    model.save_pretrained("gpt2 local")
    tokenizer.pad_token = tokenizer.eos_token


    def get_full_prompt(prompt_response_pair):
        return f"""
        <Human>: {prompt_response_pair['prompt']}
        <Shrek>: {prompt_response_pair['response']}
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

    trainer.save_model(character + 'model')