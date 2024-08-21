import csv
from datetime import datetime

# Erişim günlüğü verileri
access_log_data = [
    {"ip_address": "192.168.1.1", "request_type": "GET", "response_code": 200, "timestamp": "2024-08-20T12:45:30", "page_accessed": "/home"},
    {"ip_address": "192.168.1.2", "request_type": "GET", "response_code": 200, "timestamp": "2024-08-20T12:46:15", "page_accessed": "/about"},
    {"ip_address": "192.168.1.1", "request_type": "POST", "response_code": 404, "timestamp": "2024-08-20T12:47:05", "page_accessed": "/submit"},
    {"ip_address": "192.168.1.3", "request_type": "GET", "response_code": 500, "timestamp": "2024-08-20T12:48:00", "page_accessed": "/contact"},
    {"ip_address": "192.168.1.4", "request_type": "GET", "response_code": 200, "timestamp": "2024-08-20T12:48:50", "page_accessed": "/services"},
    {"ip_address": "192.168.1.2", "request_type": "GET", "response_code": 200, "timestamp": "2024-08-20T12:50:10", "page_accessed": "/home"},
    {"ip_address": "192.168.1.5", "request_type": "POST", "response_code": 401, "timestamp": "2024-08-20T12:51:20", "page_accessed": "/login"},
    {"ip_address": "192.168.1.1", "request_type": "GET", "response_code": 200, "timestamp": "2024-08-20T12:52:30", "page_accessed": "/dashboard"},
    {"ip_address": "192.168.1.4", "request_type": "GET", "response_code": 200, "timestamp": "2024-08-20T12:53:15", "page_accessed": "/about"},
    {"ip_address": "192.168.1.3", "request_type": "GET", "response_code": 403, "timestamp": "2024-08-20T12:54:00", "page_accessed": "/settings"}
]

# Hata günlüğü verileri
error_log_data = [
    {"timestamp": "2024-08-20T12:47:05", "error_code": 404, "error_message": "Not Found: /submit"},
    {"timestamp": "2024-08-20T12:48:00", "error_code": 500, "error_message": "Internal Server Error: /contact"},
    {"timestamp": "2024-08-20T12:51:20", "error_code": 401, "error_message": "Unauthorized: /login"},
    {"timestamp": "2024-08-20T12:54:00", "error_code": 403, "error_message": "Forbidden: /settings"}
]

# CSV dosyalarını oluşturma
def create_csv(filename, data, fieldnames):
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Erişim günlükleri dosyası
access_fieldnames = ["ip_address", "request_type", "response_code", "timestamp", "page_accessed"]
create_csv("access_log.csv", access_log_data, access_fieldnames)

# Hata günlükleri dosyası
error_fieldnames = ["timestamp", "error_code", "error_message"]
create_csv("error_log.csv", error_log_data, error_fieldnames)

print("CSV dosyaları oluşturuldu: access_log.csv ve error_log.csv")
