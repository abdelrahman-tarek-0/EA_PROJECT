import numpy as np
from src.classes.Individual import Individual
import time 
from joblib import Parallel, delayed

def append_to_file(file_name, text):
    with open(f'src/logs/{file_name}.log', 'a') as file:
        file.write(text)

class DE:
    def __init__(self, *, data=[], gene_pool=None, Model=None, num_individuals=10, mutateWeight=0.8, crossoverRate=0.7, send_report=None, epochs=5, generations=100, layers=[]):
        self.data = data
        self.gene_weights_pool = gene_pool[0]
        self.gene_learning_rate_pool = gene_pool[1]
        self.num_individuals = num_individuals
        self.mutateWeight = mutateWeight
        self.crossoverRate = crossoverRate
        self.send_report = send_report
        self.epochs = epochs
        self.generations = generations
        self.layers = layers
        self.weightsShape = Model.getModelShapeList(Model.create_model(0.01, self.layers))
        self.weightsListSize = len(np.concatenate([w.flatten() for w in Model.create_model(0.01, self.layers).get_weights()]).tolist())

        self.fitness_function = lambda genes: Model.fitness_function(genes, self.data, self.weightsShape, self.layers, self.epochs)

        self.send_report({
            "command": "start",
            'message': 'Algorithm started',
            "data": {
                "num_individuals": self.num_individuals,
                "mutateWeight": self.mutateWeight,
                "crossoverRate": self.crossoverRate,
                "epochs": self.epochs,
                "generations": self.generations,
                "layers": self.layers,
                "weightsLen": self.weightsListSize + 1
            }
        })

        self.population = self.init_population()


    def init_population(self):
        start = time.time()
        print("Initializing Population")

        def create_individual(i):
            print(f"Creating individual {i}")
            ind = self.generate_individual(i)
            self.send_report({
                "command": "create_individual",
                "individual": {
                    "id": i,
                    "fitness": ind.Fitness,
                    "genes": ind.Genes.tolist(),
                },
            })
            return ind
        
        # population = []
        # for i in range(self.num_individuals):
        #     population.append(create_individual(i))

        population = Parallel(n_jobs=-1)(delayed(create_individual)(i) for i in range(self.num_individuals))

        end = time.time()
        print(f"Time taken to initialize population: {end - start} seconds")

        return population

    def mutation (self, r1, r2, r3):
        mutated  = r3.Genes + self.mutateWeight*(r1.Genes - r2.Genes)
        self.send_report({"fitness": self.fitness_function(mutated), "id": "mutated"})

        return np.clip(mutated, -1, 1)

    def crossover(self, target, mutated):
        trail_gene = []
        for i in range(len(target.Genes)):
            if np.random.rand() < self.crossoverRate:
                trail_gene.append(mutated[i])
            else:
                trail_gene.append(target.Genes[i])

        self.send_report({"fitness": self.fitness_function(trail_gene), "id": "trail_gene"})
        return trail_gene
       
    def survive(self, target, trail_gene):
        trail_gene_fitness = self.fitness_function(trail_gene)
        print(f"Trail Gene Fitness: {trail_gene_fitness}")

        new_individual = None
        append_to_file("trail_ind", f"{trail_gene_fitness}\n")

        if trail_gene_fitness > target.Fitness:
            append_to_file("serv_ind", f"Individual Fitness: {target.Fitness} is less than Trail Gene Fitness: {trail_gene_fitness}\n")
            new_individual = Individual(trail_gene, trail_gene_fitness, target.id)
        else:
            new_individual = target

        self.send_report({"fitness": new_individual.Fitness, "id": "new_individual"})

        return new_individual


    def selection(self, i):
        target = self.population[i]
        populationWithoutTarget = self.population[:i] + self.population[i+1:]
        
        r1, r2, r3 = np.random.choice(populationWithoutTarget, 3, replace=False) 

        return target, r1, r2, r3
    
    def get_best_individual(self):
        best = None

        for ind in self.population:
            if best is None or ind.Fitness > best.Fitness:
                best = ind

        return best


    def generate_individual(self, id):
        genes = np.random.choice(self.gene_weights_pool, self.weightsListSize).tolist()
        genes.append(np.random.choice(self.gene_learning_rate_pool))
        fitness = self.fitness_function(genes)

        return Individual(genes, fitness, id)
    
    def run(self):
        print("Running DE")
     
        for j in range(self.generations):

            append_to_file("pop_ind", f"+++++++++++++++++++++++Generation {j}+++++++++++++++++++++++\n")
            append_to_file("trail_ind", f"+++++++++++++++++++++++Generation {j}+++++++++++++++++++++++\n")
            append_to_file("serv_ind", f"+++++++++++++++++++++++Generation {j}+++++++++++++++++++++++\n")
            append_to_file("normal_ind", f"+++++++++++++++++++++++Generation {j}+++++++++++++++++++++++\n")

            print(f"\n+++++++++++++++++++++++Generation {j}+++++++++++++++++++++++")

            self.send_report({
                "command": "generation_started",
                "generation": j,
                "best_fitness": self.get_best_individual().Fitness,
                "message": f"Running Generation {j}"
            })
        
            new_population = []

            # start = time.time()
            # for i in range(len(self.population)):
            #     target, r1, r2, r3 = self.selection(i)
            #     mutated = self.mutation(r1, r2, r3)
            #     trail_gene = self.crossover(target, mutated)

            #     print(f"Individual {i} Fitness: {target.Fitness}")
            #     append_to_file("normal_ind", f"{target.Fitness}\n")

            #     new_individual = self.survive(target, trail_gene)
            #     new_population.append(new_individual)


            #     append_to_file("pop_ind", f"{self.population[i].Fitness}\n")

            # end = time.time()

            start = time.time()
            def opt(i): 
                target, r1, r2, r3 = self.selection(i)
                mutated = self.mutation(r1, r2, r3)
                trail_gene = self.crossover(target, mutated)

                print(f"Individual {i} Fitness: {target.Fitness}")

                self.send_report({"fitness": target.Fitness, "id": i})
                # append_to_file("normal_ind", f"{target.Fitness}\n")

                new_individual = self.survive(target, trail_gene)

                # append_to_file("pop_ind", f"{new_individual.Fitness}\n")

                return new_individual


            new_population = Parallel(n_jobs=-1)(delayed(opt)(i) for i in range(len(self.population)))
            end = time.time()   

            print(f"Time taken to run generation {j}: {end - start} seconds")

            bestInGeneration = self.get_best_individual()
            self.population = new_population # generational model

            self.send_report({"fitness": bestInGeneration.Fitness, "id": j, "message": f"Best in Generation {j}"})

            print(f"Best in Generation {j} Fitness: {bestInGeneration.Fitness}\n")
       

        self.send_report({"command": "finish", "message": "Algorithm finished"})

        return self.get_best_individual()
    
    # def stop(self):


    


    
# export DE_ALGO


