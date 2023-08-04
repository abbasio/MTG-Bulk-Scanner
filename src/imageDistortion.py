from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
import random


def zoom_rotate_img(image):
    # store initial image size
    initial_size = image.size
    # determine at random how much or little we scale the image
    scale = 0.95 + random.random() * 0.1
    scaled_img_size = tuple([int(i * scale) for i in initial_size])

    # create a blank background with a random color and same size as intial image
    bg_color = tuple(np.random.choice(range(256), size=3))
    background = Image.new("RGB", initial_size, bg_color)

    # determine the center location to place our rotated card
    center_box = tuple((n - o) // 2 for n, o in zip(initial_size, scaled_img_size))

    # scale the image
    scaled_img = image.resize(scaled_img_size)

    # randomly select an angle to skew the image
    max_angle = 5
    skew_angle = random.randint(-max_angle, max_angle)

    # add the scaled image to our color background
    background.paste(
        scaled_img.rotate(skew_angle, fillcolor=bg_color, expand=1).resize(
            scaled_img_size
        ),
        center_box,
    )

    # randomly flip the image 180 degrees
    if random.choice([True, False]):
        background = background.rotate(180)

    return background


def blur_img(image):
    return image.filter(filter=ImageFilter.BLUR)


def adjust_color(image):
    converter = ImageEnhance.Color(image)
    # randomly decide to half or double the image saturation
    saturation = random.choice([0.5, 1.5])
    return converter.enhance(saturation)


def adjust_contrast(image):
    converter = ImageEnhance.Contrast(image)
    # randomly decide to half or double the image saturation
    contrast = random.choice([0.5, 1.5])
    return converter.enhance(contrast)


def adjust_sharpness(image):
    converter = ImageEnhance.Sharpness(image)
    # randomly decide to half or double the image saturation
    sharpness = random.choice([0.5, 1.5])
    return converter.enhance(sharpness)


def random_edit_img(image):
    """Help: Make poor edits to the image at random and return the finished copy. Can optionally not distort
    the image if need be."""

    # randomly choose which editing operations to perform
    edit_permission = np.random.choice(a=[False, True], size=(4))

    # always skew the image, randomly make the other edits
    image = zoom_rotate_img(image)
    if edit_permission[0]:
        image = blur_img(image)
    if edit_permission[1]:
        image = adjust_color(image)
    if edit_permission[2]:
        image = adjust_contrast(image)
    if edit_permission[3]:
        image = adjust_sharpness(image)
    return image
