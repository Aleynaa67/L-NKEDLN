# retrieval_test.py

from transformers import T5Tokenizer, T5ForConditionalGeneration
import re

# Model ve tokenizer'ı yükle
model_name = "t5-base"
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
        max_length=500,  # Yanıt uzunluğunu ayarla
        num_beams=5,
        early_stopping=True,
        no_repeat_ngram_size=2,
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id
    )

    # Yanıtı decode et ve temizle
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer


def format_answer(answer):
    # Yanıtı düzenle
    lines = answer.split('. ')
    formatted_lines = [line.strip() for line in lines if line.strip()]
    formatted_answer = '\n'.join(formatted_lines)

    # Gereksiz boşlukları ve özel karakterleri temizle
    formatted_answer = re.sub(r'\s+', ' ', formatted_answer).strip()
    return formatted_answer


# Test soruları ve cevapları
questions = [
    "Web sitesinde en sık karşılaşılan hata türleri nelerdir?",
    "Son 24 saat içinde meydana gelen 500 hatalarının ayrıntıları nelerdir?",
    "Son bir haftada en yoğun trafiğe sahip saat dilimleri hangileridir?",
    "Bugün gerçekleşen tüm '404 Not Found' hataları nelerdir?",
    "En son 10 erişim kaydı hangi IP adreslerinden geldi?",
    "En çok ziyaret edilen 5 sayfa nedir?",
]

context = """
2024-08-20T12:48:00, 500, Internal Server Error: /contact
192.168.1.3, POST, 500, 2024-08-20T12:48:00, /contact
2024-08-20T12:51:20, 401, Unauthorized: /login
2024-08-20T12:47:05, 404, Not Found: /submit
192.168.1.2, GET, 404, 2024-08-20T12:46:15, /about
"""

# Test sorularını çalıştır
for question in questions:
    answer = generate_answer(question, context)
    formatted_answer = format_answer(answer)
    print(f"Soru: {question}")
    print(f"Oluşturulan Yanıt: {formatted_answer}\n")
