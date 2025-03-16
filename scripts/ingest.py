import os
import random
import string
import time

import requests
from pymongo import MongoClient

from definitions import ROOT_DIR
from tests.generator import generate_advertisement_create, generate_user_create


run_locally = False
pictures_per_advertisement = 2


if run_locally:
    client = MongoClient()
    base_url = "http://localhost:8500"
else:
    client = MongoClient("mongodb+srv://Julian:Julian2143{}@cluster0.bnlyb.mongodb.net/test")
    base_url = "https://hidden-slice-416812.ew.r.appspot.com"


def delete_all_advertisements():
    col = client["andelsbolig_basen"]["advertisement"]
    col.delete_many({})


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def create_fake_advertisements(count: int):
    pictures_path = f"{ROOT_DIR}/scripts/dev_data"
    pictures = [f for f in os.listdir(pictures_path) if os.path.isfile(os.path.join(pictures_path, f))]
    session = requests.Session()  # Use a session to keep connections alive

    for i in range(count):
        print(f"Creating advertisement {i + 1}/{count}")
        user_create = generate_user_create(f"{generate_random_string(5)}@gmail.com")
        r1 = session.post(f"{base_url}/user", json=user_create.model_dump())
        jwt_token = r1.json()["jwt"]
        headers = {"Authorization": f"Bearer {jwt_token}"}

        # Upload 2 random pics
        random_pictures = random.sample(pictures, pictures_per_advertisement)
        for random_picture in random_pictures:
            with open(f"{pictures_path}/{random_picture}", "rb") as file:
                files = {"file": (random_picture, file, "image/png")}
                r2 = session.post(f"{base_url}/upload", files=files, headers=headers)
                if r2.status_code != 200:
                    print(f"Error uploading image: {r2.text}")
                    exit()

        # Create advertisement
        advertisement_create = generate_advertisement_create()
        r3 = session.post(f"{base_url}/advertisement", json=advertisement_create, headers=headers)
        if r3.status_code != 200:
            print(f"Error creating advertisement: {r3.text}")
            exit()


# delete_all_advertisements()
create_fake_advertisements(10)
