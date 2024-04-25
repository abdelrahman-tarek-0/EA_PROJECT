import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
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

        # shapes = [w.shape for w in model.get_weights()]
        # weights = np.concatenate([w.flatten() for w in model.get_weights()])

        # print(f"Model created with learning rate: {shapes} and weights: {weights.shape}")

        return model

    #@staticmethod
    #def set_weights(weights):
    @staticmethod
    def prepare_weights(weights):

        flattened_weights = np.array(weights) # الأوزان لزمن طبقة نم باي اراي وطوله 222
        shapes = [(8, 12), (12,), (12, 8), (8,), (8, 1), (1,)] # شكل النيورنات في كل طبقة

        reshaped_weights = []
        start_idx = 0
        for shape in shapes:
            size = np.prod(shape)
            layer_weights = np.array(flattened_weights[start_idx:start_idx+size]).reshape(shape)
            reshaped_weights.append(layer_weights)
            start_idx += size

        return reshaped_weights

    @staticmethod
    def fitness_function(weights, data):      
        (X_train, y_train), (X_test, y_test) = data

        # [weights -> 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, learning -> 0.01]
        learning_rate = weights[-1]
        weights = weights[:-1]

        weights = Model.prepare_weights(weights)
        model = Model.create_model(learning_rate)
        
        model.set_weights(weights)

        model.fit(X_train, y_train, epochs=5, batch_size=10, verbose=0)

        loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
   
        return accuracy
   
    
   
    @staticmethod
    def load_data(datasetLocation):
        names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
        data = pd.read_csv(datasetLocation, names=names, header=None)

        # Replace missing values (0s) with NaN
        data = data.replace({'Glucose': {0: np.nan},
                            'BloodPressure': {0: np.nan},
                            'SkinThickness': {0: np.nan},
                            'Insulin': {0: np.nan},
                            'BMI': {0: np.nan}}).iloc[1:]

        data.dropna(inplace=True)

        numeric_data = data.apply(pd.to_numeric, errors='coerce').dropna()

        X = numeric_data.drop('Outcome', axis=1)
        y = numeric_data['Outcome']

        scaler = StandardScaler()
        X_normalized = scaler.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(X_normalized, y, test_size=0.2, random_state=42)
        
        return (X_train, y_train), (X_test, y_test)
    