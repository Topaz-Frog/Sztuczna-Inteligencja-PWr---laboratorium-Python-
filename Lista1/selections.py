import math
from random import random, shuffle
import sys
from utilis import createNelemList, sortTupleList

class Selection():
    def __init__(self, population):
        self.population = population
        self.populationNum = len(population)

    def roulette(self, maxFitness, beta):
        exp_list = []
        probSum = 0

        for i in range(self.populationNum):
            exp_list.append(math.exp(-beta * self.population[i][1] / maxFitness))
        
        probSum = sum(exp_list)
        probability = [value/probSum for value in exp_list]
        
        probSum = 0
        for i in range(len(probability)):
            probSum += probability[i]
            if (random() <= probSum):
                return i

    def tournament(self, chosenNum):
        populationIndexes = createNelemList(self.populationNum,self.populationNum)
        shuffle(populationIndexes)
        adaptHelper = []

        for index,specIndex in enumerate(populationIndexes):
            if index < chosenNum:
                adaptHelper.append((self.population[specIndex][1],specIndex))

        bestIndex = -1
        lowestFitness = sys.maxsize * 2 + 1

        for index, fitness in enumerate(adaptHelper):
            if fitness[0] < lowestFitness:
                lowestFitness = fitness[0]
                bestIndex = fitness[1]
        
        return bestIndex

    def getElites(self, numOfElites):
        temp_indexes = []
        best = []
        
        for index, fitness in enumerate(self.population):
            temp_indexes.append((index, fitness[1]))

        sorted_population = sortTupleList(temp_indexes)
        for i in range(2*numOfElites):
            best.append(sorted_population[i][0])

        return best
