data = {'name': 'John', 'age': 25}

# วิธีปกติ - ใช้ []
# print(data['name'])  # ได้: John
# print(data['age'])  # ได้: 25

# # ใช้ .get() แทน
# print(data.get('name'))  # ได้: John
# print(data.get('city'))  # ได้: None (ไม่ error!)
print(data.get('city', 'gg'))  # ได้: 'gg' , (ค่า default)