import os
import json
import requests
import concurrent.futures
from utils import items_to_clean
from PIL import Image


def get_cards(set: str) -> list:
    data = []
    URL = "https://api.scryfall.com/cards/search?include_extras=true&include_variations=true&order=set&q=e%3A{}&unique=prints".format(
        set
    )

    def get_card_pages(url):
        cards = requests.get(url).json()
        isNextPage = cards.get("has_more")
        cardsList = cards.get("data")

        for card in cardsList:
            data.append(card)

        if isNextPage:
            get_card_pages(cards.get("next_page"))
        else:
            return

    get_card_pages(URL)

    # Clean data
    for card in data:
        for item in items_to_clean:
            item_exists = item in card
            if item_exists:
                del card[item]

    data_directory = "./data"
    cards_json = json.dumps(data, indent=4)
    path = os.path.join(data_directory, "{}.json".format(set))
    if os.path.exists(path):
        print("Data for this set already exists!")
    else:
        with open(path, "w") as data_file:
            data_file.write(cards_json)
    print("Successfully got data for {} cards".format(len(data)))
    return data


def get_image(card: dict) -> bytes:
    img_directory = "./images"
    path = os.path.join(img_directory, card["set_name"], card["name"])
    if not os.path.exists(path):
        os.makedirs(path)

    img_link = card["image_uris"]["large"]
    img_file_name = card["id"]
    try:
        img_data = requests.get(img_link).content
        card_path = os.path.join(path, "{}_0.png".format(img_file_name))
        with open(card_path, "wb") as img_file:
            img_file.write(img_data)
    except Exception as error:
        print(error)
    return img_data


def get_images_from_data(set: str):
    path = os.path.join("./data", "{}.json".format(set))
    try:
        with open(path, "r") as openfile:
            cards = json.load(openfile)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(get_image, cards)
    except Exception as error:
        print(error)


current_set = "ktk"
# get_cards(current_set)
# get_images_from_data(current_set)
