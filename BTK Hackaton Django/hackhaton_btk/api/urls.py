from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    ResultModelViewSet,
    YKSExamResultViewSet,
    ExamModelViewSet,
    ExamResultsSuggestionView,
    DailyReportModelTYTViewSet,
    DailyReportModelAYTViewSet,
    UserActivitySuggestionView,
    UserActivitySuggestionListView,
    upload_page
)

# Router oluştur
router = DefaultRouter()
router.register(r'results', ResultModelViewSet)
router.register(r'exams', ExamModelViewSet)
router.register(r'daily_reports_tyt', DailyReportModelTYTViewSet)
router.register(r'daily_reports_ayt', DailyReportModelAYTViewSet)
router.register(r'yks-exam-results', YKSExamResultViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin paneli
    path('api/', include(router.urls)),  # API yollarını buraya ekliyoruz
    path('user-suggestion/', UserActivitySuggestionView.as_view(), name='user-suggestion'),
    path('api/exam-results-suggestions/', ExamResultsSuggestionView.as_view(), name='exam-results-suggestions'),
    path('api/yks-exam-results/', YKSExamResultViewSet.as_view({'post': 'create'}), name='yks-exam-results'),
    path('upload/', upload_page, name='upload_page')
]
