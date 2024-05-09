from keras_visualizer import visualizer
import tensorflow as tf
import numpy as np
from tensorflow import keras


class Model:
    @staticmethod  
    def create_model(learning_rate):
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(12, activation='relu', input_dim=8),
            tf.keras.layers.Dense(8, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(loss='binary_crossentropy', optimizer=keras.optimizers.Adam(learning_rate=learning_rate), metrics=['accuracy'])
        return model

    @staticmethod
    def getModelShapeList(model):
        shape = [w.shape for w in model.get_weights()]
        return shape

    @staticmethod
    def prepare_weights(weights, shape_list):
        flattened_weights = np.array(weights) # الأوزان لزمن طبقة نم باي اراي وطوله 222
        #shape_list = [(8, 12), (12,), (12, 8), (8,), (8, 1), (1,)] # شكل النيورنات في كل طبقة

        reshaped_weights = []
        start_idx = 0
        for shape in shape_list:
            size = np.prod(shape)
            layer_weights = np.array(flattened_weights[start_idx:start_idx+size]).reshape(shape)
            reshaped_weights.append(layer_weights)
            start_idx += size

        return reshaped_weights

    @staticmethod
    def fitness_function(weights, data, shape_list, epochs=5):      
        (X_train, y_train), (X_test, y_test) = data

        learning_rate = weights[-1]
        weights = weights[:-1]

        weights = Model.prepare_weights(weights, shape_list)
        model = Model.create_model(learning_rate)
        
        model.set_weights(weights)

        model.fit(X_train, y_train, epochs=epochs, batch_size=10, verbose=0)

        loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
   
        return accuracy
   
    
   
    