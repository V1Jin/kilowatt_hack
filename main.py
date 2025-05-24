import tensorflow as tf
import matplotlib.pyplot as plt
import json
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

print(tf.__version__)

training_count = 4826
epochs = [20]
batchers = [32]
learning_rates = [0.0005]
layers_list = [[64, 0.2, 1]]


with open("dataset_train.json", encoding="utf-8") as file:
    train_data = json.load(file)

with open("dataset_test.json", encoding="utf-8") as file:
    test_data = json.load(file)


def normalize_data(data):

    type_mapping = {
        "Частный": 1,
        "Многоквартирный": 2,
        "Прочий": 3,
        "Сарай": 4,
        "Дача": 5,
        "Гараж": 6
    }

    lister = [data["consumption"][str(x)] if str(x) in list(data["consumption"].keys()) else 0 for x in range(1,13)]
    # print(lister)
    query_data = tf.constant([
        type_mapping[data["buildingType"]],
        0 if "roomsCount" not in data.keys() else data["roomsCount"],
        0 if "residentsCount" not in data.keys() else data["residentsCount"],
        0 if "totalArea" not in data.keys() else data["totalArea"],
    ] + lister, dtype=tf.float32)

    query_data = tf.reshape(query_data, (1, -1))
    return query_data


mock = tf.constant([
    1, # bulding type
    2, # rooms count
    3, #resident count
    76.40, #total area
    1911, # killovats 1
    1827,# 2
    1506,# 3
    1248,# 4
    1534,# 5
    1154,# 6
    1599,# 7 
    1528, # 8
    1444, # 9 
    1250,# 10 
    1156, # 11
    1028 # 12
], dtype=tf.float32)

label = tf.constant([0], dtype=tf.float32)

mock = tf.reshape(mock, (1, -1))

print (mock.shape)


def create_model(learning_rate, layers, activation_function):
    keras_layers = []
    for i in layers[:-1]:
        if abs(i) <= 1:
            keras_layers.append(tf.keras.layers.Dropout(i))
        else: 
            keras_layers.append(tf.keras.layers.Dense(i, activation=activation_function, input_shape=(16,)))
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

                history = model.fit(
                    query_train_data,
                    query_train_data_labels,
                    epochs=epoch,  # Увеличьте количество эпох
                    batch_size=batch_size,
                    verbose=1,
                    validation_split = 0.2
                    )


                # тестируем сеть

                # преобразуем данные 
                # query_test_data = []
                # query_test_data_labels = []

                # for i in range(len(test_data)):
                #     label = tf.constant([1] if test_data[i]["isCommercial"] == True else [0], dtype=tf.float32) 
                #     normal_test_data = normalize_data(test_data[i])
                #     query_test_data.append(normal_test_data)
                #     query_test_data_labels.append(label)
                # query_test_data = tf.concat(query_test_data, axis=0)
                # query_test_data_labels = tf.concat(query_test_data_labels, axis=0)

                # prediction = model.predict(mock)
                # print(f"Предсказание после обучения: {prediction.tolist()}")

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

                iterator += 1

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

                prediction = model.predict(normalize_data(query))
                print(prediction.tolist())

with open("comprasion.json","w+", encoding="utf-8") as file:
    json.dump(comprasion, file, indent=4, ensure_ascii=False)


print(f"\nМаксимальное среднее = {maxi_avg} у Модели: {maxi_avg_name}.\nМаксимальное {maxi} У Модели: {maxi_name}")

# plt.show()


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