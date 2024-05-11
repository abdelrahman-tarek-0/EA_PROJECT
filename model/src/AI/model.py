import os
from keras_visualizer import visualizer
import tensorflow as tf
import numpy as np
from tensorflow import keras
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from keras.models import Sequential
from keras.layers import Dense




class Model:
    @staticmethod 
    def create_model(layers,input_dim=8):
        model = Sequential()
        for i, layer_params in enumerate(layers):
            if i == 0:
                model.add(Dense(layer_params['n'], activation=layer_params['activation'], input_dim=input_dim))
            else:
                model.add(Dense(layer_params['n'], activation=layer_params['activation']))

        model.add(Dense(1, activation='sigmoid'))
        model.compile(loss='binary_crossentropy', optimizer=keras.optimizers.Adam(learning_rate=0.01), metrics=['accuracy'])

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
    def fitness_function(weights, data, shape_list, layers, input_dim=8):      
        (X, y) = data

        weights = Model.prepare_weights(weights, shape_list)
        model = Model.create_model(layers, input_dim)
        
        model.set_weights(weights)

        loss, accuracy = model.evaluate(X, y, verbose=0)
   
        return accuracy
   
    @staticmethod
    def visualize_model(model, name, moveToLocation):
        visualizer(
            file_format='png',
            model=model,
            file_name=name,
        )
        location = os.path.join(os.getcwd(), f"{name}.png")
        graphLocation = os.path.join(os.getcwd(), f"{name}")
        os.remove(graphLocation)

        if moveToLocation:
            newLocation = os.path.join(moveToLocation, f"{name}.png")
            os.rename(location, newLocation)
      
        return f"{name}.png"
   
    @staticmethod
    def visualize_history_over_time(generations,location):
        data = []
        for i, generation in enumerate(generations):
            for individual in generation:
                data.append([i, individual.id, individual.Fitness])

        df = pd.DataFrame(data, columns=['Generation', 'Individual', 'Fitness'])

        plt.figure(figsize=(10, 6))

        for individual in df['Individual'].unique():
            plt.plot(df[df['Individual'] == individual]['Generation'], df[df['Individual'] == individual]['Fitness'], marker='', color='grey', linewidth=1, alpha=0.4)

        best_fitness = df.groupby('Generation')['Fitness'].max()
        plt.plot(best_fitness, marker='', color='orange', linewidth=2.5, alpha=0.9, label='Best in each generation')

        plt.title("Fitness over Generations", loc='left', fontsize=12, fontweight=0, color='orange')
        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.legend()

        plt.savefig(location)

    @staticmethod
    def visualize_history_bounders(generations, location):
        data = []
        for i, generation in enumerate(generations):
            for individual in generation:
                data.append([i, individual.id, individual.Fitness])

        df = pd.DataFrame(data, columns=['Generation', 'Individual', 'Fitness'])

        plt.figure(figsize=(10, 6))

        df.boxplot(column='Fitness', by='Generation')

        plt.title("Fitness Distribution over Generations")
        plt.xlabel("Generation")
        plt.ylabel("Fitness")

        plt.savefig(location)