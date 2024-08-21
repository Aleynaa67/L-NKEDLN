from transformers import T5Tokenizer, T5ForConditionalGeneration
from spellchecker import SpellChecker

def correct_spelling(text):
    spell = SpellChecker()
    words = text.split()
    corrected_words = [spell.candidates(word).pop() if len(spell.candidates(word)) > 0 else word for word in words]
    return ' '.join(corrected_words)

# Model ve tokenizer'ı yükleyin
model_name = "t5-base"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

def generate_answer(query, context):
    # Sorgu ve bağlamı birleştirin
    input_text = f"Question: {query} Context: {context}"
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)

    # Modeli kullanarak yanıtı oluşturun
    outputs = model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=300,
        min_length=50,
        num_beams=5,
        early_stopping=True,
        length_penalty=1.0,
        no_repeat_ngram_size=2,
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id
    )

    # Yanıtı decode edin
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer

def main():
    # Sorgular ve genişletilmiş bağlam
    queries = [
        "Web sitesinde en sık rastlanan hata türlerinin neler olduğunu ve bu hataların hangi sıklıkta meydana geldiğini belirtir misiniz?",
        "Son 24 saat içinde meydana gelen tüm 500 Internal Server Error hatalarının tarih ve saat bilgileriyle birlikte ayrıntılı açıklamalarını listeleyebilir misiniz?",
        "Son bir haftalık dönemde, web sitesinde en yüksek trafik yoğunluğuna sahip olan saat dilimlerini sıralar mısınız?",
        "Bugün içinde meydana gelen tüm '404 Not Found' hatalarının detaylarını, tarih ve saat bilgileriyle birlikte listeleyebilir misiniz?",
        "Son 10 erişim kaydının hangi IP adreslerinden geldiğini tarih ve saat bilgileriyle birlikte sıralayabilir misiniz?",
        "Web sitesinde son bir hafta içinde en çok ziyaret edilen 5 sayfanın URL'lerini ve ziyaret sayılarını listeleyebilir misiniz?",
    ]

    context = """
    2024-08-20T12:48:00, 500, Internal Server Error: /contact - Sunucu hatası, sayfa yüklenemedi. Bu hata, sunucu tarafında beklenmedik bir durumdan kaynaklandı ve kullanıcıya hata mesajı gösterildi.
    2024-08-20T12:49:05, 500, Internal Server Error: /api/data - Veri sağlama hatası, sunucu yanıt vermedi. API çağrısı sırasında bir hata oluştu ve kullanıcıya veri sağlanamadı.
    2024-08-20T12:50:00, 500, Internal Server Error: /contact - Tekrar eden sunucu hatası, sayfa yüklenemedi. Önceki hata ile aynı sebep, kullanıcıya hata mesajı gösterildi.
    2024-08-20T12:51:20, 401, Unauthorized: /login - Kimlik doğrulama hatası, oturum açma başarısız. Kullanıcı girdiği kimlik bilgileriyle oturum açamadı.
    2024-08-20T12:52:15, 404, Not Found: /submit - Sayfa bulunamadı, kullanıcıya bilgi verilmedi. Kullanıcı tarafından istenilen sayfa mevcut değil, hata mesajı gösterildi.
    2024-08-20T12:53:10, 404, Not Found: /about - İstenilen sayfa mevcut değil, kullanıcıya hata mesajı gösterildi. Sayfa bulunamadı ve kullanıcıya hata bilgisi verildi.
    2024-08-20T12:54:20, 200, OK: /home - Sayfa başarıyla yüklendi. Kullanıcıya istenilen veri başarıyla sağlandı.
    2024-08-19T11:47:05, 404, Not Found: /oldpage - Eski sayfa, bulunamadı. Kullanıcı tarafından erişilmeye çalışılan eski sayfa mevcut değil, hata mesajı gösterildi.
    2024-08-19T11:50:00, 200, OK: /contact - Sayfa başarıyla yüklendi, tüm veriler sağlandı. Kullanıcıya doğru bilgi sunuldu.
    """

    # Her bir sorgu için yanıtları oluşturun
    for query in queries:
        answer = generate_answer(query, context)
        corrected_answer = correct_spelling(answer)
        print(f"Soru: {query}")
        print(f"Oluşturulan Yanıt: {corrected_answer}")
        print("-" * 80)

if __name__ == "__main__":
    main()
