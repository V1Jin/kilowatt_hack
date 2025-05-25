import tensorflow as tf
import matplotlib.pyplot as plt
import json
import os
from sklearn.preprocessing import StandardScaler
import numpy as np
import random

base_dir = os.path.dirname(os.path.abspath(__file__))

print(tf.__version__)

training_count = 28956 #4826
epochs = [35]
batchers = [64] 
learning_rates = [0.0001]
layers_list = [[128,0.2, 64,0.2,  32, 1]]


with open("dataset_train.json", encoding="utf-8") as file:
    train_data = json.load(file)

with open("dataset_test.json", encoding="utf-8") as file:
    test_data = json.load(file)

def maxis():
    maximus = {
        "roomsCount": 0,
        "roomsSum": 0,
        "residentsCount": 0,
        "residentsSum": 0,
        "totalArea": 0,
        "totalAreaSum": 0,
        "kilowattSum": 0 ,
        "kilowattCount": 0 
    }

    for i in train_data:
        if ("roomsCount" in i.keys()):
            maximus["roomsCount"] += 1
            maximus["roomsSum"] += i["roomsCount"]
        if ("residentsCount" in i.keys()):
            maximus["residentsCount"] += 1
            maximus["residentsSum"] += i["residentsCount"]
        if ("totalArea" in i.keys()):
            maximus["totalArea"] += 1
            maximus["totalAreaSum"] += i["totalArea"]
        maximus["kilowattSum"] += sum(list(i["consumption"].values()))
        maximus["kilowattCount"] += len(list(i["consumption"].values()))
    return maximus

maximus = maxis()
print(maximus)
maximus["roomsAvg"] = maximus["roomsSum"]/maximus["roomsCount"]
maximus["residentsAvg"] = maximus["residentsSum"]/maximus["residentsCount"]
maximus["totalAreaAvg"] = maximus["totalAreaSum"]/maximus["totalArea"]
maximus["kilowattAvg"] = maximus["kilowattSum"]/maximus["kilowattCount"]

print(maximus)

# физич. где то до 1500 - 3000, юрлиц до беск.
#{'roomsCount': 48, 'residentsCount': 19, 'totalArea': 80895.0, 'kilowatt': 446670}
#{'roomsCount': 4343, 'roomsSum': 13142, 'residentsCount': 4159, 'residentsSum': 10035, 'totalArea': 2800, 'totalAreaSum': 1033988.1600000001, 'kilowattSum': 169518176, 'kilowattCount': 54942, 'roomsAvg': 3.026018880957863, 'residentsAvg': 2.412839624909834, 'totalAreaAvg': 369.2814857142858, 'kilowattAvg': 3085.402351570747}
# print(maxis())
def normalize_data(data):

    types = ["Частный", "Многоквартирный", "Прочий", "Сарай", "Дача", "Гараж"]
    building_type_one_hot = tf.one_hot(types.index(data["buildingType"]), depth=6, dtype=tf.float32)  
    lister = [data["consumption"][str(x)]/maximus["kilowattAvg"] - 1 if str(x) in list(data["consumption"].keys()) else 0 for x in range(1,13)]
    # print(lister)
    query_data = tf.constant([
        0 if "roomsCount" not in data.keys() else data["roomsCount"]/maximus["roomsAvg"] - 1,
        0 if "residentsCount" not in data.keys() else data["residentsCount"]/maximus["residentsAvg"] - 1,
        0 if "totalArea" not in data.keys() else data["totalArea"]/maximus["totalAreaAvg"] - 1,
    ] + lister, dtype=tf.float32)
    query_data = tf.concat([tf.reshape(building_type_one_hot, [1, -1]), 
                          tf.reshape(query_data, [1, -1])], axis=1)

    query_data = tf.reshape(query_data, (1, -1))
    return query_data

mock = {
            "accountId": 1497,
            "isCommercial": True,
            "address": "Краснодарский край, р-н Мостовский, пгт Мостовской, ул Колхозная, д. 37 1",
            "buildingType": "Частный",
            "roomsCount": 1,
            "residentsCount": 1,
            "consumption": {
                "1": 3484,
                "2": 2824,
                "3": 3035,
                "4": 3597,
                "5": 2664,
                "6": 3874,
                "7": 3270,
                "8": 3714,
                "9": 3124,
                "10": 2981,
                "11": 2923,
                "12": 2216
            }
        }

# label = tf.constant([0], dtype=tf.float32)

# mock = tf.reshape(mock, (1, -1))

# print (mock.shape)


def create_model(learning_rate, layers, activation_function):

    

    keras_layers = []
    for i in layers[:-1]:
        if abs(i) <= 1:
            keras_layers.append(tf.keras.layers.Dropout(i))
        else: 
            keras_layers.append(tf.keras.layers.Dense(i, activation=activation_function, input_shape=(21,)))
            # keras_layers.append(tf.keras.layers.BatchNormalization())
    keras_layers.append(tf.keras.layers.Dense(1, activation='sigmoid'))
    # 2. Создание модели
    # model = tf.keras.Sequential([
    #     tf.keras.layers.Dense(64, activation='relu', input_shape=(16,)),
    #     # tf.keras.layers.Dropout(0.2),
    #     # tf.keras.layers.Dense(32, activation='sigmoid'),
    #     tf.keras.layers.Dense(1, activation='sigmoid')
    # ])
    print(keras_layers)
    model = tf.keras.Sequential(keras_layers)

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss='binary_crossentropy', 
        metrics=['accuracy']
    )

    return model

# Обучение

def get_stat():
    maxi, maxi_avg, maxi_name, maxi_avg_name = 0, 0, 0, 0
    comprasion = {} # конечноe, лучшее, среднее
    iterator = 0
    for batch_size in batchers:
        for epoch in epochs:
            for lr in learning_rates:
                for layers in layers_list:
                    # layers = [64, 0.2, 1] # последний - всегда 1
                    layers_count = len([x for x in layers if x > 1])
                    active_func = "relu"
                    model = create_model(lr, layers=layers, activation_function=active_func)


                    # преобразуем данные
                    query_train_data = []
                    query_train_data_labels = []

                    for i in range(len(train_data[:training_count])):
                        label = tf.constant([1] if train_data[i]["isCommercial"] == True else [0], dtype=tf.float32) 
                        normal_train_data = normalize_data(train_data[i])
                        query_train_data.append(normal_train_data)
                        query_train_data_labels.append(label)
                    query_train_data = tf.concat(query_train_data, axis=0)
                    query_train_data_labels = tf.concat(query_train_data_labels, axis=0)


                    early_stopping = tf.keras.callbacks.EarlyStopping(
                                        monitor='val_accuracy',  # Метрика для мониторинга (val_loss, val_accuracy и т. д.)
                                        patience=5,         # Сколько эпох ждать улучшения
                                        restore_best_weights=True,  # Восстановить веса лучшей модели
                                        verbose=1
                                    )
                    

                    history = model.fit(
                        query_train_data,
                        query_train_data_labels,
                        epochs=epoch,
                        batch_size=batch_size,
                        verbose=1,
                        validation_split = 0.2,
                        callbacks=[early_stopping]
                        )


                    model.save("my_model.keras")

                    print(history.history)

                    name = f'model {layers_count} layers {layers},  batch = {batch_size}, epochs = {epoch}, learningRate = {lr}, activation = {active_func}'

                    # 1. График точности
                    plt.figure(iterator, figsize=(12, 5))
                    plt.subplot(1, 2, 1)
                    plt.plot(history.history['accuracy'], label='Train Accuracy')
                    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
                    plt.title('Model Accuracy')
                    plt.ylabel('Accuracy')
                    plt.xlabel('Epoch')
                    plt.legend(loc='lower right')

                    # 2. График потерь
                    plt.subplot(1, 2, 2)
                    plt.plot(history.history['loss'], label='Train Loss')
                    plt.plot(history.history['val_loss'], label='Validation Loss')
                    plt.title('Model Loss')
                    plt.ylabel('Loss')
                    plt.xlabel('Epoch')
                    plt.legend(loc='upper right')
                    plt.suptitle(name, fontsize=16)

                    plt.tight_layout()


                    comprasion[name] = history.history.copy()
                    comprasion[name]["avg"] = sum(history.history["accuracy"])/len(history.history["accuracy"])
                    comprasion[name]["max"] = max(history.history["accuracy"])
                    if (comprasion[name]["max"] > maxi):
                        maxi =  comprasion[name]["max"]
                        maxi_name = name
                    if (comprasion[name]["avg"] > maxi_avg):
                        maxi_avg =  comprasion[name]["avg"]
                        maxi_avg_name = name
                    plt.savefig(os.path.join(base_dir, "graphs", name) + ".png")
                    
                    query = {
                                "accountId": 1497,
                                "isCommercial": True,
                                "address": "Краснодарский край, р-н Мостовский, пгт Мостовской, ул Колхозная, д. 37 1",
                                "buildingType": "Частный",
                                "roomsCount": 1,
                                "residentsCount": 1,
                                "consumption": {
                                    "1": 3484,
                                    "2": 2824,
                                    "3": 3035,
                                    "4": 3597,
                                    "5": 2664,
                                    "6": 3874,
                                    "7": 3270,
                                    "8": 3714,
                                    "9": 3124,
                                    "10": 2981,
                                    "11": 2923,
                                    "12": 2216
                                }
                            }

                    # prediction = model.predict(normalize_data(query))
                    # print(prediction.tolist())

                    # тестируем сеть

                    # преобразуем данные 
                    query_test_data = []
                    query_test_data_labels = []

                    for i in range(len(test_data)):
                        label = tf.constant([1] if test_data[i]["isCommercial"] == True else [0], dtype=tf.float32) 
                        normal_test_data = normalize_data(test_data[i])
                        query_test_data.append(normal_test_data)
                        query_test_data_labels.append(label)
                    query_test_data = tf.concat(query_test_data, axis=0)
                    query_test_data_labels = tf.concat(query_test_data_labels, axis=0)

                    accuracy, loss = model.evaluate(query_test_data, query_test_data_labels, verbose = 1)
                    print(f'Validation Accuracy: {accuracy}, Loss: {loss}')




                    iterator += 1

    with open("comprasion.json","w+", encoding="utf-8") as file:
        json.dump(comprasion, file, indent=4, ensure_ascii=False)


    print(f"\nМаксимальное среднее = {maxi_avg} у Модели: {maxi_avg_name}.\nМаксимальное {maxi} У Модели: {maxi_name}")

# print(normalize_data(mock))
# plt.show()
# get_stat()


def test_model():
    loaded_model = tf.keras.models.load_model("my_model.keras")


    result = {
        "correct": 0,
        "incorrect":0
    }
    for m in range(len(test_data)):
        prediction = loaded_model.predict(normalize_data(test_data[m]))
        print(f"PREDICTION = {prediction.tolist()}, REAL = {test_data[m]["isCommercial"]}")
        if (prediction.tolist()[0][0] >=0.5 and test_data[m]["isCommercial"] == True or prediction.tolist()[0][0] <0.5 and test_data[m]["isCommercial"] == False):
            result["correct"]+= 1
        else: result["incorrect"]+= 1

    result["stat_correct"] = result["correct"]/(result["correct"] + result["incorrect"]) * 100
    print(result)

# test_model()

def return_predictions(data):
    loaded_model = tf.keras.models.load_model("my_model.keras")

    result = []

    for i in range(len(data)):
        result.append(data[i].copy())

        prediction = loaded_model.predict(normalize_data(data[i]))
        if (prediction.tolist()[0][0] >=0.5):
            result[i]["isCommercial"] = True
        else:
            result[i]["isCommercial"] = False
        result[i]["prediction"] = prediction.tolist()[0][0]
    
    return result

with open("data_test_without_label.json", "r", encoding="utf-8") as file:
    data = json.load(file)

with open("data_test_without_label.json", "w", encoding="utf-8") as file:
    json.dump(return_predictions(data),file, indent=4, ensure_ascii=False)

# файл сравнения

# print(f"before {train_data[0]}")
# print(f"after {normalize_data(train_data[0])}")
# {
#         "accountId": 2589,
#         "isCommercial": false,
#         "address": "Краснодарский край, г Сочи, с Веселое, пер Короткий, д. 9 А",
#         "buildingType": ['Прочий', 'Сарай', 'Частный', 'Дача', 'Многоквартирный', 'Гараж']
#         "roomsCount": 2,
#         "residentsCount": 3,
#         "totalArea": 76.40,
#         "consumption": {
#             "1": 1911,
#             "2": 1827,
#             "3": 1506,
#             "4": 1248,
#             "5": 1534,
#             "6": 1154,
#             "7": 1599,
#             "8": 1528,
#             "9": 1444,
#             "10": 1250,
#             "11": 1156,
#             "12": 1028
#         }
#     }