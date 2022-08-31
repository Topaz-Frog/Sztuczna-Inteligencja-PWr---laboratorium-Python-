import random
from utilis import createNelemList
import random

class Specimen():
    def __init__(self, C, R, machinesNum):
        self.machines = []
        self.C = C
        self.R = R
        self.machinesNum = machinesNum
        self.mutationProb = 0.05

    def generateMachines(self):
        helper = createNelemList(self.C * self.R, self.machinesNum)
        random.shuffle(helper)
        self.machines = []

        for r in range(self.R):
            tempList = []
            for c in range(self.C):
                tempList.append(helper[0])
                del helper[0]
            self.machines.append(tempList)

    def inheritMachines(self, machines):
        self.machines = []
        index = 0
        for r in range(self.R):
            tempList = []
            for c in range(self.C):
                tempList.append(machines[index])
                index += 1
            self.machines.append(tempList)

    def checkMutation1(self):
        if (random.random() < self.mutationProb):
            pos1 = random.randint(0, self.machinesNum - 1)
            pos2 = random.randint(0, self.machinesNum - 1)
            
            while pos1 == pos2:
                pos2 = random.randint(0, self.machinesNum - 1)

            machines_flat = []

            for list in self.machines:
                for machine in list:
                    machines_flat.append(machine)

            first_ele = machines_flat.pop(pos1)  
            second_ele = machines_flat.pop(pos2-1)
            
            machines_flat.insert(pos1, second_ele)
            machines_flat.insert(pos2, first_ele)

            self.inheritMachines(machines_flat)
            self.checkMutation1

    def checkMutation2(self):
        if (random.random() < self.mutationProb):
            pos = random.randint(0, self.machinesNum - 1)
            machines_flat = []

            for list in self.machines:
                for machine in list:
                    machines_flat.append(machine)

            machines_flat.append(machines_flat.pop(pos))
            self.inheritMachines(machines_flat)
