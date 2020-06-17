# -*- coding: utf-8 -*-

import tensorflow as tf
import os
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import Model
from pickle import dump

!wget https://github.com/jbrownlee/Datasets/releases/download/Flickr8k/Flickr8k_Dataset.zip
!wget https://github.com/jbrownlee/Datasets/releases/download/Flickr8k/Flickr8k_text.zip

!unzip /content/Flickr8k_Dataset.zip
!unzip /content/Flickr8k_text.zip

def extract_features(directory):
  model = VGG16()

  model.layers.pop()
  model = Model(inputs=model.inputs, outputs = model.layers[-1].output)
  print(model.summary())

  features = dict()
  try:
    for name in os.listdir(directory):
      filename = directory + '/' + name
      image = load_img(filename, target_size=(224,224))
      image = img_to_array(image)

      image = image.reshape(1,image.shape[0],image.shape[1],image.shape[2])

      image = preprocess_input(image)

      feature = model.predict(image, verbose=0)

      image_id = name.split('.')[0]
      features[image_id] = feature
      print(image_id)
  except:
    print('err')
    
  return features

directory = '/Flicker8k_Dataset'
features = extract_features(directory)

dump(features, open('Image_caption/features.pkl', 'wb'))


