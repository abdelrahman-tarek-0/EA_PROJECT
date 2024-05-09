from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import requests
import numpy as np
import random
from src.AI.de_algo import DE
from src.AI.model import Model
from src.utils.loaders import load_dataset, load_gene_pool

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



def main(*,  epochs=5, num_individuals=100, mutateWeight=0.5, crossoverRate=0.5, num_generations=3):
    global is_running
    is_running = True

    de = DE(
        data=load_dataset(),
        Model=Model,
        gene_pool=load_gene_pool(),
        crossoverRate=crossoverRate,
        mutateWeight=mutateWeight,
        num_individuals=num_individuals,
        send_report=send_report,
        epochs=epochs,
        generations=num_generations
    )

    best = de.run()

    # print(f'Best Fitness: {best.Fitness}')
    # print(f'Best Genes: {best.Genes}')

    # best_model = Model.create_model(best.Genes[-1])
    # best_model.set_weights(Model.prepare_weights(best.Genes[:-1]))
    # best_model.fit(de.data, epochs=epochs, batch_size=10)

    # # save the model
    # best_model.save('./dataset/best_model.h5')

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
    
    best_fitness = main(
        epochs=epochs,
        num_individuals=num_individuals,
        mutateWeight=mutateWeight,
        crossoverRate=crossoverRate,
        num_generations=num_generations
    )

    is_running = False

    return f'Best Fitness: {best_fitness}'

@app.route('/status', methods=['GET'])
def status():
    global is_running
    return 'Running' if is_running else 'Idle'

if __name__ == '__main__':

    is_node_up = check_node()
    modelCreated = Model.create_model(0.01)

    if not is_node_up:
        print('Node report server is not up')
        exit()

    print('Node report server is up')
    app.run(host='0.0.0.0', port=8000)