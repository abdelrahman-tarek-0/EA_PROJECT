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
    # Replace missing values (0s) with NaN
    data = data.replace({'Glucose': {0: np.nan},
                            'BloodPressure': {0: np.nan},
                            'SkinThickness': {0: np.nan},
                            'Insulin': {0: np.nan},
                            'BMI': {0: np.nan}}).iloc[1:]



    data.dropna(inplace=True)

    numeric_data = data.apply(pd.to_numeric, errors='coerce').dropna()
    #shuffle data
    numeric_data = numeric_data.sample(frac=1).reset_index(drop=True)

    X = numeric_data.drop('Outcome', axis=1)
    y = numeric_data['Outcome']

    # print(X.shape, y.shape)
    # print(X.head())
    # print(y.head())
    

    return X, y

def load_dataset_2():
    names = ['Age','Year','Nodes','IsDead']
    data = pd.read_csv("src/dataset/haberman.csv", names=names, header=None)

    print(data.isnull().sum())

    print(data.head())
    print(data.shape)
    # Replace missing values (0s) with NaN
    data = data.replace({'Age': {0: np.nan},
                            'Year': {0: np.nan},
                            'Nodes': {0: np.nan},
                            'IsDead': {0: np.nan}}).iloc[1:]
    
    # data.dropna(inplace=True)

    print(data.shape)
    #convert last column to binary
    data['IsDead'] = data['IsDead'].apply(lambda x: 1 if x == 2 else 0)


    numeric_data = data.apply(pd.to_numeric, errors='coerce')
    #shuffle data
    numeric_data = numeric_data.sample(frac=1).reset_index(drop=True)

    X = numeric_data.drop('IsDead', axis=1)
    y = numeric_data['IsDead']


    return X, y


# load_dataset_2()
# load_dataset()

    # scaler = StandardScaler()
    # X_normalized = scaler.fit_transform(X)
    # if(split):
    #     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
    #     return (X_train, y_train), (X_test, y_test)
    # else:
    #     return X, y
    
    # gene_weights_pool = np.load("./dataset/gene_weights_pool.npy")
    # gene_learning_rate_pool = np.load("./dataset/gene_learning_rate_pool.npy")

def load_gene_pool():
    gene_weights_pool = np.load("src/dataset/gene_pool.npy")
    # gene_learning_rate_pool = np.load("src/dataset/gene_learning_rate_pool.npy")

    return gene_weights_pool