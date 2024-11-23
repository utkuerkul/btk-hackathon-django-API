from django.shortcuts import render
from rest_framework import viewsets
from .models import ExamModel,YKSExamResult, ResultModel, DailyReportModelTYT, DailyReportModelAYT, UserActivitySuggestion, UserModel
from .serializers import ExamModelSerializer,YKSExamResultSerializer,ExamModelSerializer, ExamResultsRequestSerializer, ResultModelSerializer, DailyReportModelTYTSerializer, DailyReportModelAYTSerializer, UserModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RequestSerializer
from django.http import JsonResponse
import google.generativeai as genai 
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from tablib import Dataset
from .models import YKSExamResult
from .resources import YKSExamResultResource
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd 

class ResultModelViewSet(viewsets.ModelViewSet):
    queryset = ResultModel.objects.all()
    serializer_class = ResultModelSerializer

class UserModelViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer

class ExamModelViewSet(viewsets.ModelViewSet):
    queryset = ExamModel.objects.all()
    serializer_class = ExamModelSerializer

class DailyReportModelTYTViewSet(viewsets.ModelViewSet):
    queryset = DailyReportModelTYT.objects.all()
    serializer_class = DailyReportModelTYTSerializer

class DailyReportModelAYTViewSet(viewsets.ModelViewSet):
    queryset = DailyReportModelAYT.objects.all()
    serializer_class = DailyReportModelAYTSerializer

class YKSExamResultViewSet(viewsets.ModelViewSet):
    queryset = YKSExamResult.objects.all()
    serializer_class = YKSExamResultSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

genai.configure(api_key="AIzaSyBzz-mPuEHIEftIDogexuPLn5gy734ERgU")

# Model yapılandırma
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 5096,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def call_gemini_api(prompt):
    
    response = model.generate_content(prompt)
    return response

class UserActivitySuggestionView(APIView):
    def post(self, request):
        serializer = RequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_data = serializer.validated_data
        prompt = (
    f"Kullanıcı Bilgileri:\n"
    f"İsim: {user_data['name']}\n"
    f"Soyisim: {user_data['surname']}\n"
    f"Doğum Tarihi: {user_data['birth_date']}\n"
    f"Bölüm: {user_data['study_field']}\n"
    f"Günlük Ders Çalışma Süresi: {user_data['daily_study_hours']} saat\n"
    f"Uzun Vadeli Hedef: {user_data['goals']}\n"
    f"GPA (Not Ortalaması): {user_data['gpa']}\n\n"

    "Öğrencinin Başarı Hedefleri İçin Strateji Önerileri:\n"
    "1. **Çalışma Planı ve Rutin:** Kullanıcının günlük çalışma süresi ve hedefi göz önünde bulundurularak, "
    "verimli bir çalışma planı hazırlanmalı. Çalışma süresini optimum düzeyde kullanmasını sağlamalı.\n\n"
    
    "2. **TYT ve AYT Sınav Stratejileri:** Sınav hedeflerine göre, TYT'de hız kazanması, temel konuları gözden "
    "geçirmesi ve düzenli soru çözme pratiği yapması tavsiye edilir. AYT için ise ilgili alanlarda ileri seviye "
    "sorular çözerek zayıf konulara odaklanması önerilir.\n\n"
    
    "3. **Motivasyonun Güçlendirilmesi:** Kullanıcının belirttiği uzun vadeli hedeflerin yol haritasını "
    "oluşturacak motivasyon kaynakları sunulmalı. Hedef odaklılık sağlayacak haftalık kontrol noktaları ve "
    "hedef takip planları önerilmelidir.\n\n"
    
    "4. **Kendini Değerlendirme ve Gelişim:** Mevcut GPA bilgisi dikkate alınarak, akademik gelişimini destekleyecek "
    "çalışma alışkanlıkları ve kaynak önerileri sunulmalı. Öğrenilen bilgilerin kalıcılığını sağlamak için tekrar "
    "yöntemleri önerilmelidir.\n\n"
    
    "Bu adımları düşünerek öğrenciye TYT ve AYT başarılarını destekleyecek, uzun vadeli hedeflerine ulaşmasına yardımcı "
    "olacak kişisel öneriler sunulacaktır. Bu adımları tek tek yazmayarak sadece Öneri çıktısı verilecek. "
)


        try:
            gemini_response = call_gemini_api(prompt)
            suggestion_text = gemini_response.text

            user_suggestion = UserActivitySuggestion.objects.create(
                uid=user_data["uid"],
                name=user_data['name'],
                surname=user_data['surname'],
                birth_date=user_data['birth_date'],
                study_field=user_data['study_field'],
                daily_study_hours=user_data['daily_study_hours'],
                goals=user_data['goals'],
                gpa=user_data.get('gpa'),  # GPA boş olabilir, get kullanarak alınır
                suggestion=suggestion_text
            )

            response_data = {
                "uid": user_suggestion.uid,
                "name": user_suggestion.name,
                "surname": user_suggestion.surname,
                "birth_date": user_suggestion.birth_date,
                "study_field": user_suggestion.study_field,
                "daily_study_hours": user_suggestion.daily_study_hours,
                "goals": user_suggestion.goals,
                "gpa": user_suggestion.gpa,
                "suggestion": user_suggestion.suggestion
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": "Bir hata oluştu: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserActivitySuggestionListView(APIView):
    def get(self, request):
        suggestions = UserActivitySuggestion.objects.all()
        data = [
            {
                "uid": suggestion.uid,
                "name": suggestion.name,
                "surname": suggestion.surname,
                "birth_date": suggestion.birth_date,
                "study_field": suggestion.study_field,
                "daily_study_hours": suggestion.daily_study_hours,
                "goals": suggestion.goals,
                "gpa": suggestion.gpa,
                "suggestion": suggestion.suggestion
            }
            for suggestion in suggestions
        ]
        return Response(data, status=status.HTTP_200_OK)
    
class ExamResultsSuggestionView(APIView):
    def post(self, request):
        serializer = ExamResultsRequestSerializer(data=request.data)

        # Serializer doğrulama
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        exam_results_data = serializer.validated_data.get('exam_results')
        user_id = serializer.validated_data.get('user_id')

        # Kullanıcı hedefini alma
        try:
            user_activity = UserActivitySuggestion.objects.get(uid=user_id)
            user_goal = user_activity.goals  # Kullanıcının hedefi
        except UserActivitySuggestion.DoesNotExist:
            return Response({"error": "Kullanıcı bulunamadı."}, status=status.HTTP_404_NOT_FOUND)

        examsuggestions = []

        # Her ders için öneri oluşturma
        for result in exam_results_data:
            lesson_name = result.get('lessons')
            true_answers = result.get('true_answers', 0)
            false_answers = result.get('false_answers', 0)
            clear_answers = result.get('clear_answers', 0.0)
            exam_date = result.get('date')
            exam_type = result.get('exam_type')

            prompt = (
                f"{exam_date} tarihinde yapılan {exam_type} sınavında {lesson_name} dersinden {true_answers} doğru ve "
                f"{false_answers} yanlış cevap verildi. Net sayısı: {clear_answers}. "
                f"Kullanıcının hedefi: {user_goal} bölümüne yerleşmek. "

                f"Geçtiğimiz yıllardaki {exam_type} sınav sonuçlarına göre, {lesson_name} dersinde "
                f"{user_goal} bölümünü kazanan adayların net aralıkları, en düşük ve en yüksek net değerleri hakkında bilgi ver. "
                f"Kullanıcının mevcut performansını bu verilerle kıyaslayarak, hedeflenen net sayısına ulaşmak için hangi "
                f"konulara ve soru tiplerine odaklanması gerektiğini kısa önerilerle açıkla. Ayrıca, bu bölümü kazanmak için "
                f"geçmiş yıllarda ortalama kaç net doğrusu olan adayların başarı sağladığını belirt ve bu bilgilere dayanarak kullanıcıya "
                f"önerilerde bulun."
            )

            # API çağrısı
            try:
                gemini_response = call_gemini_api(prompt)
                suggestion_text = gemini_response.text.strip()  # Boşlukları temizle

                examsuggestions.append({
                    "lesson": lesson_name,
                    "exam_date": exam_date,
                    "exam_type": exam_type,
                    "goal": user_goal,
                    "suggestion": suggestion_text
                })

            except Exception as e:
                examsuggestions.append({
                    "lesson": lesson_name,
                    "exam_date": exam_date,
                    "exam_type": exam_type,
                    "goal": user_goal,
                    "suggestion": f"Hata: {str(e)}"
                })

        # Sonuçları JSON formatında döndür
        return Response({"examsuggestion": examsuggestions}, status=status.HTTP_200_OK)
    

class YKSExamResultViewSet(viewsets.ModelViewSet):
    queryset = YKSExamResult.objects.all()
    serializer_class = YKSExamResultSerializer
    parser_classes = (MultiPartParser, FormParser)  # Dosya yüklemek için gerekli parser'lar

    def create(self, request, *args, **kwargs):
        file = request.FILES.get('file') 
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Dosyayı pandas ile oku
        try:
            data = pd.read_excel(file)
            # Satırları YKSExamResult modeline ekle
            for _, row in data.iterrows():
                YKSExamResult.objects.create(
                    program_kodu=row['Program Kodu'],
                    universite_turu=row['Üniversites Türü'],
                    universite_adi=row['Üniversite Adı'],
                    # Diğer alanları buraya ekleyin
                )
            return Response({"status": "File uploaded and data saved"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
def upload_page(request):
    return render(request, 'upload.html')