import os
import json
import time
import concurrent.futures
from PIL import Image
from imageDistortion import random_edit_img


def generate_distorted_images(card):
    img_directory: str = "./images"
    set_name: str = card["set_name"]
    card_name: str = card["name"]
    card_id: str = card["id"]
    img_number: str = "_0"
    img_extension: str = ".png"
    path = os.path.join(
        img_directory, set_name, card_name, card_id + img_number + img_extension
    )
    initial_image = Image.open(path)
    try:
        for x in range(9):
            img_number = "_" + str(x + 1)
            if x <= 1:
                img_data = initial_image
            else:
                img_data = random_edit_img(initial_image)
            path = os.path.join(
                img_directory, set_name, card_name, card_id + img_number + img_extension
            )
            if not os.path.exists(path):
                img_data.save(path)
        print("Generated training images for {}".format(card_name))
    except Exception as error:
        print(error)


def generate_dataset(set: str):
    try:
        start = time.time()
        path = os.path.join("./data", "{}.json".format(set))
        with open(path, "r") as openfile:
            cards = json.load(openfile)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(generate_distorted_images, cards)
        end = time.time()
        print("Generated {} images in {} seconds".format(len(cards) * 9, end - start))
    except Exception as error:
        print(error)


current_set = ""
# generate_dataset(current_set)
