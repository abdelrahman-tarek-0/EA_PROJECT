from model import Model
import numpy as np

def main():
    model = Model.create_model(0.1)
    
    flattened_weights = np.concatenate([w.flatten() for w in model.get_weights()])
    # print(flattened_weights)
    flattened_weights = np.append(flattened_weights, 0.1)

    data = Model.load_data("./dataset/")

    Model.fit_function(flattened_weights, data)
   

if __name__ == '__main__':
    main()