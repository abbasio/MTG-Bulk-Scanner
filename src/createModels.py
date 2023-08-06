import os
import random
from PIL import Image
import json
import numpy as np
import tensorflow as tf

from tensorflow import keras
from keras import layers
from keras.models import Sequential
from utils import make_dirs


def get_image_datasets(set_name: str):
    train_dir = "./images/training"
    test_dir = "./images/testing"
    train_path = os.path.join(train_dir, set_name)
    test_path = os.path.join(test_dir, set_name)
    # Get datasets from image directories
    train_ds = keras.utils.image_dataset_from_directory(
        train_path, "inferred", image_size=(312, 224)
    )
    test_ds = keras.utils.image_dataset_from_directory(
        test_path, "inferred", image_size=(312, 224)
    )
    return (train_ds.class_names, test_ds.class_names)


def train_set_CNN_model(
    model_name: str, img_datasets: tuple, set_name: str, epochs: int = 10
):
    # save model
    model_dir = os.path.join("./models", set_name)
    make_dirs([model_dir])
    model_file = os.path.join(model_dir, f"{model_name}.json")
    if os.path.exists(model_file):
        raise Exception(f"Model already exists with name {model_name}")

    try:
        (train_ds, test_ds) = img_datasets
        class_names = train_ds.class_names
        number_of_cards = len(class_names)
        # use buffered prefetching
        AUTOTUNE = tf.data.AUTOTUNE
        train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
        test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)

        # define model
        model = Sequential()
        model.add(
            layers.Conv2D(32, (3, 3), activation="relu", input_shape=((312, 224, 3)))
        )
        model.add(layers.MaxPooling2D(2, 2))
        model.add(layers.Conv2D(64, (3, 3), activation="relu"))
        model.add(layers.MaxPooling2D(2, 2))
        model.add(layers.Conv2D(64, (3, 3), activation="relu"))
        model.add(layers.Flatten())
        model.add(layers.Dense(64, activation="relu"))
        model.add(layers.Dense(number_of_cards * 10, activation="softmax"))

        # compile the model
        model.compile(
            optimizer="adam",
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )

        # fit model to data
        model.fit(train_ds, validation_data=test_ds, epochs=epochs)

        # save model
        with open(model_file, "w") as model_json:
            model_json.write(model.to_json())

        # test model
        test_img_paths = [
            "./images/base/Fate Reforged/Shu Yun, the Silent Tempest.png",
            "./images/base/Fate Reforged/War Flare.png",
            "./images/base/Fate Reforged/Dark Deal.png",
            "./images/base/Fate Reforged/Fierce Invocation.png",
            "./images/base/Fate Reforged/Shamanistic Revelation.png",
        ]
        for path in test_img_paths:
            test_img_data = Image.open(path)
            test_model(model, test_img_data)
    except Exception as error:
        print(f"Error creating datasets for {set_name}")
        print(error)


def test_model(model: Sequential, image):
    cards = []
    card_img = image.resize((224, 312))
    card_img_array = np.array(np.array(card_img) / 255)
    cards.append(card_img_array)
    try:
        cards = np.array(cards)
        result = model.predict(cards)
        result_index, confidence = np.argmax(result), result[0, np.argmax(result)]
        print(result_index)
        print(confidence)
    except Exception as error:
        print(error)


# model_path = "./models/Fate Reforged/model_json.json"
# json_file = open(model_path, "r")
# loaded_model_json = json_file.read()
# json_file.close()
# model = tf.keras.models.load_model(model_path)
# model = tf.keras.models.model_from_json(loaded_model_json)
# img_path = "./images/base/Fate Reforged/Arcbond.png"
# img_data = Image.open(img_path)
# test_model(model, img_data)
set_name = "Fate Reforged"
img_datasets = get_image_datasets(set_name)
print(img_datasets)
# model_name = "model_0"
# train_set_CNN_model(model_name, img_datasets, set_name, 1)
