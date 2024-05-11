import os
import time
import shutil

os.environ["PATH"] += os.pathsep + 'C:/Graphviz-11.0.0-win64/bin'

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import requests
import numpy as np
from keras.models import Sequential, load_model
from sklearn.preprocessing import StandardScaler

from src.AI.de_algo import DE
from src.AI.model import Model
from src.utils.loaders import load_dataset, load_dataset_2, load_gene_pool

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

node_backend = 'http://127.0.0.1:8001'
is_running = False


def send_report(report):
    requests.post(f'{node_backend}/reports', json=report)

def check_node():
    try:
        requests.get(f'{node_backend}/health')
    except requests.exceptions.ConnectionError:
        return False
    return True



def main(*,  epochs=5, num_individuals=100, mutateWeight=0.5, crossoverRate=0.5, num_generations=3, layers=[], delay=0, dataset='diabetes', isParallel=False):
    global is_running
    is_running = True

    data = []
    if dataset == 'diabetes':
        data = load_dataset()
    else:
        data = load_dataset_2()

    input_dim = 8 if dataset == 'diabetes' else 3
    
    de = DE(
        data=data,
        Model=Model,
        gene_pool=load_gene_pool(),
        crossoverRate=crossoverRate,
        mutateWeight=mutateWeight,
        num_individuals=num_individuals,
        send_report=send_report,
        epochs=epochs,
        generations=num_generations,
        layers=layers,
        delay=delay,
        input_dim=input_dim,
        isParallel=isParallel
    )

    (best, history) = de.run()
    modelId = round(time.time()*1000)
    
    publicLocationHistoryOV = os.path.join(os.getcwd(), f'../server/public/uploads/{modelId}-history-ov.png')
    publicLocationHistoryB = os.path.join(os.getcwd(), f'../server/public/uploads/{modelId}-history-b.png')

    Model.visualize_history_over_time(history, publicLocationHistoryOV)
    Model.visualize_history_bounders(history, publicLocationHistoryB)


    best_model = Model.create_model(layers, input_dim)
    best_model.set_weights(Model.prepare_weights(best.Genes, de.weightsShape))

    

    directory = "diabetes" if dataset == 'diabetes' else "haberman"

    best_model.save(f'./generated_models/{directory}/{modelId}.keras')

    copyModelLocation = os.path.join(os.getcwd(), f'./generated_models/{directory}/{modelId}.keras')
    locationTo = os.path.join(os.getcwd(), f'../server/public/uploads/{modelId}.keras')

    #copy
    shutil.copy(copyModelLocation, locationTo)

    send_report({
        "command": "finish",
        "id": modelId,
        "dataset": directory,
        "fitness": best.Fitness
    })


    return best.Fitness


@app.route('/run/', methods=['POST'])
def run():
    global is_running
    
    if is_running:
        return 'Algorithm is already running'
    
    data = request.json

    epochs = data.get('epochs', 5)
    num_individuals = data.get('num_individuals', 100)
    num_generations = data.get('num_generations', 3)
    mutateWeight = data.get('mutateWeight', 0.5)
    crossoverRate = data.get('crossoverRate', 0.5)
    layers = data.get('layers', [])
    delay = data.get('delay', 0)
    dataset = data.get('dataset', 'diabetes')
    isParallel = data.get('parallelism', False)

    delay = 0 if isParallel else delay
    
    best_fitness = main(
        epochs=epochs,
        num_individuals=num_individuals,
        mutateWeight=mutateWeight,
        crossoverRate=crossoverRate,
        num_generations=num_generations,
        layers=layers,
        delay=delay,
        dataset=dataset,
        isParallel=isParallel
    )

    is_running = False

    return f'Best Fitness: {best_fitness}'

@app.route('/modelInfo/', methods=['POST'])
def get_model_info ():
    data = request.json

    layers = data.get('layers', [])
    dataset = data.get('dataset', 'diabetes')

    input_dim = 8 if dataset == 'diabetes' else 3

    if len(layers) == 0:
        return 'No layers provided'
    
    model = Model.create_model(layers, input_dim)
    shape = Model.getModelShapeList(model)
    weights = len(np.concatenate([w.flatten() for w in model.get_weights()]).tolist())
    name = Model.visualize_model(model, f"graph-{round(time.time()*1000)}", "../server/public/uploads")

    return jsonify({
        'shape': shape,
        'weights': weights + 1,
        'image': "/uploads/" + name
    })

@app.route('/status', methods=['GET'])
def status():
    global is_running
    return 'Running' if is_running else 'Idle'

@app.route('/model-status/', methods=['GET'])
def model_status():
    modelId = request.args.get('id')
    dataset = request.args.get('dataset', 'diabetes')

    location = "diabetes" if dataset == 'diabetes' else "haberman"
    modelPath = f'./generated_models/{location}/{modelId}.keras'
    isModelExists = os.path.exists(modelPath)

    return jsonify({
        'exists': isModelExists,
        'path': modelPath
    })
    
@app.route('/predict/', methods=['POST'])
def predict():
    data = request.json
    modelId = data.get('id')
    inputDataArray = data.get('data')
    dataset = data.get('dataset', 'diabetes')

    location = "diabetes" if dataset == 'diabetes' else "haberman"
    print(modelId, location)
    modelPath = f'./generated_models/{location}/{modelId}.keras'

    if not os.path.exists(modelPath):
        return 'Model not found'
    
    model = load_model(modelPath)
    X = np.array(inputDataArray).reshape(1, -1)
    y = model.predict(X)
    print(y)

    return jsonify({
        'prediction': f'{y.tolist()[0][0]}'
    })

if __name__ == '__main__':

    is_node_up = check_node()

    if not is_node_up:
        print('Node report server is not up')
        exit()

    print('Node report server is up')
    app.run(host='0.0.0.0', port=8000)