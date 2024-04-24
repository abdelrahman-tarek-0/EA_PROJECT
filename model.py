import tensorflow as tf
import numpy as np
from tensorflow import keras
from keras import layers, models


class Model:
    @staticmethod
    def create_model(learning_rate):
        nn = models.Sequential([
            layers.Dense(64, activation='relu', input_shape=(28, 28)),
            layers.Dense(32, activation='relu'),
            layers.Dense(10, activation='softmax')
        ])
        nn.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        return nn

    #@staticmethod
    #def set_weights(weights):
    @staticmethod
    def prepare_weights(weights):

        flattened_weights = np.array(weights) # الأوزان لزمن طبقة نم باي اراي وطوله 4266
        shapes = [(28, 64), (64,), (64, 32), (32,), (32, 10), (10,)] # شكل النيورنات في كل طبقة

        reshaped_weights = []
        start_idx = 0
        for shape in shapes:
            size = np.prod(shape)
            layer_weights = np.array(flattened_weights[start_idx:start_idx+size]).reshape(shape)
            reshaped_weights.append(layer_weights)
            start_idx += size

        return reshaped_weights

    @staticmethod
    def fit_function(weights, data):      
        (train_ds, test_ds) = data

        # [weights -> 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, learning -> 0.01]
        learning_rate = weights[-1]
        weights = weights[:-1]

        print("Learning rate: ", learning_rate)
        print("Weights: ", weights)
        print("Weights shape: ", len(weights))

        weights = Model.prepare_weights(weights)
            
        model = Model.create_model(learning_rate)
        
        model.set_weights(weights)

        model.fit(train_ds, epochs=5, batch_size=64)

        return model.evaluate(test_ds)
      
      
        # model.nn.set_weights(weights)
        # model.nn.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        # 
   
    @staticmethod
    def load_data(directory):
        print("Loading data from: ", directory)
        (train_ds, test_ds) = tf.keras.utils.image_dataset_from_directory(
            directory,
            image_size=(28, 28),
            seed=123,
            validation_split=.25,
            subset='both',
            color_mode='grayscale',
        )
        return train_ds, test_ds
    