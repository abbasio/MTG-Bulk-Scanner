import os
import json
import requests
import concurrent.futures
from utils import items_to_clean, make_dirs


def get_cards(set: str) -> list:
    data = []
    URL = f"https://api.scryfall.com/cards/search?include_extras=true&include_variations=true&order=set&q=e%3A{set}&unique=prints"

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
    path = os.path.join(data_directory, f"{set}.json")
    if os.path.exists(path):
        print("Data for this set already exists!")
    else:
        with open(path, "w") as data_file:
            data_file.write(cards_json)
    print(f"Successfully got data for {len(data)} cards")
    return data


def get_image(card: dict):
    img_dir = "./images"
    card_name = card["name"]
    set_name = card["set_name"]
    base_path = os.path.join(img_dir, "base", set_name)
    make_dirs([base_path])
    img_link = card["image_uris"]["large"]
    try:
        img_data = requests.get(img_link).content
        card_file = os.path.join(base_path, f"{card_name}.png")
        with open(card_file, "wb") as img_file:
            img_file.write(img_data)
        print(f"Retrieved images for card {card_name}")
    except Exception as error:
        print(f"Error on retrieving image for {card_name}")
        print(error)


def get_images_from_data(set: str):
    path = os.path.join("./data", f"{set}.json")
    try:
        with open(path, "r") as openfile:
            cards = json.load(openfile)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(get_image, cards)
    except Exception as error:
        print(error)


current_set = ""
# get_cards(current_set)
# get_images_from_data(current_set)
