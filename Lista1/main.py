import sys
from turtle import pos
from utilis import getAdaptation, loadCostFile, loadFlowFile
from selections import Selection
from specimen import Specimen
from crossover import Crossover

# EASY
cost_file = "flo_dane_v1/easy_cost.json"
flow_file = "flo_dane_v1/easy_flow.json"
machinesNumber = 9
r = 3
c = 3

#FLAT
# cost_file = "flo_dane_v1/flat_cost.json"
# flow_file = "flo_dane_v1/flat_flow.json"
# machinesNumber = 12
# r = 1
# c = 12

#HARD
# cost_file = "flo_dane_v1/hard_cost.json"
# flow_file = "flo_dane_v1/hard_flow.json"
# machinesNumber = 24
# r = 5
# c = 6

costList = loadCostFile(cost_file, machinesNumber)
flowList = loadFlowFile(flow_file, machinesNumber)

populationNum = 100
numOfGenerations = 10
population = []
best_list = []
average_list = []
worst_list = []

for i in range(populationNum):
    temp = Specimen(c,r,machinesNumber)
    temp.generateMachines()
    population.append((temp, getAdaptation(costList,flowList,temp,machinesNumber)))

for gen in range(numOfGenerations):
    select = Selection(population)
    next_gen = []
    numOfElites = 4
    best = sys.maxsize * 2 + 1
    bestIndex = -1
    worst = -1
    worstIndex = -1
    sum = 0

    for index, specimen in enumerate(population):
        sum += specimen[1]
        if specimen[1] < best:
            best = specimen[1]
            bestIndex = index
        if specimen[1] > worst:
            worst = specimen[1]
            worstIndex = index

    best_indexes = select.getElites(numOfElites)

    for i in best_indexes:
        next_gen.append(population[i])

    remainingNum = populationNum - numOfElites

    for i in range(int(remainingNum/2)):
        p1_index = select.roulette(sum)
        p2_index = select.roulette(sum)

        while p1_index == p2_index:
            p2_index = select.roulette(sum)


        cross = Crossover(population, c, r)
        c1_machines, c2_machines = cross.single_point(p1_index, p2_index)

        child1 = Specimen(c,r,machinesNumber)
        child2 = Specimen(c,r,machinesNumber)
        child1.inheritMachines(c1_machines, True)
        child2.inheritMachines(c2_machines, True)
        next_gen.append((child1, getAdaptation(costList,flowList,child1,machinesNumber)))
        next_gen.append((child2, getAdaptation(costList,flowList,child2,machinesNumber)))

    for spec in population:
        print(spec[1], end=', ')
    print()
    population = next_gen

    average = sum / populationNum

    print("Average: " + str(average))
    print("Best: " + str(best))
    print("Worst: " + str(worst))

    average_list.append(average)
    best_list.append(best)
    worst_list.append(worst)
