class OrderData:
    BASE_ORDER = {
        "firstName": "Тестовый",
        "lastName": "Заказчик",
        "address": "Тестовая улица, 123",
        "metroStation": 4,
        "phone": "+7 999 888 77 66",
        "rentTime": 5,
        "deliveryDate": "2024-01-20",
        "comment": "Тестовый заказ"
    }

    ORDERS_WITH_COLORS = [
        {**BASE_ORDER, "color": ["BLACK"]},
        {**BASE_ORDER, "color": ["GREY"]},
        {**BASE_ORDER, "color": ["BLACK", "GREY"]},
        {**BASE_ORDER, "color": []}
    ]

    ORDERS_FOR_TRACK_CHECK = [
        {**BASE_ORDER, "color": ["BLACK", "GREY"]},
        BASE_ORDER
    ]


class CourierColors:
    BLACK = "BLACK"
    GREY = "GREY"
    ALL_COLORS = [BLACK, GREY]
