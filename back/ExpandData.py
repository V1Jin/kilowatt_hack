import json
import os
import random
import copy
import numpy as np

base_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(base_dir, "dataset_train.json"), "r", encoding="utf-8") as file:
    data = json.load(file)

def add_noise(value, noise_scale=0.1):
    if isinstance(value, (int, float)):
        noise = np.random.normal(0, noise_scale * abs(value))
        return max(0, value + noise)  # чтобы не было отрицательных значений
    return value

def generate_synthetic_data(original_data, num_copies=1, noise_scale=0.1):
    synthetic_data = []
    max_account_id = max(item["accountId"] for item in original_data)
    
    for item in original_data:
        for _ in range(num_copies):
            new_item = copy.deepcopy(item)
            
            max_account_id += 1
            new_item["accountId"] = max_account_id
            
            if ("roomsCount" in new_item.keys()): new_item["roomsCount"] = int(add_noise(new_item["roomsCount"], noise_scale)) + 1
            if ("residentsCount" in new_item.keys()): new_item["residentsCount"] = int(add_noise(new_item["residentsCount"], noise_scale)) + 1
            
            if "totalArea" in new_item:
                new_item["totalArea"] = round(add_noise(new_item["totalArea"], noise_scale), 2) + 1
            
            for month in new_item["consumption"]:
                new_item["consumption"][month] =int(add_noise(new_item["consumption"][month], noise_scale)) + 1
            
            synthetic_data.append(new_item)
    
    return synthetic_data

original_data = data
synthetic_data = generate_synthetic_data(original_data, num_copies=1, noise_scale=0.1)

data = data + synthetic_data

with open('dataset_train.json', "w", encoding="utf-8" ) as file:
    json.dump(data,file, indent=4, ensure_ascii=False)

# Вывод первого синтетического объекта
print(synthetic_data)