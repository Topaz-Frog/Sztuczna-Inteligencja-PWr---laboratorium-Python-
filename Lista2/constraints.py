
def checkBinSum(puzzle, n):
    for row in puzzle:
        row0Sum = 0
        row1Sum = 0
        for elem in row:
            if (elem.value == 0):
                row0Sum+=1
            elif (elem.value == 1):
                row1Sum+=1
        if (row0Sum > n/2 or row1Sum > n/2):
            return False
    
    for col in range(n):
        col0Sum = 0
        col1Sum = 0
        for row in range(n):
            if (puzzle[row][col].value == 0):
                col0Sum+=1
            elif (puzzle[row][col].value == 1):
                col1Sum+=1
        if (col0Sum > n/2 or row1Sum > n/2):
            return False
            
    return True

def checkForSameValues(testPuzzle,isBinary,n):
    if isBinary:
        # checking if the same value appears 3 times in a row hehe
        for row in testPuzzle:
            for col in range(n - 2):
                if (row[col].value == row[col+1].value and row[col+1].value == row[col+2].value and row[col].value != None and row[col+1].value != None and row[col+2].value != None):
                    return False
        
        for col in range(n):
            for row in range(n - 2):
                if (testPuzzle[row][col].value == testPuzzle[row + 1][col].value and testPuzzle[row + 1][col].value == testPuzzle[row + 2][col].value and testPuzzle[row][col].value != None and testPuzzle[row+1][col].value != None and testPuzzle[row+2][col].value != None):
                    return False
    else:
        for row in testPuzzle:
            col1_Idx = 0
            for col1 in row:
                col2_Idx = 0
                for col2 in row:
                    if (col1.value == col2.value and col1_Idx != col2_Idx and col1.value != None and col2.value != None):
                        return False
                    col2_Idx+=1
                col1_Idx+=1
        
        for col in range(n):
            for row1 in range(n):
                for row2 in range(n):
                    if (testPuzzle[row1][col].value != None and testPuzzle[row2][col].value != None and row1 != row2 and testPuzzle[row1][col].value == testPuzzle[row2][col].value):
                        return False

    return True

def checkRowUnique(testPuzzle, n):
    # checking if every row and collumn is unique
    row1_Idx = 0
    for row1 in testPuzzle:
        row2_Idx = 0
        for row2 in testPuzzle:
            if (row1.count(None) == 0 and row2.count(None) == 0 and row1_Idx != row2_Idx and row1 == row2):
                return False
            row2_Idx += 1
        row1_Idx += 1

    col1_values = []
    for col1 in range(n):
        for row1 in range(n):
            col1_values.append(testPuzzle[row1][col1].value)
        
        col2_values = []
        for col2 in range(n):
            col2_values.clear()

            if (col1 != col2):
                for row2 in range(n):
                    col2_values.append(testPuzzle[row2][col2].value)
            if (col1_values.count(None) == 0 and col2_values.count(None) == 0 and col1_values == col2_values):
                return False

        col1_values.clear()

    return True

def checkInequality(listConstraints,testPuzzle,n,scopes):
    for r in range(n):
        for c in range(n):
            if (c >= 0 and c < n-1):
                if (type(testPuzzle[r][c+1].value) is int):
                    if (listConstraints[(2 * r)][c] == '>'):
                        tempScope = []
                        for s in scopes[r][c]:
                            if (s > testPuzzle[r][c+1].value):
                                if (testPuzzle[r][c].value == None):
                                    tempScope.append(s)
                                elif (testPuzzle[r][c].value > testPuzzle[r][c+1].value):
                                    tempScope.append(s)
                        if (len(tempScope) == 0):
                            # print('1')
                            return False
                    elif (listConstraints[(2 * r)][c] == '<'):
                        tempScope = []
                        for s in scopes[r][c]:
                            if (s < testPuzzle[r][c+1].value):
                                if (testPuzzle[r][c].value == None):
                                    tempScope.append(s)
                                elif (testPuzzle[r][c].value < testPuzzle[r][c+1].value):
                                    tempScope.append(s)
                        if (len(tempScope) == 0):
                            # print('2')
                            return False
            if (c > 0 and c <= len(listConstraints[0])):
                if (type(testPuzzle[r][c-1].value) is int):
                    if (listConstraints[(2 * r)][c-1] == '>'):
                        tempScope = []
                        for s in scopes[r][c]:
                            if (s < testPuzzle[r][c-1].value):
                                if (testPuzzle[r][c].value == None):
                                    tempScope.append(s)
                                elif (testPuzzle[r][c].value < testPuzzle[r][c-1].value):
                                    tempScope.append(s)
                        if (len(tempScope) == 0):
                            # print('3')
                            return False
                    elif (listConstraints[(2 * r)][c-1] == '<'):
                        tempScope = []
                        for s in scopes[r][c]:
                            if (s > testPuzzle[r][c-1].value):
                                if (testPuzzle[r][c].value == None):
                                    tempScope.append(s)
                                elif (testPuzzle[r][c].value > testPuzzle[r][c-1].value):
                                    tempScope.append(s)
                        if (len(tempScope) == 0):
                            # print('4')
                            return False

            if (r >= 0 and r < len(listConstraints[0])):
                if (type(testPuzzle[r+1][c].value) is int):
                    if (listConstraints[(2 * r)+1][c] == '>'):
                        tempScope = []
                        for s in scopes[r][c]:
                            if (s > testPuzzle[r+1][c].value):
                                if (testPuzzle[r][c].value == None):
                                    tempScope.append(s)
                                elif (testPuzzle[r][c].value > testPuzzle[r+1][c].value):
                                    tempScope.append(s)
                        if (len(tempScope) == 0):
                            # print('5')
                            return False
                    elif (listConstraints[(2 * r)+1][c] == '<'):
                        tempScope = []
                        for s in scopes[r][c]:
                            if (s < testPuzzle[r+1][c].value):
                                if (testPuzzle[r][c].value == None):
                                    tempScope.append(s)
                                elif (testPuzzle[r][c].value < testPuzzle[r+1][c].value):
                                    tempScope.append(s)
                        if (len(tempScope) == 0):
                            # print('6')
                            return False
            if (r > 0 and r <= len(listConstraints[0])):
                if (type(testPuzzle[r-1][c].value) is int):
                    if (listConstraints[(2 * r)-1][c] == '>'):
                        tempScope = []
                        for s in scopes[r][c]:
                            if (s < testPuzzle[r-1][c].value):
                                if (testPuzzle[r][c].value == None):
                                    tempScope.append(s)
                                elif (testPuzzle[r][c].value < testPuzzle[r-1][c].value):
                                    tempScope.append(s)
                        if (len(tempScope) == 0):
                            # print('7')
                            return False
                    elif (listConstraints[(2 * r)-1][c] == '<'):
                        tempScope = []
                        for s in scopes[r][c]:
                            if (s > testPuzzle[r-1][c].value):
                                if (testPuzzle[r][c].value == None):
                                    tempScope.append(s)
                                elif (testPuzzle[r][c].value > testPuzzle[r-1][c].value):
                                    tempScope.append(s)
                        if (len(tempScope) == 0):
                            # print('8')
                            return False
    return True