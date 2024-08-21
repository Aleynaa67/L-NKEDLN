from transformers import T5Tokenizer, T5ForConditionalGeneration
from spellchecker import SpellChecker

def correct_spelling(text):
    spell = SpellChecker()
    words = text.split()
    corrected_words = []

    for word in words:
        # Kelimenin doğru olup olmadığını kontrol et
        if word in spell:
            corrected_words.append(word)
        else:
            # Yanlış yazılmış kelime için önerileri al
            candidates = spell.candidates(word)
            if candidates:
                corrected_word = max(candidates, key=len)
            else:
                corrected_word = word  # Öneri yoksa orijinal kelimeyi kullan
            corrected_words.append(corrected_word)

    return ' '.join(corrected_words)

# Model ve tokenizer'ı yükleyin
model_name = "t5-base"
tokenizer = T5Tokenizer.from_pretrained(model_name, legacy=False)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Yanıt üreten fonksiyon
def generate_answer(query, context):
    input_text = f"Question: {query}\nContext:\n{context}"
    print(f"Girdi Metni: {input_text}")  # Girdi metnini yazdırın

    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    print(f"Tokenize Edilmiş Girdi: {inputs}")  # Tokenize edilmiş girdileri yazdırın

    try:
        outputs = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=150,
            min_length=50,
            num_beams=5,
            early_stopping=True,
            length_penalty=1.2,
            no_repeat_ngram_size=2,
            pad_token_id=tokenizer.eos_token_id
        )
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"Model Çıkışı: {outputs}")  # Model çıktısını yazdırın
        print(f"Yanıt: {answer}")  # Yanıtı yazdırın
        return answer
    except Exception as e:
        print(f"Yanıt Üretme Hatası: {e}")
        return "Yanıt oluşturulurken bir hata meydana geldi."

def main():
    # Soru kümesi
    queries = [
        "What are the most common types of errors encountered on the website and how frequently do they occur?",
        "Can you list all the 500 Internal Server Error logs from the past 24 hours with timestamps and detailed descriptions?",
        "Can you rank the time periods with the highest traffic on the website over the past week?",
        "Can you provide details of all '404 Not Found' errors occurring today, including timestamps?",
        "Can you list the last 10 access logs including the IP addresses with timestamps?"
    ]

    # Güncellenmiş log verileri
    context = """
    2024-08-20T12:48:00, 500, Internal Server Error: /contact - IP: 192.168.1.1 - Server error, page could not be loaded. This error was caused by an unexpected issue on the server side and an error message was shown to the user.
    2024-08-20T12:49:05, 500, Internal Server Error: /api/data - IP: 192.168.1.2 - Data provision error, server did not respond. An error occurred during the API call and data could not be provided to the user.
    2024-08-20T12:50:00, 500, Internal Server Error: /contact - IP: 192.168.1.3 - Recurring server error, page could not be loaded. Same cause as the previous error, an error message was shown to the user.
    2024-08-20T12:51:20, 401, Unauthorized: /login - IP: 192.168.1.4 - Authentication error, login failed. The user could not log in with the provided credentials.
    2024-08-20T12:52:15, 404, Not Found: /submit - IP: 192.168.1.5 - Page not found, no information provided to the user. The page requested by the user does not exist, an error message was shown.
    2024-08-20T12:53:10, 404, Not Found: /about - IP: 192.168.1.6 - Requested page does not exist, an error message was shown to the user. Page not found and error information was provided to the user.
    2024-08-20T12:54:20, 200, OK: /home - IP: 192.168.1.7 - Page successfully loaded. The requested data was successfully provided to the user.
    2024-08-19T11:47:05, 404, Not Found: /oldpage - IP: 192.168.1.8 - Old page, not found. The old page the user attempted to access does not exist, an error message was shown.
    2024-08-19T11:50:00, 200, OK: /contact - IP: 192.168.1.9 - Page successfully loaded, all data was provided. Accurate information was provided to the user.
    """

    for query in queries:
        answer = generate_answer(query, context)
        corrected_answer = correct_spelling(answer)

        print(f"Soru: {query}")
        print(f"Oluşturulan Yanıt: {corrected_answer}")
        print("-" * 80)

if __name__ == "__main__":
    main()
