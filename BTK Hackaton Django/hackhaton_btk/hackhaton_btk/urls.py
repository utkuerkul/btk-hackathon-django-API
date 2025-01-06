from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    ExamResultsSuggestionView,
    UserActivitySuggestionView,

)

# Router oluştur
router = DefaultRouter()
urlpatterns = [
    path('admin/', admin.site.urls),  # Admin paneli
    path('api/', include(router.urls)),  # Router için yollar eklendi
    path('api/user-suggestion/', UserActivitySuggestionView.as_view(), name='user-suggestion'),
    path('api/exam-results-suggestions/', ExamResultsSuggestionView.as_view(), name='exam-results-suggestions'),]