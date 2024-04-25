import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras


def load_dataset():
    names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
    data = pd.read_csv("src/dataset/diabetes.csv", names=names, header=None)

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
    
    # gene_weights_pool = np.load("./dataset/gene_weights_pool.npy")
    # gene_learning_rate_pool = np.load("./dataset/gene_learning_rate_pool.npy")

def load_gene_pool():
    gene_weights_pool = np.load("src/dataset/gene_weights_pool.npy")
    gene_learning_rate_pool = np.load("src/dataset/gene_learning_rate_pool.npy")

    return gene_weights_pool, gene_learning_rate_pool