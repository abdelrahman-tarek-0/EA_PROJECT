import numpy as np
class Individual:
    def __init__(self, Genes, Fitness, id):
        self.Genes = np.array(Genes)
        self.Fitness = Fitness
        self.id = id

    def setFitness(self, Fitness):
        self.Fitness = Fitness

    def getFitness(self):
        return self.Fitness
    
    def getGenes(self):
        return self.Genes
    
    def setGenes(self, Genes):
        self.Genes = np.array(Genes)