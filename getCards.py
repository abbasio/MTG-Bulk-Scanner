import requests
import os
import concurrent.futures


def get_cards(set):
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
    return data


def get_image(card):
    img_directory = "./images"
    path = os.path.join(img_directory, card["set_name"], card["name"])
    if os.path.exists(path):
        print("Found image directory: {}".format(path))
    else:
        os.makedirs(path)

    img_link = card["image_uris"]["large"]
    img_file_name = card["id"]
    try:
        img_data = requests.get(img_link).content
        card_path = os.path.join(path, "{}-clean.jpg".format(img_file_name))
        with open(card_path, "wb") as img_file:
            img_file.write(img_data)
    except Exception as error:
        print(error)


cards = get_cards("ktk")

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(get_image, cards)
