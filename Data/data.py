# !pip install pandas
import pandas as pd
import requests

url = "http://air4thai.pcd.go.th/services/getNewAQI_JSON.php"
data = requests.get(url).json()
# ข้อมูลอยู่ใน stations
stations = data['stations']


# ดูแถวแรกว่ามีกี่คอลัมน์
# print(stations[0])
# print(stations[0].keys())
# (['stationID', 'nameTH', 'nameEN', 'areaTH', 'areaEN', 'stationType', 'lat', 'long', 'forecast', 'AQILast'])

df = pd.json_normalize(stations)
print(df)
