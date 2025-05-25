
const mockActual = [
    {
        address: "Краснодарский край, р-н Тимашевский, ст-ца Роговская, ул Свободная, д. 14 ",
        buildingType: "Частный",
        probability: 99,
        coordinates: [
          38.716499,
          45.738844
        ]
    },
    {
        address: "Краснодарский край, р-н Анапский, село Витязево, проезд Красивый, д. 3",
        buildingType: "Частный",
        probability: 97,
        coordinates: [
          37.256265,
          44.986342
        ]
    },
    {
        address: "Краснодарский край, р-н Усть-Лабинский, х Братский, ул Ленина, д. 49 А",
        buildingType: "Частный",
        probability: 92,
        coordinates: [
            40.80446,
            44.405181
        ]
    },
    {
        address: "Краснодарский край, р-н Тбилисский, ст-ца Тбилисская, ул Хуторская, д. 31 ",
        buildingType: "Частный",
        probability: 87,
        coordinates: [
            40.226399,
            45.359428
        ]
    },
    {
        address: "Краснодарский край, р-н Анапский, с Сукко, ул Кооперативная, д. 2 ",
        buildingType: "Частный",
        probability: 85,
        coordinates: [
            37.391738,
            44.786765
        ]
    },
    {
        address: "Краснодарский край, р-н Анапский, село Витязево, проезд Красивый, д. 3 ",
        buildingType: "Частный",
        probability: 59,
        coordinates: [
            37.256265,
            44.986342
        ]
    },
    {
        address: "Краснодарский край, р-н Анапский, село Витязево, пер Благовещенский, д. 14 ",
        buildingType: "Частный",
        probability: 39,
        coordinates: [
            37.260786,
            44.987214
        ]
    }
];

const mockSavings = [
    {
        address: "Краснодарский край, р-н Тимашевский, ст-ца Роговская, ул Свободная, д. 14 ",
        buildingType: "Частный",
        probability: 99,
        coordinates: [
          38.716499,
          45.738844
        ]
    },
    {
        address: "Краснодарский край, р-н Анапский, село Витязево, проезд Красивый, д. 3",
        buildingType: "Частный",
        probability: 97,
        coordinates: [
          37.256265,
          44.986342
        ]
    },
    {
        address: "Краснодарский край, р-н Усть-Лабинский, х Братский, ул Ленина, д. 49 А",
        buildingType: "Частный",
        probability: 92,
        coordinates: [
            40.80446,
            44.405181
        ]
    }
];

const mockComplaints = [
    {
        id: 1,
        address: "Краснодарский край, р-н Анапский, село Витязево, проезд Летний, д. 2 А",
        message: "Проблемы с электричеством. Розетки в некоторых комнатах не работают. В лифт заходить страшно...",
        date: "23.05.2025"
    },
    {
        id: 2,
        address: "Краснодарский край, р-н Анапский, село Витязево, проезд Летний, д. 2 А",
        message: "Проблемы с электричеством. Розетки в некоторых комнатах не работают. В лифт заходить страшно...",
        date: "22.05.2025"
    },
    {
        id: 3,
        address: "Краснодарский край, р-н Анапский, село Витязево, проезд Летний, д. 2 А",
        message: "Проблемы с электричеством. Розетки в некоторых комнатах не работают. В лифт заходить страшно...",
        date: "21.05.2025"
    },
    {
        id: 4,
        address: "Краснодарский край, р-н Анапский, село Витязево, проезд Летний, д. 2 А",
        message: "Проблемы с электричеством. Розетки в некоторых комнатах не работают. В лифт заходить страшно...",
        date: "20.05.2025"
    },
    {
        id: 5,
        address: "Краснодарский край, р-н Анапский, село Витязево, проезд Летний, д. 2 А",
        message: "Проблемы с электричеством. Розетки в некоторых комнатах не работают. В лифт заходить страшно...",
        date: "19.05.2025"
    },
];

function getColorByRange(percent) {
    // Ограничение значения в диапазоне 0-100
    percent = Math.max(0, Math.min(100, percent));

    if (percent <= 40) {
        return 'rgb(92, 194, 8)';
    } else if (percent <= 65) {
        return 'rgb(232, 203, 10)';
    } else if (percent <= 78) {
        return '#FFA500';
    } else {
        return '#FF0000';
    }
}

let complaintsList = document.querySelector(".complaints_list");
let objectsList = document.querySelector("#tab__obj_list");
let savingsList = document.querySelector("#tab__saved_list");

mockActual.forEach(obj => {
    objectsList.innerHTML +=
        `
            <div class="tab__obj_list-card">
                <h2 class="card__address">
                    ${obj.address}
                </h2>
                <div class="card__probability">
                    ${obj.probability}%
                    <div class="card__probability-progress">
                        <div class="progress__value" style="width: ${obj.probability}%; background: ${getColorByRange(obj.probability)}"></div>
                    </div>
                </div>
                <div class="card__more">
                    <div class="card__more-full">Подробный отчёт</div>
                    <div class="card__more-map" onclick="moveToPoint([${obj.coordinates[0]}, ${obj.coordinates[1]}])">К карте</div>
                    <div class="card__more-save">Сохранить</div>
                </div>
            </div>
        `;
});


mockSavings.forEach(obj => {
    savingsList.innerHTML +=
        `
            <div class="tab__obj_list-card">
                <h2 class="card__address">
                    ${obj.address}
                </h2>
                <div class="card__probability">
                    ${obj.probability}%
                    <div class="card__probability-progress">
                        <div class="progress__value" style="width: ${obj.probability}%; background: ${getColorByRange(obj.probability)}"></div>
                    </div>
                </div>
                <div class="card__more">
                    <div class="card__more-full">Подробный отчёт</div>
                    <div class="card__more-map" onclick="moveToPoint([${obj.coordinates[0]}, ${obj.coordinates[1]}])">К карте</div>
                    <div class="card__more-save">Сохранить</div>
                </div>
            </div>
        `;
});

mockComplaints.forEach(comp => {
    complaintsList.innerHTML +=
        `
        <div class="complaints_list__card">
            
            <div class="complaints_list__card-theme">
                ${comp.message}
            </div>
            <div class="complaints_list__card-address">
                ${comp.address}
            </div>
            <div class="complaints_list__card-time">
                ${comp.date}
            </div>
        </div>
    `;
});

let map_inited = false;

let map;

document.querySelectorAll(".nav_bar__btn").forEach(btn => {
    btn.onclick = () => {
        document.querySelector(".active_tab").classList.remove("active_tab");
        document.querySelector(`.tab[data-tab="${btn.dataset.tab}"]`).classList.add("active_tab");

        if (document.querySelector(".active_tab").dataset.tab == 4 && !map_inited) {
            map = new mapgl.Map('map', {
                center: [38.995672, 45.037415],
                zoom: 13,
                key: 'f93a5b47-6e3b-4c23-ba03-185daa02ef64',
                style: 'c080bb6a-8134-4993-93a1-5b4d8c36a59b'
            });
            mockActual.forEach(i => {
                const marker = new mapgl.Marker(map, {
                    coordinates: i.coordinates,
                });
            });

            map_inited = true;
        }
    };
});

function moveToPoint([x, y]) {
    document.querySelector(`.nav_bar__btn[data-tab="4"]`).click();
    map.setCenter([x, y]);
}