import copy
import random
import time
from utilis import f_check_ineq, f_check_sv_row, f_check_sv_col, printPuzzle, b_check_row_sum, b_check_col_sum, b_check_sv_row, b_check_sv_col, containsNone
from constraints import checkBinSum, checkInequality, checkRowUnique, checkForSameValues

class Algorithms():
    def __init__(self, puzzle, isBinary, isForward, isHeur, constraints):
        self.puzzle = puzzle
        self.isBinary = isBinary
        self.isForward = isForward
        self.isHeur = isHeur
        self.n = len(self.puzzle)
        self.constraints = constraints
        self.scopes = self.getScopes()
        self.solutions = []
        self.nodes_count = 0
        self.returns_count = 0
        self.start_time = time.time()
        self.foundfirst = False

    def heurTracking(self):
        if self.isHeur:
            self.shuffleScopes()
        tempSolution = copy.deepcopy(self.puzzle)
        tempScopes = copy.deepcopy(self.scopes)
        r,c = self.getStartPoint(tempSolution,tempScopes)

        print("starting from:",r,c)
        self.heurTrackingRec(r,c,tempSolution, tempScopes)
        self.fixSolutions()

    def heurTrackingRec(self,r,c,tempSolution, tempScopes):
        # print(r,c)
        # x = self.countNones(tempSolution)
        # if x < 20:
        #     printPuzzle(tempSolution)
        self.nodes_count += 1
        
        tScopes = copy.deepcopy(tempScopes)
        tSolution = copy.deepcopy(tempSolution)
        
        if not tSolution[r][c].isSet:
            if self.isForward:
                tScopes = self.updateScopes(tSolution, tScopes, r, c)
            if tScopes[r][c] != []:
                found = False
                for i in tScopes[r][c]:
                    tSolution[r][c].value = i
                    if self.checkConstraints(tSolution, tempScopes):
                        # tScopes1 = copy.deepcopy(tScopes)
                        nextR,nextC = self.getStartPoint(tSolution,tScopes)
                        if nextR != -1 or nextC != -1:
                            found = True
                            self.heurTrackingRec(nextR,nextC,tSolution,tempScopes)
                        
                        elif self.countNones(tSolution) == 0:
                            found = True
                            if (self.checkConstraints(tSolution, tempScopes) and self.solutions.count(tSolution) == 0 and not containsNone(tSolution)):
                                tSolution1 = copy.deepcopy(tSolution)
                                if not self.foundfirst:
                                    print("1st found")
                                    print("%s ms" % round(((time.time() - self.start_time)*1000),2))
                                    print(self.returns_count)
                                    print(self.nodes_count)
                                    self.foundfirst = True
                                # print('x',end='')
                                self.solutions.append(tSolution1)
                                # printPuzzle(tSolution)
                    tSolution[r][c].value = None
                if not found:
                    self.returns_count += 1
                # print("x")

    def tracking(self):
        if self.isHeur:
            self.shuffleScopes()
        tempSolution = copy.deepcopy(self.puzzle)
        tempScopes = copy.deepcopy(self.scopes)
        r = 0
        c = 0

        self.trackingRecursive(r,c,tempSolution, tempScopes)
        self.fixSolutions()

    def trackingRecursive(self,r,c,tempSolution, tempScopes):
        tScopes = copy.deepcopy(tempScopes)
        self.nodes_count += 1

        if (r != self.n-1 and c == self.n-1):
            if (tempSolution[r][c].value == None):
                if self.isForward:
                    tScopes = self.updateScopes(tempSolution, tScopes, r, c)
                if tScopes != []:
                    found = False
                    for i in tScopes[r][c]:
                        tempSolution[r][c].value = i
                        if self.checkConstraints(tempSolution, tempScopes):
                            self.trackingRecursive(r+1,0,tempSolution, tempScopes)
                            found = True
                        tempSolution[r][c].value = None
                    if not found:
                        self.returns_count += 1
            else:
                self.trackingRecursive(r+1,0,tempSolution, tempScopes)

        elif (r <= self.n and c < self.n-1):
            if (tempSolution[r][c].value == None):
                if self.isForward:
                    tScopes = self.updateScopes(tempSolution, tScopes, r, c)
                if tScopes != []:
                    found = False
                    for i in tScopes[r][c]:
                        tempSolution[r][c].value = i
                        if self.checkConstraints(tempSolution, tempScopes):
                            self.trackingRecursive(r,c+1,tempSolution, tempScopes)
                            found = True
                        tempSolution[r][c].value = None
                    if not found:
                        self.returns_count += 1
            else:
                self.trackingRecursive(r,c+1,tempSolution, tempScopes)

        elif (r == self.n-1 and c == self.n-1):
            if (tempSolution[r][c].value == None):
                if  self.isForward:
                    tScopes = self.updateScopes(tempSolution, tScopes, r, c)
                if tScopes != []:
                    found = False
                    for i in tScopes[r][c]:
                        tempSolution[r][c].value = i
                        if (self.checkConstraints(tempSolution, tempScopes) and self.solutions.count(tempSolution) == 0):
                            if not self.foundfirst:
                                print("1st found")
                                print("%s ms" % round(((time.time() - self.start_time)*1000),2))
                                print(self.returns_count)
                                print(self.nodes_count)
                                self.foundfirst = True
                            # print("x", end="")
                            self.solutions.append(copy.deepcopy(tempSolution))
                            # printPuzzle(tempSolution)
                            # print()
                            found = True
                        tempSolution[r][c].value = None
                    if not found:
                        self.returns_count += 1
    def checkConstraints(self, testPuzzle, tempScopes):
        if self.isBinary:
            if not checkBinSum(testPuzzle, self.n) or not checkForSameValues(testPuzzle,self.isBinary,self.n) or not checkRowUnique(testPuzzle, self.n):
                return False
        else:
            if not checkInequality(self.constraints,testPuzzle,self.n,tempScopes) or not checkForSameValues(testPuzzle,self.isBinary,self.n):
                return False
        return True
    
    def fixSolutions(self):
        # print("fixing")
        # if self.isBinary:
        #     for solution1 in self.solutions:
        #         printPuzzle(solution1)
        #         print()
        sol1_Idx = 0
        for solution1 in self.solutions:
            sol2_Idx = 0
            for solution2 in self.solutions:
                if (solution1 == solution2 and sol1_Idx != sol2_Idx):
                    self.solutions.remove(solution2)
                sol2_Idx+=1
            if containsNone(solution1):
                self.solutions.remove(solution1)
            sol1_Idx+=1

        # if not self.isBinary:
        #     for solution1 in self.solutions:
        #         if not (self.checkConstraints):
        #             printPuzzle(solution1)

    def updateScopes(self, tempSolution, tScopes, r, c):
        if self.isBinary:
            row0Sum, row1Sum = b_check_row_sum(tempSolution, r)
            if (row0Sum == self.n/2 or row1Sum == self.n/2):
                for col_Idx in range(self.n):
                    if (tempSolution[r][col_Idx].value == None):
                        if row0Sum == self.n/2 and 0 in tScopes[r][col_Idx]:
                            tScopes[r][col_Idx].remove(0)
                        if row1Sum == self.n/2 and 1 in tScopes[r][col_Idx]:
                            tScopes[r][col_Idx].remove(1)
            
            col0Sum, col1Sum = b_check_col_sum(tempSolution, self.n, c)
            if (col0Sum == self.n/2 or col1Sum == self.n/2):
                for row_Idx in range(self.n):
                    if (tempSolution[row_Idx][c].value == None):
                        if col0Sum == self.n/2 and 0 in tScopes[row_Idx][c]:
                            tScopes[row_Idx][c].remove(0)
                        if col1Sum == self.n/2 and 1 in tScopes[row_Idx][c]:
                            tScopes[row_Idx][c].remove(1)

            rptd_row_Idx, val_row = b_check_sv_row(tempSolution,self.n,r)
            if (rptd_row_Idx != -1 and rptd_row_Idx < self.n):
                if (val_row == 0 and 0 in tScopes[r][rptd_row_Idx]):
                    tScopes[r][rptd_row_Idx].remove(0)
                elif (val_row == 1 and 1 in tScopes[r][rptd_row_Idx]):
                    tScopes[r][rptd_row_Idx].remove(1)

            rptd_col_Idx, val_col = b_check_sv_col(tempSolution,self.n,c)
            if (rptd_col_Idx != -1 and rptd_col_Idx < self.n):
                if (val_col == 0 and 0 in tScopes[rptd_col_Idx][c]):
                    tScopes[rptd_col_Idx][c].remove(0)
                elif (val_col == 1 and 1 in tScopes[rptd_col_Idx][c]):
                    tScopes[rptd_col_Idx][c].remove(1)

            return tScopes
        else:
            tScopes[r][c] = f_check_sv_row(tempSolution,tScopes,self.n,r,c)
            tScopes[r][c] = f_check_sv_col(tempSolution,tScopes,self.n,r,c)
            tScopes[r][c] = f_check_ineq(tempSolution,tScopes,self.n,r,c,self.constraints)
            return tScopes

    def getScopes(self):
        if self.isBinary:
            scopes = []
            for row in self.puzzle:
                tempRow = []
                for elem in row:
                    if elem is not None:
                        tempRow.append([0,1])
                scopes.append(tempRow)
        else:
            scopes = []
            for row in self.puzzle:
                tempRow = []
                for elem in row:
                    tempRow.append(elem.scope)
                scopes.append(tempRow)
        return scopes

    def getStartPoint(self, tSolution, tScopes):
        picked_start = (-1,-1)
        min_s_len = self.n + 1

        for i in range(self.n):
            for j in range(self.n):
                if tSolution[i][j].value == None:
                    if len(tScopes[i][j]) < min_s_len:
                        picked_start = (i,j)
                        min_s_len = len(tScopes[i][j])

        return picked_start
    
    def shuffleScopes(self):
        for row  in self.scopes:
            for elem in row:
                random.shuffle(elem)

    def countNones(self, tSolution):
        counter = 0
        for row in tSolution:
            for elem in row:
                if elem.value is None:
                    counter += 1
        
        return counter
            