import os
import json
import time
import concurrent.futures
from PIL import Image
from imageDistortion import random_edit_img
from utils import make_dirs


def generate_img_sets(card):
    img_dir_base: str = "./images/base"
    img_dir_training: str = "./images/training"
    img_dir_testing: str = "./images/testing"
    set_name: str = card["set_name"]
    card_number: str = card["collector_number"]
    card_name: str = card["name"]
    card_id: str = card["id"]
    img_extension: str = ".png"

    training_path = os.path.join(img_dir_training, set_name, card_number)
    testing_path = os.path.join(img_dir_testing, set_name, card_number)
    make_dirs([training_path, testing_path])

    base_path = os.path.join(img_dir_base, set_name, card_name + img_extension)
    base_image = Image.open(base_path)
    # Generate 2 clean images and 8 distorted images per card
    try:
        for x in range(10):
            img_number = "_" + str(x)
            img_file_training = os.path.join(
                training_path, card_id + img_number + img_extension
            )
            img_file_testing = os.path.join(
                testing_path, card_id + img_number + img_extension
            )
            if os.path.exists(img_file_testing) or os.path.exists(img_file_training):
                print(f"Data already exists for {card_name}")
                break
            else:
                img_data_training = base_image
                img_data_testing = base_image
                if x >= 2:
                    img_data_testing = random_edit_img(base_image)
                if x >= 3:
                    img_data_training = random_edit_img(base_image)
                img_data_training.resize((224, 312)).save(img_file_training)
                img_data_testing.resize((224, 312)).save(img_file_testing)
        print(f"Generated training and testing images for {card_name}")
    except Exception as error:
        print(f"Error when generating images for {card_name}")
        print(error)


def generate_dataset(set: str):
    try:
        start = time.time()
        data_directory = "./data"
        card_file = f"{set}.json"
        path = os.path.join(data_directory, card_file)
        with open(path, "r") as openfile:
            cards = json.load(openfile)
        cards_to_generate = len(cards) * 10
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(generate_img_sets, cards)
            executor.shutdown(wait=True)
        end = time.time()
        seconds = end - start
        print(
            f"Generated {cards_to_generate} training and {cards_to_generate} testing images in {seconds} seconds"
        )
    except Exception as error:
        print(error)


current_set = "frf"
generate_dataset(current_set)
