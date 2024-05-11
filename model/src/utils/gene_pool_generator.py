import numpy as np


weight = np.random.uniform(-0.1, 0.1, 30_000_000)

np.save('src/dataset/gene_pool.npy', weight)
