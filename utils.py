# Giriş metnini tanımlayın
input_text = """
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