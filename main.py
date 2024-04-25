from model import Model
import numpy as np
import random
from de_algo import DE

def main():
    data = Model.load_data("./dataset/diabetes.csv")
    gene_weights_pool = np.load("./dataset/gene_weights_pool.npy")
    gene_learning_rate_pool = np.load("./dataset/gene_learning_rate_pool.npy")
    fitness_function = Model.fitness_function


    de = DE(
        data=data,
        fitness_function=fitness_function,
        gene_weights_pool=gene_weights_pool,
        gene_learning_rate_pool=gene_learning_rate_pool,
        crossoverRate=0.5,
        mutateWeight=0.5,
        num_individuals=30
    )

    best = de.run(5)

    print(f'Best Fitness: {best.Fitness}')
    print(f'Best Genes: {best.Genes}')

    best_model = Model.create_model(best.Genes[-1])
    best_model.set_weights(Model.prepare_weights(best.Genes[:-1]))

    # save the model
    best_model.save('./dataset/best_model.h5')

    # print(selected[0].Genes[1])
    # print(selected[1].Genes[1])

    # print(selected[0].Genes[2])
    # print(selected[1].Genes[2])

    # print(selected[0].Genes - selected[1].Genes)




    # for ind in de.population:
    #     print(ind.Fitness, len(ind.Genes))  

    # ind = de.generate_individual()
    # ind2 = de.generate_individual()
    # ind3 = de.generate_individual()
    # ind4 = de.generate_individual()
    # ind5 = de.generate_individual()
    # ind6 = de.generate_individual()
    # ind7 = de.generate_individual()

    # print(ind.Fitness, len(ind.Genes))
    # print(ind2.Fitness, len(ind2.Genes))
    # print(ind3.Fitness, len(ind3.Genes))
    # print(ind4.Fitness, len(ind4.Genes))
    # print(ind5.Fitness, len(ind5.Genes))
    # print(ind6.Fitness, len(ind6.Genes))
    # print(ind7.Fitness, len(ind7.Genes))


    # de = DE(data, fitness_function, gene_weights_pool, gene_learning_rate_pool)
    # data = de.load_gene_pool()
    # print(data[0].shape, data[1].shape)
   

    
if __name__ == '__main__':
    main()