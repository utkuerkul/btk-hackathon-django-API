from django.db import models

class ResultModel(models.Model):
    lessons = models.CharField(max_length=100)
    true_answers = models.IntegerField()
    false_answers = models.IntegerField()
    clear_answers = models.FloatField()

    def __str__(self):
        return f"{self.field} - True: {self.true_answers}, False: {self.false_answers}, Clear: {self.clear_answers}"


class ExamModel(models.Model):
    exam_type = models.CharField(max_length=100)
    date = models.DateField()
    result_list = models.ManyToManyField(ResultModel, related_name='exams')

    def __str__(self):
        return f"{self.exam_type} on {self.date}"


class DailyReportModelTYT(models.Model):
    date = models.DateField()
    daily_list = models.ManyToManyField(ResultModel, related_name='daily_reports_tyt')

    def __str__(self):
        return f"TYT Report on {self.date}"


class DailyReportModelAYT(models.Model):
    date = models.DateField()
    daily_list = models.ManyToManyField(ResultModel, related_name='daily_reports_ayt')

    def __str__(self):
        return f"AYT Report on {self.date}"

class APICall(models.Model):
    prompt = models.TextField()  # Gönderilen istek
    response = models.TextField()  # Alınan yanıt
    timestamp = models.DateTimeField(auto_now_add=True)  # İsteğin yapıldığı zaman

    def __str__(self):
        return f"API Call at {self.timestamp}"
    
class UserModel(models.Model):
    uid = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    birth_date = models.DateField()
    field = models.CharField(max_length=255)

    # İlişkiler için ForeignKey kullan
    daily_report_list_tyt = models.ManyToManyField(DailyReportModelTYT, related_name='users', blank=True)
    daily_report_list_ayt = models.ManyToManyField(DailyReportModelAYT, related_name='users', blank=True)

    def __str__(self):
        return f"{self.name} {self.surname}"

class UserActivitySuggestion(models.Model):

    # Kişisel Bilgiler
    uid = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    birth_date = models.DateField()
    study_field = models.CharField(max_length=100)  # Kullanıcının okuduğu bölüm veya alan

    # Günlük ve Haftalık Çalışma Alışkanlıkları
    daily_study_hours = models.FloatField()  # Günlük ders çalışma süresi

    goals = models.TextField(blank=True)  # Hedef

   
    # Akademik Performans Verileri
    gpa = models.FloatField(blank=True, null=True)  # Not ortalaması

    # Öneri Metni
    suggestion = models.TextField()

    def _str_(self):
        return f"{self.name} {self.surname} - Suggestion: {self.suggestion}" 
    
from django.db import models

class YKSExamResult(models.Model):
    program_code = models.CharField(max_length=100, verbose_name="Program Kodu")
    university_type = models.CharField(max_length=100, verbose_name="Üniversites Türü")
    university_name = models.CharField(max_length=255, verbose_name="Üniversite Adı")
    faculty_name = models.CharField(max_length=255, verbose_name="Fakülte/Yüksekokul Adı")
    program_name = models.CharField(max_length=255, verbose_name="Program Adı")
    score_type = models.CharField(max_length=50, verbose_name="Puan Türü")
    
    kontenjan_1 = models.IntegerField(null=True, blank=True, verbose_name="Kontenjan")
    yerlesen_1 = models.IntegerField(null=True, blank=True, verbose_name="Yerleşen")
    min_score_1 = models.FloatField(null=True, blank=True, verbose_name="En Küçük Puan")
    max_score_1 = models.FloatField(null=True, blank=True, verbose_name="En Büyük Puan")

    kontenjan_2 = models.IntegerField(null=True, blank=True, verbose_name="Kontenjan.1")
    yerlesen_2 = models.IntegerField(null=True, blank=True, verbose_name="Yerleşen.1")
    min_score_2 = models.FloatField(null=True, blank=True, verbose_name="En Küçük Puan.1")
    max_score_2 = models.FloatField(null=True, blank=True, verbose_name="En Büyük Puan.1")

    kontenjan_3 = models.IntegerField(null=True, blank=True, verbose_name="Kontenjan.2")
    yerlesen_3 = models.IntegerField(null=True, blank=True, verbose_name="Yerleşen.2")
    min_score_3 = models.FloatField(null=True, blank=True, verbose_name="En Küçük Puan.2")
    max_score_3 = models.FloatField(null=True, blank=True, verbose_name="En Büyük Puan.2")

    kontenjan_4 = models.IntegerField(null=True, blank=True, verbose_name="Kontenjan.3")
    yerlesen_4 = models.IntegerField(null=True, blank=True, verbose_name="Yerleşen.3")
    min_score_4 = models.FloatField(null=True, blank=True, verbose_name="En Küçük Puan.3")
    max_score_4 = models.FloatField(null=True, blank=True, verbose_name="En Büyük Puan.3")

    kontenjan_5 = models.IntegerField(null=True, blank=True, verbose_name="Kontenjan.4")
    yerlesen_5 = models.IntegerField(null=True, blank=True, verbose_name="Yerleşen.4")
    min_score_5 = models.FloatField(null=True, blank=True, verbose_name="En Küçük Puan.4")
    max_score_5 = models.FloatField(null=True, blank=True, verbose_name="En Büyük Puan.4")

    def __str__(self):
        return f"{self.program_name} - {self.university_name}"
