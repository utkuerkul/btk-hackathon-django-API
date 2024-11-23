# serializers.py

from rest_framework import serializers
from .models import (
    UserModel,
    YKSExamResult,
    ExamModel, 
    ResultModel, 
    DailyReportModelTYT, 
    DailyReportModelAYT, 
    UserActivitySuggestion
)

class ResultModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultModel
        fields = '__all__'  # Tüm alanları dahil etmek için '__all__' kullanıyoruz

class ExamModelSerializer(serializers.ModelSerializer):
    result_list = ResultModelSerializer(many=True)  # İlişkili result listesi

    class Meta:
        model = ExamModel
        fields = '__all__'

class DailyReportModelTYTSerializer(serializers.ModelSerializer):
    daily_list = ResultModelSerializer(many=True)

    class Meta:
        model = DailyReportModelTYT
        fields = '__all__'

class DailyReportModelAYTSerializer(serializers.ModelSerializer):
    daily_list = ResultModelSerializer(many=True)

    class Meta:
        model = DailyReportModelAYT
        fields = '__all__'

class UserModelSerializer(serializers.ModelSerializer):
    daily_report_list_tyt = DailyReportModelTYTSerializer(many=True, read_only=True)
    daily_report_list_ayt = DailyReportModelAYTSerializer(many=True, read_only=True)

    class Meta:
        model = UserModel
        fields = [
            'uid', 
            'name', 
            'surname', 
            'birth_date', 
            'field', 
            'daily_report_list_tyt', 
            'daily_report_list_ayt'
        ]

class UserActivitySuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivitySuggestion
        fields = '__all__'  # Tüm alanları dahil ediyoruz

class RequestSerializer(serializers.Serializer):
    uid = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=100)
    surname = serializers.CharField(max_length=100)
    birth_date = serializers.DateField()
    study_field = serializers.CharField(max_length=100)
    daily_study_hours = serializers.FloatField()
    goals = serializers.CharField(allow_blank=True)
    gpa = serializers.FloatField(required=False, allow_null=True)

class ExamResultSerializer(serializers.Serializer):
    lessons = serializers.CharField(max_length=100)  # Ders adı
    true_answers = serializers.IntegerField(required=True)  # Doğru cevap sayısı
    false_answers = serializers.IntegerField(required=True)  # Yanlış cevap sayısı
    clear_answers = serializers.FloatField(required=True)  # Net cevap sayısı
    date = serializers.DateField(required=True)  # Tarih
    exam_type = serializers.ChoiceField(
        choices=[("TYT", "TYT"), ("AYT", "AYT")], 
        required=True  # Sınav türü zorunlu
    )

class ExamResultsRequestSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=255, required=True)  # Kullanıcı kimliği
    exam_results = serializers.ListField(
        child=ExamResultSerializer(),  # Burada özel serializer kullanıyoruz
        required=True  # Sınav sonuçları zorunlu
    )

class YKSExamResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = YKSExamResult
        fields = '__all__'