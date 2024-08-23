from transformers import T5Tokenizer, T5ForConditionalGeneration

# Model ve tokenizer'ı yükleyin
model = T5ForConditionalGeneration.from_pretrained('./fine-tuned-t5')
tokenizer = T5Tokenizer.from_pretrained('./fine-tuned-t5')


def generate_answer(query, context):
    # Giriş metnini hazırlayın
    input_text = f"Explain the reasons behind the following error code from the log data:\n\n{query}\n\nContext:\n{context}"

    # Tokenize etme
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    attention_mask = inputs['attention_mask']

    try:
        # Modeli çalıştırma
        outputs = model.generate(
            inputs['input_ids'],
            attention_mask=attention_mask,
            max_length=200,
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
    # Yanıtın formatını kontrol et
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
    """

    answer = generate_answer(query, context)
    formatted_answer = format_answer(answer)

    print(f"Soru: Can you explain the reasons behind the 500 Internal Server Error in the logs?")
    print(f"Oluşturulan Yanıt: {formatted_answer}")


if __name__ == "__main__":
    main()
