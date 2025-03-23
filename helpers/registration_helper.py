import random
import string
from helpers.api_helpers import CourierAPI
from helpers.courier_helper import generate_courier_data


def register_new_courier():
    courier_data = generate_courier_data()
    response = CourierAPI.create_courier(courier_data)
    if response.status_code == 201:
        return courier_data
    return None
