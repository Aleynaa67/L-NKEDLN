def format_logs(logs):
    formatted_logs = []
    for log in logs:
        # Temizleme ve düzenleme işlemleri
        clean_log = log.replace('\n', ' ').strip()  # Satır başı ve boşlukları temizle
        formatted_logs.append(clean_log)
    return formatted_logs

if __name__ == "__main__":
    # Test logları
    access_logs = [
        "192.168.1.1, GET, 200, 2024-08-20T12:45:30, /home",
        "192.168.1.2, GET, 404, 2024-08-20T12:46:15, /about",
        "192.168.1.3, POST, 500, 2024-08-20T12:48:00, /contact"
    ]

    error_logs = [
        "2024-08-20T12:47:05, 404, Not Found: /submit",
        "2024-08-20T12:48:00, 500, Internal Server Error: /contact",
        "2024-08-20T12:51:20, 401, Unauthorized: /login"
    ]

    all_logs = access_logs + error_logs

    # Temizleme işlemi
    formatted_logs = format_logs(all_logs)

    # Temizlenmiş logları yazdır
    print("Temizlenmiş loglar:")
    for log in formatted_logs:
        print(log)
