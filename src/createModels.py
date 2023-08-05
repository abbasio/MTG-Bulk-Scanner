import numpy as np
import os
import PIL
import tensorflow as tf

from tensorflow import keras
from keras import layers
from keras.models import Sequential
import matplotlib.pyplot as plt

img_directory = "./images"
set_name = "Arabian Nights"
path = os.path.join(img_directory, set_name)
img_dataset = keras.utils.image_dataset_from_directory(path, "inferred")
class_names = img_dataset.class_names
