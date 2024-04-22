import tensorflow as tf
from tensorflow import keras
from keras import layers, models


class model:
    def __init__(self, num_classes, dataset):
        nn = models.Sequential([
            layers.Dense(64, activation='relu', input_shape=(28, 28)),
            layers.Dense(32, activation='relu'),
            layers.Dense(num_classes, activation='softmax')
        ])
        nn.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        self.nn = nn
        self.training_ds = dataset.train_ds
        self.test_ds = dataset.test_ds

    @staticmethod
    def load_data(self, directory):
        (training_ds, test_ds) = tf.keras.utils.image_dataset_from_directory(
            directory,
            image_size=(28, 28),
            seed=123,
            validation_split=.25,
            subset='both',
            color_mode='grayscale',
        )
        return training_ds, test_ds
        
     
        