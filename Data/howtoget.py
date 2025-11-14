data = {'name': 'John', 'age': 25}

# วิธีปกติ - ใช้ []
# print(data['name'])  # ได้: John
# print(data['age'])  # ได้: 25

# # ใช้ .get() แทน
# print(data.get('name'))  # ได้: John
# print(data.get('city'))  # ได้: None (ไม่ error!)
# print(data.get('city', 'gg'))  # ได้: 'gg' , (ค่า default)



import requests
import pandas as pd
pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)

url = "http://air4thai.pcd.go.th/services/getNewAQI_JSON.php"
data = requests.get(url).json()

stations = data['stations']

df = pd.json_normalize(stations)
df['province'] = df['areaEN'].str.split(', ').str[-1]
print(df['province'].unique())