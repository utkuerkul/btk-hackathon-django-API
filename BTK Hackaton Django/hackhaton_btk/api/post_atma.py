import requests

url = "http://127.0.0.1:8000/api/exam-results-suggestions/"

data = {
    "uid": "user12345",
    "date": "2024-12-02",
    "userField": "Sayısal",
    "userGoal": "YOZGAT BOZOK ÜNİVERSİTESİ)",
    "lessonName": "Rehberlik ve Psikolojik Danışmanlık",
    "type": "weekly",
    "lessonData": [
        {"lesson": "Matematik", "trueAnswers": 18, "falseAnswers": 2, "clearAnswers": 17.0, "totalAnswer": 20},
        {"lesson": "Matematik", "trueAnswers": 14, "falseAnswers": 6, "clearAnswers": 11.0, "totalAnswer": 20},
        {"lesson": "Matematik", "trueAnswers": 12, "falseAnswers": 8, "clearAnswers": 8.0, "totalAnswer": 20}
    ]
}

resp = requests.post(url, json=data)
print("Status Code:", resp.status_code)
print("Response:", resp.json())
