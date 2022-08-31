from audioop import cross
import random

class Crossover():
    def __init__(self, population, C, R, machinesNumber):
        self.population = population
        self.populationNum = len(population)
        self.C = C
        self.R = R
        self.machinesNumber = machinesNumber

    def single_point(self, p1_index, p2_index):
        parent1 = self.population[p1_index][0]
        parent2 = self.population[p2_index][0]
        p1_flat = []
        p2_flat = []
        nulls1_available = self.C * self.R - self.machinesNumber
        nulls2_available = self.C * self.R - self.machinesNumber

        for list in parent1.machines:
            for machine in list:
                p1_flat.append(machine)

        for list in parent2.machines:
            for machine in list:
                p2_flat.append(machine)

        crossover_point = random.randint(0, len(p1_flat))
        c1_flat = []
        c2_flat = []

        for i in range(crossover_point):
            if (p1_flat[i] == None):
                nulls1_available -= 1
            c1_flat.append(p1_flat[i])

            if (p2_flat[i] == None):
                nulls2_available -= 1
            c2_flat.append(p2_flat[i])
        
        for i in range(len(p2_flat)):
            if (p2_flat[i] not in c1_flat):
                c1_flat.append(p2_flat[i])
            elif (p2_flat[i] == None and nulls1_available > 0):
                c1_flat.append(p2_flat[i])
                nulls1_available -= 1

            if (p1_flat[i] not in c2_flat):
                c2_flat.append(p1_flat[i])
            elif (p1_flat[i] == None and nulls2_available > 0):
                c2_flat.append(p1_flat[i])
                nulls2_available -= 1

        return c1_flat, c2_flat
