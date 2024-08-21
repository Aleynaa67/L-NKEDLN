import csv

# Erişim günlüğü verileri
access_log_data = [
    {"ip_address": "192.168.1.1", "request_type": "GET", "response_code": 500, "timestamp": "2024-08-20T12:48:00", "page_accessed": "/contact", "description": "Internal Server Error, page could not be loaded. This error was caused by an unexpected issue on the server side and an error message was shown to the user."},
    {"ip_address": "192.168.1.2", "request_type": "GET", "response_code": 500, "timestamp": "2024-08-20T12:49:05", "page_accessed": "/api/data", "description": "Internal Server Error, server did not respond. An error occurred during the API call and data could not be provided to the user."},
    {"ip_address": "192.168.1.3", "request_type": "GET", "response_code": 500, "timestamp": "2024-08-20T12:50:00", "page_accessed": "/contact", "description": "Recurring server error, page could not be loaded. Same cause as the previous error, an error message was shown to the user."},
    {"ip_address": "192.168.1.4", "request_type": "POST", "response_code": 401, "timestamp": "2024-08-20T12:51:20", "page_accessed": "/login", "description": "Authentication error, login failed. The user could not log in with the provided credentials."},
    {"ip_address": "192.168.1.5", "request_type": "POST", "response_code": 404, "timestamp": "2024-08-20T12:52:15", "page_accessed": "/submit", "description": "Page not found, no information provided to the user. The page requested by the user does not exist, an error message was shown."},
    {"ip_address": "192.168.1.6", "request_type": "GET", "response_code": 404, "timestamp": "2024-08-20T12:53:10", "page_accessed": "/about", "description": "Requested page does not exist, an error message was shown to the user. Page not found and error information was provided to the user."},
    {"ip_address": "192.168.1.7", "request_type": "GET", "response_code": 200, "timestamp": "2024-08-20T12:54:20", "page_accessed": "/home", "description": "Page successfully loaded. The requested data was successfully provided to the user."},
    {"ip_address": "192.168.1.8", "request_type": "GET", "response_code": 404, "timestamp": "2024-08-19T11:47:05", "page_accessed": "/oldpage", "description": "Old page, not found. The old page the user attempted to access does not exist, an error message was shown."},
    {"ip_address": "192.168.1.9", "request_type": "GET", "response_code": 200, "timestamp": "2024-08-19T11:50:00", "page_accessed": "/contact", "description": "Page successfully loaded, all data was provided. Accurate information was provided to the user."}
]

# Hata günlüğü verileri
error_log_data = [
    {"timestamp": "2024-08-20T12:48:00", "error_code": 500, "error_message": "Internal Server Error: /contact - Server error, page could not be loaded. This error was caused by an unexpected issue on the server side and an error message was shown to the user."},
    {"timestamp": "2024-08-20T12:49:05", "error_code": 500, "error_message": "Internal Server Error: /api/data - Data provision error, server did not respond. An error occurred during the API call and data could not be provided to the user."},
    {"timestamp": "2024-08-20T12:50:00", "error_code": 500, "error_message": "Internal Server Error: /contact - Recurring server error, page could not be loaded. Same cause as the previous error, an error message was shown to the user."},
    {"timestamp": "2024-08-20T12:51:20", "error_code": 401, "error_message": "Unauthorized: /login - Authentication error, login failed. The user could not log in with the provided credentials."},
    {"timestamp": "2024-08-20T12:52:15", "error_code": 404, "error_message": "Not Found: /submit - Page not found, no information provided to the user. The page requested by the user does not exist, an error message was shown."},
    {"timestamp": "2024-08-20T12:53:10", "error_code": 404, "error_message": "Not Found: /about - Requested page does not exist, an error message was shown to the user. Page not found and error information was provided to the user."},
    {"timestamp": "2024-08-20T12:54:20", "error_code": 200, "error_message": "OK: /home - Page successfully loaded. The requested data was successfully provided to the user."},
    {"timestamp": "2024-08-19T11:47:05", "error_code": 404, "error_message": "Not Found: /oldpage - Old page, not found. The old page the user attempted to access does not exist, an error message was shown."},
    {"timestamp": "2024-08-19T11:50:00", "error_code": 200, "error_message": "OK: /contact - Page successfully loaded, all data was provided. Accurate information was provided to the user."}
]

# CSV dosyalarını oluşturma
def create_csv(filename, data, fieldnames):
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Erişim günlükleri dosyası
access_fieldnames = ["ip_address", "request_type", "response_code", "timestamp", "page_accessed", "description"]
create_csv("access_log.csv", access_log_data, access_fieldnames)

# Hata günlükleri dosyası
error_fieldnames = ["timestamp", "error_code", "error_message"]
create_csv("error_log.csv", error_log_data, error_fieldnames)

print("CSV dosyaları oluşturuldu: access_log.csv ve error_log.csv")
