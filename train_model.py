from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments
from datasets import load_dataset

# Model ve tokenizer'ı yükleyin
model_name = "t5-base"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Veriyi yükleme
def preprocess_function(examples):
    inputs = examples['question'] + " " + examples['context']
    targets = examples['answer']
    model_inputs = tokenizer(inputs, max_length=512, truncation=True)
    labels = tokenizer(targets, max_length=512, truncation=True)
    model_inputs['labels'] = labels['input_ids']
    return model_inputs

dataset = load_dataset('json', data_files={'train': 'train_data.json', 'validation': 'valid_data.json'})
tokenized_datasets = dataset.map(preprocess_function, batched=True)

# Eğitim argümanları
training_args = TrainingArguments(
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    output_dir='./results',
    num_train_epochs=3,
    evaluation_strategy="epoch",
    logging_dir='./logs',
    logging_steps=10,
)

# Trainer'ı oluşturma
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets['train'],
    eval_dataset=tokenized_datasets['validation'],
)

# Eğitimi başlatma
trainer.train()

# Modeli kaydetme
model.save_pretrained('./fine-tuned-t5')
tokenizer.save_pretrained('./fine-tuned-t5')
