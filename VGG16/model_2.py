# -*- coding: utf-8 -*-
"""Model_2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_FlgzkC-NgUPXistdlRhMWP5PsoYn__P
"""

#from google.colab import drive
#drive.mount('/content/drive')

import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image_dataset_from_directory
import cv2
import numpy as np
import os
import pandas as pd

# VGG model requires 224*224 input so we are going to re-size all images
IMAGE_SIZE = [224, 224]

train_path = '/content/drive/MyDrive/valid2/train'
valid_path = '/content/drive/MyDrive/valid2/test'

# example of progressively loading images from file
from tensorflow.keras.preprocessing.image import ImageDataGenerator
# create generator
# generator applied random preprocessing to make the model --> robust
datagen = ImageDataGenerator(rescale = 1./255,
                             shear_range = 0.2, # every image will be randomly distorted 0-0.2
                             zoom_range = 0.2, # every image will be randomly zoomed 0-0.2
                             horizontal_flip = True, #
                             vertical_flip=True,
                             rotation_range=30) #every image will be randomly ratated 0-30 degree
# prepare an iterators for each dataset
train_it = datagen.flow_from_directory( '/content/drive/MyDrive/valid2/train',
                                       class_mode='categorical',
                                       classes=['Alan Ritchson', 'Brie Larson', 'Charlize Theron', 'Helen Mirren', 'Jason Momoa', 'Jason Statham', 'John Cena', 'Jordana Brewster', 'Ludacris', 'Michelle Rodriguez', 'Nathalie Emmanuel', 'Scott Eastwood', 'Sung Kang', 'Tyrese Gibson', 'Vin Diesel'],
                                       target_size=(224, 224),
                                       batch_size=2,
                                       seed=7)
val_it = datagen.flow_from_directory('/content/drive/MyDrive/valid2/test',
                                       class_mode='categorical',
                                       classes=['Alan Ritchson', 'Brie Larson', 'Charlize Theron', 'Helen Mirren', 'Jason Momoa', 'Jason Statham', 'John Cena', 'Jordana Brewster', 'Ludacris', 'Michelle Rodriguez', 'Nathalie Emmanuel', 'Scott Eastwood', 'Sung Kang', 'Tyrese Gibson', 'Vin Diesel'],
                                       target_size=(224, 224),
                                       batch_size=2,
                                       seed=7)
test_it = datagen.flow_from_directory('/content/drive/MyDrive/valid2/test',
                                       class_mode='categorical',
                                       classes=['Alan Ritchson', 'Brie Larson', 'Charlize Theron', 'Helen Mirren', 'Jason Momoa', 'Jason Statham', 'John Cena', 'Jordana Brewster', 'Ludacris', 'Michelle Rodriguez', 'Nathalie Emmanuel', 'Scott Eastwood', 'Sung Kang', 'Tyrese Gibson', 'Vin Diesel'],
                                       target_size=(224, 224),
                                       batch_size=2,
                                       seed=7)
# confirm the iterator works
batchX, batchy = train_it.next()
print('Batch shape=%s, min=%.3f, max=%.3f' % (batchX.shape, batchX.min(), batchX.max()))

"""VGG 16"""

IMAGE_SIZE = [224, 224]

vgg = VGG16(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)

"""## Don't train existing weights"""

for layer in vgg.layers:
  layer.trainable = False

"""# Add Our Layers at End of VGG16"""

output_classes = 15

# our layers - you can add more if you want
x = Flatten()(vgg.output)
x = Dense(1000, activation='relu')(x)
prediction = Dense(output_classes, activation='softmax')(x)

# create a model object
model = Model(inputs=vgg.input, outputs=prediction)

# view the structure of the model
model.summary()

model.compile(
  loss='binary_crossentropy',
  optimizer='adam',
  metrics=['accuracy']
)

history_vgg= model.fit(
  train_it,
  validation_data=val_it,
  epochs=5
)

model.save('model_vgg.h5')

import matplotlib.pyplot as plt
plt.plot(history_vgg.history['loss'])
plt.plot(history_vgg.history['val_loss'])

plt.plot(history_vgg.history['accuracy'])
plt.plot(history_vgg.history['val_accuracy'])