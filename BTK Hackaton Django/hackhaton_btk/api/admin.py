from django.contrib import admin
from .models import ExamModel
from .models import APICall
from import_export.admin import ImportExportModelAdmin
from .models import YKSExamResult
from import_export import resources

admin.site.register(APICall)
admin.site.register(YKSExamResult,ImportExportModelAdmin)
