from django.db import models
from django.utils.timezone import now

class UserModel(models.Model):
    uid = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    birth_date = models.DateField()
    field = models.CharField(max_length=255)
    goal = models.TextField(blank=True)  # Kullanıcının hedefi

    def __str__(self):
        return f"{self.name} {self.surname}"


class LessonData(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="lesson_data")
    lesson_name = models.CharField(max_length=100)
    true_answers = models.IntegerField()
    false_answers = models.IntegerField()
    clear_answers = models.FloatField()
    total_answers = models.IntegerField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.lesson_name} - {self.date} - Net: {self.clear_answers}"

class ExamModel(models.Model):
    exam_type = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return f"{self.exam_type} on {self.date}"

class UserActivitySuggestion(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="suggestions")
    analysis_type = models.CharField(
        max_length=50,
        choices=[
            ("daily", "Günlük"),
            ("weekly", "Haftalık"),
            ("mock", "Deneme"),
        ],
        default="daily",
    )
    suggestion = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return f"{self.user} - {self.analysis_type} Suggestion"


class APICall(models.Model):
    prompt = models.TextField()  # Gönderilen istek
    response = models.TextField()  # Alınan yanıt
    timestamp = models.DateTimeField(auto_now_add=True)  # İsteğin yapıldığı zaman

    def __str__(self):
        return f"API Call at {self.timestamp}"


class YKSExamResult(models.Model):
    program_code = models.CharField(max_length=100, verbose_name="Program Kodu")
    university_type = models.CharField(max_length=100, verbose_name="Üniversite Türü")
    university_name = models.CharField(max_length=255, verbose_name="Üniversite Adı")
    faculty_name = models.CharField(max_length=255, verbose_name="Fakülte/Yüksekokul Adı")
    program_name = models.CharField(max_length=255, verbose_name="Program Adı")
    score_type = models.CharField(max_length=50, verbose_name="Puan Türü")
    min_score = models.FloatField(null=True, blank=True, verbose_name="En Küçük Puan")
    max_score = models.FloatField(null=True, blank=True, verbose_name="En Büyük Puan")

    def __str__(self):
        return f"{self.program_name} - {self.university_name}"
