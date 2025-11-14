# !pip install pandas
import pandas as pd
import json

with open('D:/ProjectOnGit/Project_BigData/Data/air4thai.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# ข้อมูลอยู่ใน stations
stations = data['stations']


# ดูแถวแรกว่ามีกี่คอลัมน์
# print(stations[0])
# print(stations[0].keys())
# (['stationID', 'nameTH', 'nameEN', 'areaTH', 'areaEN', 'stationType', 'lat', 'long', 'forecast', 'AQILast'])

df_aqi = pd.json_normalize(data["AQILast"])


tabel = []
for i in range(len(stations)):
    tabel.append(stations[i]+df_aqi[i])

df = pd.DataFrame(tabel)
print(df)