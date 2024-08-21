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
    queries = [
        "Web sitesinde en sık rastlanan hata türlerinin neler olduğunu ve bu hataların hangi sıklıkta meydana geldiğini belirtir misiniz?",
        "Son 24 saat içinde meydana gelen tüm 500 Internal Server Error hatalarının tarih ve saat bilgileriyle birlikte ayrıntılı açıklamalarını listeleyebilir misiniz?",
        "Son bir haftalık dönemde, web sitesinde en yüksek trafik yoğunluğuna sahip olan saat dilimlerini sıralar mısınız?",
        "Bugün içinde meydana gelen tüm '404 Not Found' hatalarının detaylarını, tarih ve saat bilgileriyle birlikte listeleyebilir misiniz?",
        "Son 10 erişim kaydının hangi IP adreslerinden geldiğini tarih ve saat bilgileriyle birlikte sıralayabilir misiniz?",
    ]

    context ="""
2024-08-20T12:48:00, 500, Internal Server Error: /contact - IP: 192.168.1.1 - Sunucu hatası, sayfa yüklenemedi. Bu hata, sunucu tarafında beklenmedik bir durumdan kaynaklandı ve kullanıcıya hata mesajı gösterildi.
2024-08-20T12:49:05, 500, Internal Server Error: /api/data - IP: 192.168.1.2 - Veri sağlama hatası, sunucu yanıt vermedi. API çağrısı sırasında bir hata oluştu ve kullanıcıya veri sağlanamadı.
2024-08-20T12:50:00, 500, Internal Server Error: /contact - IP: 192.168.1.3 - Tekrar eden sunucu hatası, sayfa yüklenemedi. Önceki hata ile aynı sebep, kullanıcıya hata mesajı gösterildi.
2024-08-20T12:51:20, 401, Unauthorized: /login - IP: 192.168.1.4 - Kimlik doğrulama hatası, oturum açma başarısız. Kullanıcı girdiği kimlik bilgileriyle oturum açamadı.
2024-08-20T12:52:15, 404, Not Found: /submit - IP: 192.168.1.5 - Sayfa bulunamadı, kullanıcıya bilgi verilmedi. Kullanıcı tarafından istenilen sayfa mevcut değil, hata mesajı gösterildi.
2024-08-20T12:53:10, 404, Not Found: /about - IP: 192.168.1.6 - İstenilen sayfa mevcut değil, kullanıcıya hata mesajı gösterildi. Sayfa bulunamadı ve kullanıcıya hata bilgisi verildi.
2024-08-20T12:54:20, 200, OK: /home - IP: 192.168.1.7 - Sayfa başarıyla yüklendi. Kullanıcıya istenilen veri başarıyla sağlandı.
2024-08-19T11:47:05, 404, Not Found: /oldpage - IP: 192.168.1.8 - Eski sayfa, bulunamadı. Kullanıcı tarafından erişilmeye çalışılan eski sayfa mevcut değil, hata mesajı gösterildi.
2024-08-19T11:50:00, 200, OK: /contact - IP: 192.168.1.9 - Sayfa başarıyla yüklendi, tüm veriler sağlandı. Kullanıcıya doğru bilgi sunuldu.
"""

    for query in queries:
        answer = generate_answer(query, context)
        corrected_answer = correct_spelling(answer)

        print(f"Soru: {query}")
        print(f"Oluşturulan Yanıt: {corrected_answer}")
        print("-" * 80)

if __name__ == "__main__":
    main()
