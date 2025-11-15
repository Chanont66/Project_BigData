# pip install pandas
# pip install requests
# # pip install matplotlib
import pandas as pd
import requests
import matplotlib.pyplot as plt # ใช้วาดกราฟ



# แก้ชื่อจังหวัดที่เขียนผิด, ลบช่องว่าง 
# method ---> ให้ คอลัม province_clean ใน dataframe ที่ส่งมา
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

    # ใช้ replace แก้ชื่อที่เขียนมาแปลกๆ แล้วเก็บเป็น คอลัมน์ใหม่ของ dataframe
    df["province_clean"] = province_clean.replace(province_check)
    
    # (เช็ตว่าครบ 77 จังหวัดไหม?)
    # print(df['province_clean'].unique())
    return df






# หาค่าเฉลี่ย ค่า pm25 ของแต่ละจังหวัด 
# method ---> ให้ dataframe province_clean, AQILast.PM25.value
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



# ดึง api dataset และ ปรับข้อมูล 
# method ---> ให้ dataframe ข้อมูลทั้งหมด
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

    # print(stations[0].keys()) # ดูแถวแรกว่ามีกี่คอลัมน์
    return df_mean

# print(fetch_data())



# แปลงเป็น list แบบ tuple ไช้ใน app
# method ---> ให้ list แบบ tuple
def fetch_data_ListTuple():
    # ขอข้อมูลที่คลีนแล้ว คิด mean แล้ว
    fetch_D = fetch_data()

    # แปลงเป็น list แบบ tuple (list ที่มีลำดับชัดเจน เพราะ js ไม่สนลำดับตอนแสดง)
    dataList = list(fetch_D.itertuples(index=False, name=None))

    return dataList

# print(fetch_data_ListTuple())




# วาดกราฟแท่ง
# method ---> ให้รูป bar ไปในไฟล์ pic
def barplot():
    # ฟอนต์ไว้เขียน ภาษาไทย
    plt.rcParams['font.family'] = 'Tahoma'

    # ขอข้อมูลที่คลีนแล้ว คิด mean แล้ว
    fetch_D = fetch_data()
    
    # เอา dataframe มาวาดกราฟแบบง่ายๆ
    fetch_D.set_index("province_clean")['AQILast.PM25.value'].plot.bar(figsize=(20, 10))

    # ชื่อกราฟ, แกน x, แกน y
    plt.title("ค่า PM2.5 เฉลี่ยตามจังหวัด")
    plt.xlabel("จังหวัด")
    plt.ylabel("ค่า PM2.5 (µg/m³)")

    # หมุนชื่อจังหวัดให้ไม่ชนกัน
    plt.xticks(rotation=90)  

    # จัดระยะให้ไม่ทับกัน
    plt.tight_layout()

    # save graph (ถ้าข้อมูลอัพเดท มันจะทับรูปเก่า)
    plt.savefig('pic/pm25_barplot.png')

# barplot()



# วาดกราฟการกระจาย
# method ---> ให้รูป scatter ไปในไฟล์ pic
def scatterplot():
    # ฟอนต์ไว้เขียน ภาษาไทย
    plt.rcParams['font.family'] = 'Tahoma'

    # ขอข้อมูลที่คลีนแล้ว คิด mean แล้ว
    fetch_D = fetch_data()
    
    # เอา dataframe มาวาดกราฟแบบง่ายๆ
    fetch_D.plot.scatter(x='province_clean', y='AQILast.PM25.value', figsize=(20, 10))

    # ชื่อกราฟ, แกน x, แกน y
    plt.title("ค่า PM2.5 เฉลี่ยตามจังหวัด")
    plt.xlabel("จังหวัด")
    plt.ylabel("ค่า PM2.5 (µg/m³)")

    # หมุนชื่อจังหวัดให้ไม่ชนกัน
    plt.xticks(rotation=90)  

    # จัดระยะให้ไม่ทับกัน
    plt.tight_layout()

    # save graph (ถ้าข้อมูลอัพเดท มันจะทับรูปเก่า)
    plt.savefig('pic/pm25_scatterplot.png')

# scatterplot()




# วาดกราฟกล่อง
# method ---> ให้รูป box ไปในไฟล์ pic
def boxplot():
    # ฟอนต์ไว้เขียน ภาษาไทย
    plt.rcParams['font.family'] = 'Tahoma'

    # ขอข้อมูลที่คลีนแล้ว คิด mean แล้ว
    fetch_D = fetch_data()
    
    # เอา dataframe มาวาดกราฟแบบง่ายๆ
    df_clean.boxplot(column='AQILast.PM25.value', by='province_clean', figsize=(20, 10))

    # ชื่อกราฟ, แกน x, แกน y
    plt.title("ค่า PM2.5 เฉลี่ยตามจังหวัด")
    plt.ylabel("ค่า PM2.5 (µg/m³)")

    # หมุนชื่อจังหวัดให้ไม่ชนกัน
    plt.xticks(rotation=90)

    # จัดระยะให้ไม่ทับกัน
    plt.tight_layout()

    # save graph (ถ้าข้อมูลอัพเดท มันจะทับรูปเก่า)
    plt.savefig('pic/pm25_boxplot.png')

boxplot()