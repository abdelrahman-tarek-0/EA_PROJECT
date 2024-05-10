import numpy as np


weight = np.random.uniform(-0.1, 0.1, 30_000_000)
# learning_rate = np.random.uniform(-0.1, 0.1, 5)

    # save the weights and learning rate in file 
np.save('src/dataset/gene_pool.npy', weight)
# np.save('src/dataset/gene_learning_rate_pool.npy', learning_rate)