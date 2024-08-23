from transformers import T5Tokenizer, T5ForConditionalGeneration

# Model ve tokenizer'ı yükleyin
model = T5ForConditionalGeneration.from_pretrained('./fine-tuned-t5')
tokenizer = T5Tokenizer.from_pretrained('./fine-tuned-t5')

def generate_answer(query, context):
    # Giriş metnini hazırlayın
    input_text = f"Explain the reasons behind the following error code from the log data:\n\nError Code: {query}\n\nLog Data:\n{context}"

    # Tokenize etme
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    attention_mask = inputs.get('attention_mask')

    try:
        # Modeli çalıştırma
        outputs = model.generate(
            inputs['input_ids'],
            attention_mask=attention_mask,
            max_length=300,
            num_beams=6,
            early_stopping=True,
            length_penalty=1.0,
            no_repeat_ngram_size=2,
            pad_token_id=tokenizer.eos_token_id
        )
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        answer = f"Yanıt oluşturulurken bir hata meydana geldi: {str(e)}"

    return answer

def format_answer(answer):
    # Yanıtın formatını kontrol et ve daha net bir çıktı üret
    if "500 Internal Server Error" in answer:
        return answer
    else:
        return f"Yanıt şu anda '500 Internal Server Error' içermiyor. Yanıt: {answer}"

def main():
    query = "500 Internal Server Error"
    context = """
    2024-08-20T12:48:00, 500, Internal Server Error: /contact - IP: 192.168.1.1 - Server error, page could not be loaded due to an unexpected issue on the server side.
    2024-08-20T12:49:05, 500, Internal Server Error: /api/data - IP: 192.168.1.2 - Data provision error, server did not respond properly. An error occurred during the API call and data could not be provided.
    2024-08-20T12:50:00, 500, Internal Server Error: /contact - IP: 192.168.1.3 - Recurring server error, page could not be loaded due to the same cause as the previous errors.
    2024-08-20T12:51:20, 401, Unauthorized: /login - IP: 192.168.1.4 - Authentication error, login failed. The user could not log in with the provided credentials.
    2024-08-20T12:52:15, 404, Not Found: /submit - IP: 192.168.1.5 - Page not found, no information provided to the user. The page requested by the user does not exist.
    2024-08-20T12:53:10, 404, Not Found: /about - IP: 192.168.1.6 - Requested page does not exist, an error message was shown to the user. Page not found.
    2024-08-19T11:47:05, 404, Not Found: /oldpage - IP: 192.168.1.8 - Old page, not found. The old page the user attempted to access does not exist.
    2024-08-19T11:50:00, 200, OK: /contact - IP: 192.168.1.9 - Page successfully loaded, all data was provided. Accurate information was provided to the user.
    """

    answer = generate_answer(query, context)
    formatted_answer = format_answer(answer)

    print(f"Soru: Can you explain the reasons behind the 500 Internal Server Error in the logs?")
    print(f"Oluşturulan Yanıt: {formatted_answer}")

if __name__ == "__main__":
    main()
