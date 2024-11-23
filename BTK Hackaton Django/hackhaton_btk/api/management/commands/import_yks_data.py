import pandas as pd
from django.core.management.base import BaseCommand
from api.models import YKSExamResult

class Command(BaseCommand):
    help = 'YKS Excel verilerini veritabanına yükler'

    def handle(self, *args, **options):
        # Excel dosyasını pandas ile oku
        df = pd.read_excel('path_to_your_file/yks_excel.xlsx')

        # Satırları iterasyona sok ve her satırı veritabanına kaydet
        for _, row in df.iterrows():
            YKSExamResult.objects.create(
                program_code=row['Program Kodu'],
                university_type=row['Üniversites Türü'],
                university_name=row['Üniversite Adı'],
                faculty_name=row['Fakülte/Yüksekokul Adı'],
                program_name=row['Program Adı'],
                score_type=row['Puan Türü'],
                kontenjan_0=row['Kontenjan'],
                yerlesen_0=row['Yerleşen'],
                min_score_0=row['En Küçük Puan'],
                max_score_0=row['En Büyük Puan'],
                kontenjan_1=row['Kontenjan.1'],
                yerlesen_1=row['Yerleşen.1'],
                min_score_1=row['En Küçük Puan.1'],
                max_score_1=row['En Büyük Puan.1'],
                kontenjan_2=row['Kontenjan.2'],
                yerlesen_2=row['Yerleşen.2'],
                min_score_2=row['En Küçük Puan.2'],
                max_score_2=row['En Büyük Puan.2'],
                kontenjan_3=row['Kontenjan.3'],
                yerlesen_3=row['Yerleşen.3'],
                min_score_3=row['En Küçük Puan.3'],
                max_score_3=row['En Büyük Puan.3'],
                kontenjan_4=row['Kontenjan.4'],
                yerlesen_4=row['Yerleşen.4'],
                min_score_4=row['En Küçük Puan.4'],
                max_score_4=row['En Büyük Puan.4']
            )
        self.stdout.write(self.style.SUCCESS('Veriler başarıyla yüklendi.'))