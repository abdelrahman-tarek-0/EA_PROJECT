import numpy as np


class DE:
    def __init__(self, pop_size, dim, max_iter, f, cr, bounds, target, func):
        self.pop_size = pop_size
        self.dim = dim
        self.max_iter = max_iter
        self.f = f
        self.cr = cr
        self.bounds = bounds
        self.target = target
        self.func = func

    def init_population(self):
        return np.random.uniform(self.bounds[0], self.bounds[1], (self.pop_size, self.dim))

    def mutation(self, population, i):
        idxs = [idx for idx in range(self.pop_size) if idx != i]
        a, b, c = population[np.random.choice(idxs, 3, replace=False)]
        return np.clip(a + self.f * (b - c), self.bounds[0], self.bounds[1])

    def crossover(self, target, mutant):
        crossover = np.random.rand(self.dim) < self.cr
        crossover[np.random.randint(self.dim)] = True
        return np.where(crossover, mutant, target)

    def selection(self, target, mutant):
        return mutant if self.func(mutant) < self.func(target) else target

    def run(self):
        population = self.init_population()
        for i in range(self.max_iter):
            new_population = np.zeros((self.pop_size, self.dim))
            for j in range(self.pop_size):
                mutant = self.mutation(population, j)
                trial = self.crossover(population[j], mutant)
                new_population[j] = self.selection(population[j], trial)
            population = new_population
        return population[np.argmin([self.func(ind) for ind in population])]
    
# export DE_ALGO


