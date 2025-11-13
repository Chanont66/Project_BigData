# !pip install pandas
import pandas as pd
import json

with open('D:/ProjectOnGit/Project_BigData/Data/air4thai.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


stations = data['stations']

# ดูแถวแรก
# print(stations[0])