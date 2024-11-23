import pandas as pd
import requests

# Excel dosyasını oku
excel_file_path = "C:\\Users\\utku-\\Desktop\\KAGGLE\\BTK Hackaton\\hackhaton_btk\\api\\yks_excel.xlsx"
df = pd.read_excel(excel_file_path)

# Sütun adlarını yazdır
print("Raw Columns:", df.columns.tolist())

# Sütun adlarını düzelt
df.columns = df.columns.str.strip().str.replace('Ã¼', 'ü').str.replace('Ã§', 'ç')

# Eğer bu yeterli olmazsa, normalize fonksiyonu ile karakterleri düzeltebiliriz
def normalize_string(s):
    return s.encode('latin1', 'replace').decode('utf-8', 'replace')

# Tüm sütun adlarını normalize et
df.columns = [normalize_string(col) for col in df.columns]

# Sütun adlarını kontrol et
print("Normalized Columns:", df.columns.tolist())

# API URL
api_url = "http://127.0.0.1:8000/api/yks-exam-results/"

# Her bir satırı POST isteği ile gönder
for index, row in df.iterrows():
    data = {
        "program_code": row['Program Kodu'],
        "university_type": row['Üniversites Türü'],
        "university_name": row['Üniversite Adı'],
        "faculty_name": row['Fakülte/Yüksekokul Adı'],
        "program_name": row['Program Adı'],
        "score_type": row['Puan Türü'],
        "kontenjan_0": row.get('Kontenjan', None),
        "yerlesen_0": row.get('Yerleşen', None),
        "min_score_0": row.get('En Küçük Puan', None),
        "max_score_0": row.get('En Büyük Puan', None),

        "kontenjan_1": row.get('Kontenjan.1', None),  # 1. yıl bilgileri
        "yerlesen_1": row.get('Yerleşen.1', None),
        "min_score_1": row.get('En Küçük Puan.1', None),
        "max_score_1": row.get('En Büyük Puan.1', None),

        "kontenjan_2": row.get('Kontenjan.2', None),  # 2. yıl bilgileri
        "yerlesen_2": row.get('Yerleşen.2', None),
        "min_score_2": row.get('En Küçük Puan.2', None),
        "max_score_2": row.get('En Büyük Puan.2', None),

        "kontenjan_3": row.get('Kontenjan.3', None),  # 3. yıl bilgileri
        "yerlesen_3": row.get('Yerleşen.3', None),
        "min_score_3": row.get('En Küçük Puan.3', None),
        "max_score_3": row.get('En Büyük Puan.3', None),

        "kontenjan_4": row.get('Kontenjan.4', None),  # 4. yıl bilgileri
        "yerlesen_4": row.get('Yerleşen.4', None),
        "min_score_4": row.get('En Küçük Puan.4', None),
        "max_score_4": row.get('En Büyük Puan.4', None),
    }

    # POST isteği gönder
    response = requests.post(api_url, json=data)

    if response.status_code == 201:
        print(f"Row {index} inserted successfully.")
    else:
        print(f"Failed to insert row {index}: {response.content}")
