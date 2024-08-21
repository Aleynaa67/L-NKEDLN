from transformers import T5Tokenizer, T5ForConditionalGeneration
import re

# Model ve tokenizer'ı yükle
model_name = "t5-large"
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)


def clean_text(text):
    # Gereksiz karakterleri temizleyin
    text = re.sub(r'[^\w\s.,:;?!]', '', text)  # Yalnızca harf, rakam ve bazı noktalama işaretlerine izin ver
    text = re.sub(r'\s+', ' ', text).strip()  # Birden fazla boşluğu tek bir boşlukla değiştir
    return text


def generate_answer(query, context):
    input_text = f"Question: {query} Context: {context}"
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)

    outputs = model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=200,  # Yanıt uzunluğunu artırdık
        min_length=30,  # Minimum yanıt uzunluğunu artırdık
        num_beams=5,  # Beam search sayısını artırdık
        early_stopping=True,
        length_penalty=1.2,  # Uzun yanıtların ödüllendirilmesini artırdık
        no_repeat_ngram_size=2,
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id
    )

    # Yanıtı decode et ve temizle
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer


def format_answer(answer):
    # Yanıtı satırlara ayır ve düzenle
    # Önce noktalama işaretleri ve boşlukları düzenleyin
    cleaned_answer = re.sub(r'\s+', ' ', answer).strip()  # Çoklu boşlukları tek boşlukla değiştir

    # Cümlelerin sonundaki boşlukları ve fazla boşlukları temizle
    cleaned_answer = re.sub(r'(\.|\?|\!)\s*(?=[A-Z])', r'\1\n', cleaned_answer)  # Cümle sonlarını ayır
    cleaned_answer = re.sub(r'(\n\s*)+', '\n', cleaned_answer)  # Birden fazla satır başını tek satır başına dönüştür

    # Gereksiz boşlukları temizle
    cleaned_answer = re.sub(r'\s+', ' ', cleaned_answer).strip()

    # Cümleleri ve paragrafları yeniden düzenle
    # Paragraf başlarını düzelt
    formatted_answer = re.sub(r'(\n\s*)+', '\n\n', cleaned_answer)  # İki boşluklu satır başları paragrafları ayırır

    return formatted_answer
