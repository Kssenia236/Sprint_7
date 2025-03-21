import random
import string
from helpers.api_helpers import CourierAPI


def register_new_courier():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    courier_data = {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }

    response = CourierAPI.create_courier(courier_data)

    if response.status_code == 201:
        return courier_data
    return None
