import json
from webbrowser import get
from random import random, shuffle
import numpy as np

def loadCostFile(filename, machinesNum):
    f = open(filename)
    data = json.load(f)
    list = []

    for i in range(machinesNum):
        helpList = [0] * machinesNum
        list.append(helpList)
        
    for i in data:
        list[i['source']][i['dest']] = i['cost']
    
    return list

def loadFlowFile(filename, machinesNum):
    f = open(filename)
    data = json.load(f)
    list = []

    for i in range(machinesNum):
        helpList = [0] * machinesNum
        list.append(helpList)

    for i in data:
        list[i['source']][i['dest']] = i['amount']

    return list

def createNelemList(nFields, machinesNum):
    l = []
    for i in range(machinesNum):
        l.append(i)
    for i in range(nFields - machinesNum):
        l.append(None)
    return l

def getDistance(x_i: int, y_i: int, x_j: int, y_j: int) -> int:
    return abs(x_i-x_j) + abs(y_i-y_j)

def getCoordinates(specimen, searched):
    for index, row in enumerate(specimen.machines):
        if searched in row:
            return (row.index(searched), index)

def getFitness(costList,flowList,specimen,machinesNum):
    fitness = 0

    for i in range(machinesNum):
        for j in range(machinesNum):
            (x_i, y_i) = getCoordinates(specimen, i)
            (x_j, y_j) = getCoordinates(specimen, j)
            distance = getDistance(x_i, y_i, x_j, y_j)
            
            fitness += costList[i][j] * flowList[i][j] * distance
    
    return fitness

def sortTupleList(list):
    lst = len(list) 
    for i in range(0, lst): 
        for j in range(0, lst-i-1): 
            if (list[j][1] > list[j + 1][1]): 
                temp = list[j] 
                list[j]= list[j + 1] 
                list[j + 1]= temp 
    return list 

def getAverage(list):
    return sum(list) / len(list)
