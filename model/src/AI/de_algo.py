import numpy as np
from src.classes.Individual import Individual
import time 
from time import sleep
from joblib import Parallel, delayed

def append_to_file(file_name, text):
    with open(f'src/logs/{file_name}.log', 'a') as file:
        file.write(text)

class DE:
    def __init__(self, *, data=[], gene_pool=None, Model=None, num_individuals=10, mutateWeight=0.8, crossoverRate=0.7, send_report=None, epochs=5, generations=100, layers=[], delay=1, input_dim=8):
        self.data = data
        self.gene_weights_pool = gene_pool
        self.num_individuals = num_individuals
        self.mutateWeight = mutateWeight
        self.crossoverRate = crossoverRate
        self.send_report = send_report
        self.epochs = epochs
        self.generations = generations
        self.layers = layers
        self.input_dim = input_dim
        
        self.weightsShape = Model.getModelShapeList(Model.create_model(self.layers,  self.input_dim))
        self.weightsListSize = len(np.concatenate([w.flatten() for w in Model.create_model(self.layers,  self.input_dim).get_weights()]).tolist())

        self.fitness_function = lambda genes: Model.fitness_function(genes, self.data, self.weightsShape, self.layers,  self.input_dim)

        self.delay = lambda padding=0 : sleep(delay + padding)

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
        
        self.send_report({
            "command": "mutation",
            "r1": {
                "id": r1.id,
                "fitness": r1.Fitness,
                "genes": r1.Genes.tolist()
            },
            "r2": {
                "id": r2.id,
                "fitness": r2.Fitness,
                "genes": r2.Genes.tolist()
            },
            "r3": {
                "id": r3.id,
                "fitness": r3.Fitness,
                "genes": r3.Genes.tolist()
            },
            "mutated": {
                "genes": mutated.tolist(),
                "fitness": "Not Calculated",
            }
        })

        mutatedGenes = np.clip(mutated, -0.1, 0.1)
        self.delay()

        return mutatedGenes

    def crossover(self, target, mutated):

        trail_gene = []
        for i in range(len(target.Genes)):
            if np.random.rand() < self.crossoverRate:
                trail_gene.append(mutated[i])
            else:
                trail_gene.append(target.Genes[i])

        self.send_report({
            "command": "crossover",
            "target": {
                "id": target.id,
            },
            "trail": trail_gene,
        })

        self.delay()
        return trail_gene
       
    def survive(self, target, trail_gene):
        self.send_report({
            "command": "survive-started",
            "target": {
                "id": target.id,
            },
        })

        trail_gene_fitness = self.fitness_function(trail_gene)

        self.send_report({
            "command": "survive-trail_gene_fitness",
            "fitness": trail_gene_fitness,
        })

        new_individual = None
        winner = None
        if trail_gene_fitness > target.Fitness:
            new_individual = Individual(trail_gene, trail_gene_fitness, target.id)
            winner = "trail_gene"
        else:
            new_individual = target
            winner = "target"

        self.delay()
        self.send_report({
            "command": "survive-finished",
            "winner": winner,
            "new_individual": {
                "id": new_individual.id,
                "fitness": new_individual.Fitness,
                "genes": new_individual.Genes.tolist()
            },
            "target" :{
                "id": target.id,
                "fitness": target.Fitness,
                "genes": target.Genes.tolist()
            },
            "trail_gene_fitness": trail_gene_fitness
        })

        
        self.delay()
        return new_individual


    def selection(self, i):
        target = self.population[i]
        populationWithoutTarget = self.population[:i] + self.population[i+1:]
        
        r1, r2, r3 = np.random.choice(populationWithoutTarget, 3, replace=False) 

        self.send_report({
            "command": "selection",
            "target": {
                "id": target.id,
                "fitness": target.Fitness,
                "genes": target.Genes.tolist()
            },
            "r1": {
                "id": r1.id,
                "fitness": r1.Fitness,
                "genes": r1.Genes.tolist()
            },
            "r2": {
                "id": r2.id,
                "fitness": r2.Fitness,
                "genes": r2.Genes.tolist()
            },
            "r3": {
                "id": r3.id,
                "fitness": r3.Fitness,
                "genes": r3.Genes.tolist()
            }
        })

        self.delay()
        return target, r1, r2, r3
    
    def get_best_individual(self):
        best = None

        for ind in self.population:
            if best is None or ind.Fitness > best.Fitness:
                best = ind

        return best


    def generate_individual(self, id):
        genes = np.random.choice(self.gene_weights_pool, self.weightsListSize).tolist()
  
        fitness = self.fitness_function(genes)

        return Individual(genes, fitness, id)
    
    def run_generation(self): 
            new_population = []

            for i in range(len(self.population)):
                target, r1, r2, r3 = self.selection(i)
                mutated = self.mutation(r1, r2, r3)
                trail_gene = self.crossover(target, mutated)
                self.send_report({
                    "command": "clean_up",
                    "deleteTrail": False,
                    "deleteMutated": False,
                    "data": [
                        {
                            "id": r1.id,
                            "fitness": r1.Fitness,
                            "genes": r1.Genes.tolist()
                        },
                        {
                            "id": r2.id,
                            "fitness": r2.Fitness,
                            "genes": r2.Genes.tolist()
                        },
                        {
                            "id": r3.id,
                            "fitness": r3.Fitness,
                            "genes": r3.Genes.tolist()
                        }
                    ]
                })
                self.delay()
                new_individual = self.survive(target, trail_gene)

                new_population.append(new_individual)

                self.send_report({
                    "command": "new-individual",
                    "individual": {
                        "id": new_individual.id,
                        "fitness": new_individual.Fitness,
                        "genes": new_individual.Genes.tolist()
                    },
                })

                self.delay()
                self.send_report({
                    "command": "clean_up",
                    "deleteTrail": True,
                    "deleteMutated": True,
                    "data": [
                        {
                            "id": target.id,
                            "fitness": target.Fitness,
                            "genes": target.Genes.tolist()
                        },
                    ]
                })
                self.delay()

            return new_population
    
    def run_generation_parallel(self):
            def opt(i): 
                target, r1, r2, r3 = self.selection(i)
                mutated = self.mutation(r1, r2, r3)
                trail_gene = self.crossover(target, mutated)

                self.send_report({
                    "command": "clean_up",
                    "deleteTrail": False,
                    "deleteMutated": False,
                    "data": [
                        {
                            "id": r1.id,
                            "fitness": r1.Fitness,
                            "genes": r1.Genes.tolist()
                        },
                        {
                            "id": r2.id,
                            "fitness": r2.Fitness,
                            "genes": r2.Genes.tolist()
                        },
                        {
                            "id": r3.id,
                            "fitness": r3.Fitness,
                            "genes": r3.Genes.tolist()
                        }
                    ]
                })
                self.delay()

                new_individual = self.survive(target, trail_gene)

                self.delay()
                self.send_report({
                    "command": "clean_up",
                    "deleteTrail": True,
                    "deleteMutated": True,
                    "data": [
                        {
                            "id": target.id,
                            "fitness": target.Fitness,
                            "genes": target.Genes.tolist()
                        },
                    ]
                })
                self.delay()
                return new_individual


            new_population = Parallel(n_jobs=-1)(delayed(opt)(i) for i in range(len(self.population)))

            return new_population

    def run(self):
        print("Running DE")
     
        for j in range(self.generations):

            self.send_report({
                "command": "generation_started",
                "generation": j,
                "best_fitness": self.get_best_individual().Fitness,
                "message": f"Running Generation {j}"
            })
        
            # new_population = []

            # start = time.time()
            # for i in range(len(self.population)):
            #     target, r1, r2, r3 = self.selection(i)
            #     mutated = self.mutation(r1, r2, r3)
            #     trail_gene = self.crossover(target, mutated)
            #     self.send_report({
            #         "command": "clean_up",
            #         "deleteTrail": False,
            #         "deleteMutated": False,
            #         "data": [
            #             {
            #                 "id": r1.id,
            #                 "fitness": r1.Fitness,
            #                 "genes": r1.Genes.tolist()
            #             },
            #             {
            #                 "id": r2.id,
            #                 "fitness": r2.Fitness,
            #                 "genes": r2.Genes.tolist()
            #             },
            #             {
            #                 "id": r3.id,
            #                 "fitness": r3.Fitness,
            #                 "genes": r3.Genes.tolist()
            #             }
            #         ]
            #     })
            #     self.delay()
            #     new_individual = self.survive(target, trail_gene)

            #     new_population.append(new_individual)

            #     self.send_report({
            #         "command": "new-individual",
            #         "individual": {
            #             "id": new_individual.id,
            #             "fitness": new_individual.Fitness,
            #             "genes": new_individual.Genes.tolist()
            #         },
            #     })

            #     self.delay()
            #     self.send_report({
            #         "command": "clean_up",
            #         "deleteTrail": True,
            #         "deleteMutated": True,
            #         "data": [
            #             {
            #                 "id": target.id,
            #                 "fitness": target.Fitness,
            #                 "genes": target.Genes.tolist()
            #             },
            #         ]
            #     })
            #     self.delay()

            # end = time.time()

            # start = time.time()
            # def opt(i): 
            #     target, r1, r2, r3 = self.selection(i)
            #     mutated = self.mutation(r1, r2, r3)
            #     trail_gene = self.crossover(target, mutated)

            #     self.send_report({
            #         "command": "clean_up",
            #         "deleteTrail": False,
            #         "deleteMutated": False,
            #         "data": [
            #             {
            #                 "id": r1.id,
            #                 "fitness": r1.Fitness,
            #                 "genes": r1.Genes.tolist()
            #             },
            #             {
            #                 "id": r2.id,
            #                 "fitness": r2.Fitness,
            #                 "genes": r2.Genes.tolist()
            #             },
            #             {
            #                 "id": r3.id,
            #                 "fitness": r3.Fitness,
            #                 "genes": r3.Genes.tolist()
            #             }
            #         ]
            #     })
            #     self.delay()

            #     new_individual = self.survive(target, trail_gene)

            #     self.delay()
            #     self.send_report({
            #         "command": "clean_up",
            #         "deleteTrail": True,
            #         "deleteMutated": True,
            #         "data": [
            #             {
            #                 "id": target.id,
            #                 "fitness": target.Fitness,
            #                 "genes": target.Genes.tolist()
            #             },
            #         ]
            #     })
            #     self.delay()


            #     return new_individual


            # new_population = Parallel(n_jobs=-1)(delayed(opt)(i) for i in range(len(self.population)))
            # end = time.time()   

            # print(f"Time taken to run generation {j}: {end - start} seconds")

            # bestInGeneration = self.get_best_individual()
            self.population = self.run_generation() # generational model

            # self.send_report({
            #     "command": "generation_finished",
            #     "generation": j,
            #     "best_fitness": bestInGeneration.Fitness,
            #     "message": f"Generation {j} finished",
            #     "best_individual": {
            #         "id": bestInGeneration.id,
            #         "fitness": bestInGeneration.Fitness,
            #         "genes": bestInGeneration.Genes.tolist()
            #     }
            # })

            self.send_report({
                "command": "generation_finished",
                "generation": j,
            })

            self.delay(2)

        return self.get_best_individual()
    
    
    # def stop(self):


    


    
# export DE_ALGO


