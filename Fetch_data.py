# !pip install pandas
import pandas as pd
import requests

url = "http://air4thai.pcd.go.th/services/getNewAQI_JSON.php"
data = requests.get(url).json()

# ข้อมูลอยู่ใน stations ต้องเข้าไปก่อน
stations = data['stations']

# แปลง json เป็น dataframe
df = pd.json_normalize(stations)



# ปรับข้อมูล (แก้ชื่อจังหวัดที่เขียนผิด, ลบช่องว่าง, แปลง Text เป็นเลข)
def clean_data(df):
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

    # แปลง Text ของค่า pm เป็นเลข
    df["AQILast.PM25.value"] = df["AQILast.PM25.value"].astype(float)
    
    # (เช็ตว่าครบ 77 จังหวัดไหม?)
    # print(df['province_clean'].unique())
    return df


# print(clean_data(df))
# ดูแถวแรกว่ามีกี่คอลัมน์
# print(stations[0].keys())


# หาค่าเฉลี่ย ค่า pm25 ของแต่ละจังหวัด
def findmean(df):
    result = df.groupby('province_clean')['AQILast.PM25.value'].mean().sort_values()
    return result


# print(findmean(clean_data(df)))