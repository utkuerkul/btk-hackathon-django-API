from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import call_inference_api,create_prompt
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from django.conf import settings
import re

class UserActivitySuggestionView(APIView):
    def post(self, request):
        user_data = request.data

        lesson_data = user_data.get("lessonData", [])
        type_of_analysis = user_data.get("type", "daily")
        uid = user_data.get("uid", "")
        user_field = user_data.get("userField", "")
        user_goal = user_data.get("userGoal", "")

        if not lesson_data:
            return Response({"error": "lessonData is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Prompt oluşturma
        prompt = (
            f"Kullanıcı Bilgileri:\n"
            f"UID: {uid}\n"
            f"Alan: {user_field}\n"
            f"Hedef: {user_goal}\n"
            f"Analiz Türü: {type_of_analysis}\n\n"
            f"Ders Performans Verileri:\n"
        )

        for lesson in lesson_data:
            lesson_name = lesson.get("lesson", "")
            true_answers = lesson.get("trueAnswers", 0)
            false_answers = lesson.get("falseAnswers", 0)
            clear_answers = lesson.get("clearAnswers", 0.0)
            total_answer = lesson.get("totalAnswer", 0)
            date = lesson.get("date", "")

            prompt += (
                f"Ders: {lesson_name}, Tarih: {date}, Doğru: {true_answers}, Yanlış: {false_answers}, Net: {clear_answers}, Toplam: {total_answer}\n"
            )

        prompt += (
            "\nBu verilere dayanarak kullanıcı için öneriler oluştur:\n"
            "- Performansını artırmak için hangi konulara odaklanması gerektiğini belirt.\n"
            "- Hedefine ulaşmak için günlük/haftalık/aylık çalışma stratejilerini sun.\n"
        )

        try:
            suggestion_text = call_inference_api(prompt)
            response_data = {
                "uid": uid,
                "userField": user_field,
                "userGoal": user_goal,
                "type": type_of_analysis,
                "suggestion": suggestion_text
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Bir hata oluştu: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ExamResultsSuggestionView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Excel dosyasının tam yolunu belirleyin
        excel_file_path = os.path.join(
            settings.BASE_DIR,
            r"C:\Users\utku-\Desktop\KAGGLE\BTK Hackaton Django\hackhaton_btk\api\yks_excel_updated.xlsx"
        )

        try:
            df_original = pd.read_excel(excel_file_path)

            # Debug: Sütunları inceleyin
            print(">>> [INIT] Excel Columns:", df_original.columns.tolist())
            print(">>> [INIT] Excel Shape:", df_original.shape)

            # Normalleştirme (strip + lower) - Sütun düzeyinde
            df_original["Üniversite Adı"] = (
                df_original["Üniversite Adı"].astype(str).str.strip().str.lower()
            )
            df_original["Program Adı"] = (
                df_original["Program Adı"].astype(str).str.strip().str.lower()
            )

            # Artık self.df normalleştirilmiş bir DataFrame
            self.df = df_original

        except FileNotFoundError as e:
            raise FileNotFoundError(f"Excel dosyası bulunamadı: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Excel yüklenirken bir hata oluştu: {str(e)}")

    def post(self, request):
        """
        Kullanıcıdan gelen veriler doğrultusunda:
        1) userGoal ve lessonName normalleştirilir,
        2) Excel üzerinden ilgili satır bulunur,
        3) Performans analizi yapılır,
        4) create_prompt ile prompt oluşturulur,
        5) call_inference_api ile LLM'e istek atılır.
        """

        # 1) Request'ten verileri al
        user_data = request.data

        user_goal = user_data.get("userGoal", "")
        lesson_name = user_data.get("lessonName", "")
        lesson_data = user_data.get("lessonData", [])

        # 2) Gerekli alanların kontrolü
        if not user_goal or not lesson_name or not lesson_data:
            return Response(
                {
                    "error": "Gerekli alanlardan biri eksik: 'userGoal', 'lessonName', 'lessonData'."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3) Kullanıcı girdilerini normalleştir (küçült + boşluklar + parantez temizliği)
        user_goal_norm = (user_goal or "").lower().strip()
        user_goal_norm = user_goal_norm.replace("(", "").replace(")", "")

        lesson_name_norm = (lesson_name or "").lower().strip()
        lesson_name_norm = lesson_name_norm.replace("(", "").replace(")", "")

        # 4) Excel filtreleme (kısmi eşleşme: str.contains)
        target_row = self.df[
            (self.df["Üniversite Adı"].str.contains(user_goal_norm, na=False, regex=False)) &
            (self.df["Program Adı"].str.contains(lesson_name_norm, na=False, regex=False))
        ]

        if target_row.empty:
            return Response(
                {
                    "error": f"Hedef üniversite veya bölüm bulunamadı: {user_goal} - {lesson_name}"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # 5) Tek satır seçip sözlüğe dönüştür (ilk eşleşen satır)
        target_row_data = target_row.iloc[0].to_dict()

        # 6) Performans analizi
        try:
            total_true = sum(item["trueAnswers"] for item in lesson_data)
            total_answers = sum(item["totalAnswer"] for item in lesson_data)
            accuracy = (total_true / total_answers) * 100 if total_answers > 0 else 0
        except Exception as e:
            return Response(
                {"error": f"Performans analizi sırasında hata: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 7) Prompt oluşturma ve LLM çağrısı
        try:
            prompt = create_prompt(user_data, target_row_data, accuracy)
            suggestion_text = call_inference_api(prompt)
        except Exception as e:
            return Response(
                {"error": f"LLM çağrısı sırasında hata: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 8) Başarılı yanıt
        return Response({"suggestion": suggestion_text}, status=status.HTTP_200_OK)