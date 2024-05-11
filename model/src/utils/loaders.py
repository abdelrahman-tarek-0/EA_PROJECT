import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras


def load_dataset():
    names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
    data = pd.read_csv("src/dataset/diabetes.csv", names=names, header=None)

    print(data.isnull().sum())
    data = data.replace({'Glucose': {0: np.nan},
                            'BloodPressure': {0: np.nan},
                            'SkinThickness': {0: np.nan},
                            'Insulin': {0: np.nan},
                            'BMI': {0: np.nan}}).iloc[1:]



    data.dropna(inplace=True)

    numeric_data = data.apply(pd.to_numeric, errors='coerce').dropna()

    numeric_data = numeric_data.sample(frac=1).reset_index(drop=True)

    X = numeric_data.drop('Outcome', axis=1)
    y = numeric_data['Outcome']

    

    return X, y

def load_dataset_2():
    names = ['Age','Year','Nodes','IsDead']
    data = pd.read_csv("src/dataset/haberman.csv", names=names, header=None)

    print(data.isnull().sum())

    print(data.head())
    print(data.shape)
    data = data.replace({'Age': {0: np.nan},
                            'Year': {0: np.nan},
                            'Nodes': {0: np.nan},
                            'IsDead': {0: np.nan}}).iloc[1:]
    


    print(data.shape)
    data['IsDead'] = data['IsDead'].apply(lambda x: 1 if x == 2 else 0)


    numeric_data = data.apply(pd.to_numeric, errors='coerce')
    numeric_data = numeric_data.sample(frac=1).reset_index(drop=True)

    X = numeric_data.drop('IsDead', axis=1)
    y = numeric_data['IsDead']


    return X, y


def load_gene_pool():
    gene_weights_pool = np.load("src/dataset/gene_pool.npy")

    return gene_weights_pool