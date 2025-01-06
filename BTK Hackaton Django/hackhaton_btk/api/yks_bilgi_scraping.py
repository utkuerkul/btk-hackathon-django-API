import requests
import bs4
import pandas as pd

url = "https://yokatlas.yok.gov.tr/content/lisans-dynamic/1210a.php?y={program_kodu}"

# Program bilgilerini çekmek için fonksiyon
def extract_program_info(program_kodu):
    response = requests.get(url.format(program_kodu=program_kodu))
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    tbody = soup.find('tbody')
    rows = tbody.find_all('tr') if tbody else []
    program_data = {}
    for row in rows:
        tds = row.find_all('td')[:2]
        if len(tds) == 2:
            key = tds[0].text.strip()
            value = tds[1].text.strip()
            program_data[key] = value
    return program_data

# Mevcut yks_excel dosyasını yükleme
yks_excel_path = r"C:\Users\utku-\Desktop\KAGGLE\BTK Hackaton Django\hackhaton_btk\api\yks_excel.xlsx"
yks_df = pd.read_excel(yks_excel_path)

# Bilgileri çekip yeni bir DataFrame oluşturma
all_program_data = []
for program_kodu in yks_df['Program Kodu']:
    program_info = extract_program_info(program_kodu)
    program_info['Program Kodu'] = program_kodu  # Program kodunu ekleyelim
    all_program_data.append(program_info)
    # Çekilen verileri yazdırma
    print(f"Program Kodu: {program_kodu}")
    for key, value in program_info.items():
        print(f"{key}: {value}")
    print("-" * 40)

# Çekilen bilgileri DataFrame'e dönüştürme
extended_df = pd.DataFrame(all_program_data)

# Çekilen bilgileri mevcut DataFrame ile birleştirme
merged_df = pd.merge(yks_df, extended_df, on='Program Kodu', how='left')

# Güncellenmiş DataFrame'i Excel dosyasına kaydetme
output_file = r"C:\Users\utku-\Desktop\KAGGLE\BTK Hackaton Django\hackhaton_btk\api\yks_excel_updated.xlsx"
merged_df.to_excel(output_file, index=False)

print(f"Bilgiler '{output_file}' dosyasına başarıyla eklendi.")
