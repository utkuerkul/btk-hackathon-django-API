# serializers.py

from rest_framework import serializers
from .models import (
    UserModel,
    YKSExamResult,
    ExamModel, 
    UserActivitySuggestion
)


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