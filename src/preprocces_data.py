import cv2 
import os
import numpy as np
from sklearn.model_selection import train_test_split


data_classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
data_location = './dataset/'

def load_data():
    data = []
    for i, data_class in enumerate(data_classes):
        data_location_class = data_location + data_class + '/'

        for img in os.listdir(data_location_class):
            print("Loading image: ", img)
            image = cv2.imread(data_location_class + img, cv2.IMREAD_GRAYSCALE)
            image = cv2.resize(image, (28, 28))

            data.append((image, i))
       
            
    return data

def preprocess_data(data):
    X = []
    y = []
    for img, label in data:
        X.append(img)
        y.append(label)

    print("preprocess_data: X: ", X)
    X = np.array(X) / 255.0
    y = np.array(y)
    X = X.reshape(-1, 28 * 28)
    return X, y

def dump_data(X, y, label='train'):
    np.save(f'{label}_X.npy', X)
    np.save(f'{label}_y.npy', y)

def main():
    data = load_data()
    X, y = preprocess_data(data)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
    
    dump_data(X_train, y_train, 'train')
    dump_data(X_test, y_test, 'test')

if __name__ == '__main__':
    main()