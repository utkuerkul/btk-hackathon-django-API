import os
import logging
import unicodedata
from huggingface_hub import InferenceClient
import google.generativeai as genai

# Google Generative AI (PaLM) API anahtarınız
API_KEY = "AIzaSyBTrGFRms4smKkFea_1yXZjC3IycW74iSY"

def call_inference_api(prompt: str) -> str:
    """
    Google Generative AI (PaLM 2) üzerinden metin üretimi yapan örnek fonksiyon.
    response.result -> modelin ürettiği metnin tamamı.
    """
    try:
        # 1) API için konfigürasyon
        genai.configure(api_key=API_KEY)

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Model çalıştırılırken hata oluştu: {str(e)}"

def create_prompt(user_data: dict, target_row_data: dict, accuracy: float) -> str:
    """
    Kullanıcı verilerini, çekilen tek satırlık veriyi ve hesaplanan doğruluk oranını
    bir araya getirip LLM için girdi metni (prompt) oluşturur.
    """
    # 1) Kullanıcı Verileri
    uid = user_data.get("uid", "")
    date = user_data.get("date", "")
    user_field = user_data.get("userField", "")
    user_goal = user_data.get("userGoal", "")
    lesson_name = user_data.get("lessonName", "")
    analysis_type = user_data.get("type", "")
    lesson_data = user_data.get("lessonData", [])

    # 2) Prompt başlangıcı
    prompt = (
        f"Kullanıcı Bilgileri:\n"
        f"- UID: {uid}\n"
        f"- Tarih: {date}\n"
        f"- Alan: {user_field}\n"
        f"- Hedef (Üniversite Adı): {user_goal}\n"
        f"- Program (Bölüm) Adı: {lesson_name}\n"
        f"- Analiz Türü: {analysis_type}\n"
        f"- Genel doğruluk oranı: % {accuracy:.2f}\n\n"
    )

    # 3) Hedef Kurum ve Program Bilgileri
    prompt += "Hedef Kurum ve Program Bilgileri:\n"
    if not target_row_data:
        prompt += "  (Bu üniversite veya program için veri bulunamadı.)\n"
    else:
        for key, value in target_row_data.items():
            prompt += f"  - {key}: {value}\n"

    # 4) Kullanıcının Ders Performansı
    prompt += "\nKullanıcının Ders Performansı (Sayısal Veriler):\n"
    if lesson_data:
        for i, lesson in enumerate(lesson_data, start=1):
            prompt += (
                f"  Ders {i}: {lesson.get('lesson', '')}\n"
                f"    - Tarih: {lesson.get('date', '')}\n"
                f"    - Doğru: {lesson.get('trueAnswers', 0)}\n"
                f"    - Yanlış: {lesson.get('falseAnswers', 0)}\n"
                f"    - Net: {lesson.get('clearAnswers', 0.0)}\n"
                f"    - Toplam Cevap: {lesson.get('totalAnswer', 0)}\n"
            )
    else:
        prompt += "  (Herhangi bir ders verisi bulunamadı.)\n"

    # 5) Nihai Talimatlar (Sayısal Verilere Dayalı Öneriler)
    prompt += (
        "\nLütfen bu verilerden hareketle, zincirleme akıl yürütme (chain of thought) mantığıyla "
        "içsel olarak düşün, ancak yalnızca SONUÇ odaklı bir final öneri metni oluştur. "
        "Aradaki akıl yürütme sürecini paylaşma.\n\n"
        "Sonuç metninde lütfen şunları yap:\n"
        "1) Öğrencinin mevcut durumunu, doğru-yanlış sayıları ve net oranı üzerinden değerlendir.\n"
        "   - Ortalama doğru-yanlış verileri ışığında öğrencinin konumunu belirt.\n\n"
        "2) İlgili kurum/bölüm için gerekli ortalama doğru cevap sayısını da dikkate alarak, "
        "öğrencinin mevcut performansı ile bu hedef arasındaki farkı rakamlarla açıkla.\n"
        "   - Mevcut ortalama doğru/yanlış netleriyle, hedeflenen doğru cevap sayısını kıyasla.\n\n"
        "3) Puan, kontenjan, başarı sıralaması vb. bilgilere atıfta bulunup, öğrenciye "
        "hedefine ulaşması için hangi derslerde ne kadar daha doğru cevap artırması gerektiğini "
        "somut bir şekilde ifade et.\n\n"
        "4) Ders performansı ve hedef arasındaki boşlukları kapatacak kısa, nicel yönlendirmeler ver.\n"
        "   - Örneğin, haftalık çalışma planı, konu eksikleri, test denemeleri, ortalama net yükseltme stratejileri.\n\n"
        "5) Yalnızca final önerilerini yaz; kesinlikle düşünce zincirini veya verilerin nereden alındığını belirtme.\n"
    )

    return prompt

