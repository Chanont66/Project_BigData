# !pip install pandas
import pandas as pd
import requests

url = "http://air4thai.pcd.go.th/services/getNewAQI_JSON.php"
data = requests.get(url).json()

# ข้อมูลอยู่ใน stations ต้องเข้าไปก่อน
stations = data['stations']


df = pd.json_normalize(stations)

# แยกข้อความด้วย , จะได้ list
province_split = df['areaEN'].str.split(', ') 

# เอาตัวสุดท้ายของ list
province_last = province_split.str[-1] 

# ตัดช่องว่างที่อยู่หน้าและหลังคำ
province_clean = province_last.str.strip() 


# แก้ชื่อจังหวัด
province_check = {
    "Chon buri": "Chon Buri",
    "Mueang Ang Thong District Ang Thong Province": "Ang Thong",
    "Pattanee": "Pattani",
    "Suphun Buri": "Suphan Buri",
    "Chang Wat Phetchaburi": "Phetchaburi",
    "Phra Nakhon Si Ayutthaya": "Ayutthaya",
}


# ใช้ replace แก้ชื่อที่เขียนมาแปลกๆ
df["province_clean"] = province_clean.replace(province_check)

# เอาชื่อจังหวัดที่ไม่ซ้ํา
# print(df['province_clean'].unique())






df_pm25 = df[['stationID', 'nameTH', 'province_clean', 'AQILast.PM25.value']]
print(df_pm25)






# ดูแถวแรกว่ามีกี่คอลัมน์
# print(stations[0])
# print(stations[0].keys())
# (['stationID', 'nameTH', 'nameEN', 'areaTH', 'areaEN', 'stationType', 'lat', 'long', 'forecast', 'AQILast'])