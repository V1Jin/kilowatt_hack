import json
import sqlite3
import os 

base_dir = os.path.dirname(os.path.abspath(__file__))

# Устанавливаем соединение с базой данных SQLite
conn = sqlite3.connect('buildings.db')
cursor = conn.cursor()

# Создаем таблицу (типы данных SQLite немного отличаются от MySQL)
cursor.execute("""
CREATE TABLE IF NOT EXISTS buildings (
    accountId INTEGER PRIMARY KEY,
    isCommercial BOOLEAN,
    address TEXT,
    buildingType TEXT,
    roomsCount INTEGER,
    residentsCount INTEGER,
    totalArea REAL,
    consumption TEXT,
    prediction REAL
)
""")

# Загружаем данные из JSON файла
with open(os.path.join(base_dir, 'dataset_train.json'), 'r', encoding='utf-8') as file:
    data = json.load(file)

# Вставляем данные в таблицу
for entry in data:
    accountId = entry.get("accountId")
    isCommercial = entry.get("isCommercial", False)
    address = entry.get("address", "")
    buildingType = entry.get("buildingType", "")
    roomsCount = entry.get("roomsCount")
    residentsCount = entry.get("residentsCount")
    totalArea = entry.get("totalArea")
    consumption = json.dumps(entry.get("consumption", {}), ensure_ascii=False)
    prediction = entry.get("prediction")

    # SQLite использует другой синтаксис для INSERT OR REPLACE вместо ON DUPLICATE KEY UPDATE
    cursor.execute("""
        INSERT OR REPLACE INTO buildings (
            accountId, isCommercial, address, buildingType,
            roomsCount, residentsCount, totalArea, consumption, prediction
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (accountId, isCommercial, address, buildingType,
          roomsCount, residentsCount, totalArea, consumption, prediction))

# Сохраняем изменения и закрываем соединение
conn.commit()
cursor.close()
conn.close()