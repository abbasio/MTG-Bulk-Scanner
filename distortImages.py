from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import json
import os


def generate_distorted_images(card):
    img_directory: str = "./images"
    set_name: str = card["set_name"]
    card_name: str = card["name"]
    card_id: str = card["id"]
    img_quality: str = "-clean.jpg"
    img_extension: str = ".jpg"
    path = os.path.join(img_directory, set_name, card_name, card_id + img_quality)
    initial_image = Image.open(path)
    try:
        for x in range(10):
            if x <= 1:
                img_quality = "-clean"
                img_data = initial_image
            else:
                img_quality = "-dirty"
                img_data = blur_image(initial_image)
            path = os.path.join(
                img_directory,
                set_name,
                card_name,
                card_id + img_quality + str(x) + img_extension,
            )
            if not os.path.exists(path):
                img_data.save(path)
                print("Printed {} images".format(str(x)))
    except Exception as error:
        print(error)


def blur_image(image):
    return image.filter(filter=ImageFilter.BLUR)


# test
path = os.path.join("./data", "ktk.json")
with open(path, "r") as openfile:
    cards = json.load(openfile)
generate_distorted_images(cards[0])
