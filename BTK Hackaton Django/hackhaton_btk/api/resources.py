from import_export import resources
from .models import YKSExamResult

class YKSExamResultResource(resources.ModelResource):
    class Meta:
        model = YKSExamResult
