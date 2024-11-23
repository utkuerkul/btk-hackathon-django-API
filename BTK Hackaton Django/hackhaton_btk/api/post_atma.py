import requests

# API URL'si
url = "http://127.0.0.1:8000/user-suggestion/"
# Göndermek istediğiniz veriler
data = {
    "uid": "456",
    "name": "Ahmet",
    "surname": "Yılmaz",
    "birth_date": "2002-05-15",
    "study_field": "Sayısal",
    "daily_study_hours": 4.5,
    "goals": "Bilgisayar Mühendisliği",
    "gpa": 3.75,
}

response = requests.post(url, json=data)
print(response.status_code, response.text)

import requests

# API URL'si
url = "http://127.0.0.1:8000/exam-results-suggestion/"

# Göndermek istediğiniz sınav sonuçları verisi
data = {
    "user_id": "456",  # Kullanıcı kimliği ekleniyor
    "exam_results": [
        {
            "lessons": "Matematik",
            "true_answers": 30,
            "false_answers": 5,
            "clear_answers": 27.5,
            "date": "2024-10-15",
            "exam_type": "TYT"
        },
        {
            "lessons": "Fizik",
            "true_answers": 15,
            "false_answers": 3,
            "clear_answers": 13.5,
            "date": "2024-10-15",
            "exam_type": "AYT"
        }
    ]
}

try:
    # POST isteğini gönder
    response = requests.post(url, json=data)

    # Yanıt durum kodunu ve içeriğini kontrol et
    print("Yanıt Durum Kodu:", response.status_code)  # Durum kodunu yazdır

    # Yanıt içeriğini kontrol et
    if response.content:
        print("Yanıt İçeriği (raw):", response.content)  # Ham içeriği yazdır
    else:
        print("Yanıt içeriği boş!")

    # Yanıtı JSON olarak alma denemesi
    try:
        response_json = response.json()  # JSON formatında yanıt al
        print("Yanıt JSON İçeriği:", response_json)  # JSON içeriği yazdır
    except ValueError:
        print("Yanıt JSON formatında değil. Hata:", response.text)  # Hata mesajını yazdır

except requests.exceptions.RequestException as e:
    # İstek hatalarını yakala
    print("İstek sırasında bir hata oluştu:", str(e))

