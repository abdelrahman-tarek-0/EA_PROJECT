import numpy as np
import random
from src.AI.de_algo import DE
from src.AI.model import Model
from src.utils.loaders import load_dataset, load_gene_pool
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def main():

    de = DE(
        data=load_dataset(),
        fitness_function=Model.fitness_function,
        gene_pool=load_gene_pool(),
        crossoverRate=0.5,
        mutateWeight=0.5,
        num_individuals=100
    )

    best = de.run(5)

    print(f'Best Fitness: {best.Fitness}')
    print(f'Best Genes: {best.Genes}')

    best_model = Model.create_model(best.Genes[-1])
    best_model.set_weights(Model.prepare_weights(best.Genes[:-1]))

    # save the model
    best_model.save('./dataset/best_model.h5')

    
if __name__ == '__main__':
    main()