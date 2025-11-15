# pip install pandas
# pip install requests
import pandas as pd
import requests


# ปรับข้อมูล (แก้ชื่อจังหวัดที่เขียนผิด, ลบช่องว่าง)
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
    
    # (เช็ตว่าครบ 77 จังหวัดไหม?)
    # print(df['province_clean'].unique())
    return df


# print(clean_data(df))
# ดูแถวแรกว่ามีกี่คอลัมน์
# print(stations[0].keys())


# หาค่าเฉลี่ย ค่า pm25 ของแต่ละจังหวัด
def find_mean(df):
    # แปลง Text ของค่า pm เป็นเลข
    df["AQILast.PM25.value"] = df["AQILast.PM25.value"].astype(float)

    # หาค่าเฉลี่ย
    result = df.groupby("province_clean")["AQILast.PM25.value"].mean()
    
    # จัดลำดับ
    result = result.sort_values(ascending=False)

    # แปลงเป็น dataframe (เพราะพอผ่าน groupby แล้วมันเป็น series)
    result = result.reset_index()

    return result


# print(findmean(clean_data(df)))



# ดึง api dataset
def fetch_data():
    url = "http://air4thai.pcd.go.th/services/getNewAQI_JSON.php"
    data = requests.get(url).json()

    # ข้อมูลอยู่ใน stations ต้องเข้าไปก่อน
    stations = data['stations']

    # แปลง json เป็น dataframe
    df = pd.json_normalize(stations)

    # ปรับข้อมูล (แก้ชื่อจังหวัดที่เขียนผิด, ลบช่องว่าง)
    df_clean = clean_data(df)

    # หาค่าเฉลี่ย ค่า pm25 ของแต่ละจังหวัด
    df_mean = find_mean(df_clean)

    # # แปลงเป็น list แบบ tuple (list ที่มีลำดับชัดเจน เพราะ js ไม่สนลำดับตอนแสดง)
    dataList = list(df_mean.itertuples(index=False, name=None))

    return dataList
    # return df_mean.info()

# print(fetch_data())