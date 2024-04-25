import numpy as np
import random

weight = [random.uniform(-1, 1) for _ in range(1530000)]
learning_rate = [random.uniform(0.01, 0.1) for _ in range(153000)]

    # save the weights and learning rate in file 
np.save('src/dataset/gene_weights_pool.npy', weight)
np.save('src/dataset/gene_learning_rate_pool.npy', learning_rate)