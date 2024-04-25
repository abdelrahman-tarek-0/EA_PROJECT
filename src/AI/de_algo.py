import numpy as np
from src.classes.Individual import Individual


def append_to_file(file_name, text):
    with open(f'src/logs/{file_name}.log', 'a') as file:
        file.write(text)

class DE:
    def __init__(self, *, data=[], fitness_function=None, gene_pool=None, num_individuals=10, mutateWeight=0.8, crossoverRate=0.7):
        self.data = data
        self.fitness_function = fitness_function
        self.gene_weights_pool = gene_pool[0]
        self.gene_learning_rate_pool = gene_pool[1]
        self.num_individuals = num_individuals
        self.mutateWeight = mutateWeight
        self.crossoverRate = crossoverRate

        self.population = self.init_population()


    def init_population(self):
        print("Initializing Population")
        population = []
        for i in range(self.num_individuals):
            print(f"Individual {i}")
            population.append(self.generate_individual())

        return population

    
    
    def mutation (self, r1, r2, r3):
        mutated  = r3.Genes + self.mutateWeight*(r1.Genes - r2.Genes)
        return np.clip(mutated, -1, 1)

    def crossover(self, target, mutated):
        trail_gene = []
        for i in range(len(target.Genes)):
            if np.random.rand() < self.crossoverRate:
                trail_gene.append(mutated[i])
            else:
                trail_gene.append(target.Genes[i])

        return trail_gene
       
    def survive(self, target, trail_gene):
        trail_gene_fitness = self.fitness_function(trail_gene, self.data)
        # print(f"Trail Gene Fitness: {trail_gene_fitness}")
        append_to_file("trail_ind", f"{trail_gene_fitness}\n")

        if trail_gene_fitness > target.Fitness:
            append_to_file("serv_ind", f"Individual Fitness: {target.Fitness} is less than Trail Gene Fitness: {trail_gene_fitness}\n")
        
            target.setGenes(trail_gene)
            target.setFitness(trail_gene_fitness)

        return target


    def selection(self, i):
        target = self.population[i]
        r1, r2, r3 = np.random.choice(self.population, 3, replace=False) 

        return target, r1, r2, r3
    
    def get_best_individual(self):
        best = None

        for ind in self.population:
            if best is None or ind.Fitness > best.Fitness:
                best = ind

        return best


    def generate_individual(self):
        genes = np.random.choice(self.gene_weights_pool, 221).tolist()
        genes.append(np.random.choice(self.gene_learning_rate_pool))
        fitness = self.fitness_function(genes, self.data)

        return Individual(genes, fitness)
    
    def run(self, generations=100):
        print("Running DE")
        for j in range(generations):

            append_to_file("pop_ind", f"+++++++++++++++++++++++Generation {j}+++++++++++++++++++++++\n")
            append_to_file("trail_ind", f"+++++++++++++++++++++++Generation {j}+++++++++++++++++++++++\n")
            append_to_file("serv_ind", f"+++++++++++++++++++++++Generation {j}+++++++++++++++++++++++\n")
            append_to_file("normal_ind", f"+++++++++++++++++++++++Generation {j}+++++++++++++++++++++++\n")

            print(f"\n+++++++++++++++++++++++Generation {j}+++++++++++++++++++++++")
            
            bestInGeneration = self.get_best_individual()


            for i in range(len(self.population)):
                target, r1, r2, r3 = self.selection(i)
                mutated = self.mutation(r1, r2, r3)
                trail_gene = self.crossover(target, mutated)

                print(f"Individual {i} Fitness: {target.Fitness}")
                append_to_file("normal_ind", f"{target.Fitness}\n")

                self.population[i] = self.survive(target, trail_gene) 


                append_to_file("pop_ind", f"{self.population[i].Fitness}\n")

            print(f"Best in Generation {j} Fitness: {bestInGeneration.Fitness}\n")
       

        

        return self.get_best_individual()


    
# export DE_ALGO


