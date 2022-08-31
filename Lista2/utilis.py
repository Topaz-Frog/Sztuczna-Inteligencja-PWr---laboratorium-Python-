from futoshiki import Futoshiki
from binary import Binary

def readBinaryFile(path):
    with open(path) as f:
        lines = f.readlines()
    
    list = []
    scope = [0,1]
    row_Idx = 0

    for line in lines:
        tempValues = []
        col_Idx = 0
        for letter in line:
            if (letter != '\n'):
                value = None
                if (letter == '0'):
                    value = 0
                elif (letter == '1'):
                    value = 1

                temp = Binary(scope, value, row_Idx, col_Idx)
                if value is not None:
                    temp.isSet = True
                tempValues.append(temp)
                col_Idx += 1
        if (len(tempValues) > 0):
            list.append(tempValues)
            row_Idx += 1
            
    for row in list:
        for elem in row:
            if type(elem) is int:
                elem.scope = [elem]

    return list

def readFutoFile(path):
    with open(path) as f:
        lines = f.readlines()
    
    list = []
    constraints = []
    scope = [*range(1, len(lines[1]))]
    row_Idx = 0

    for line in lines:
        tempValues = []
        tempConstraints = []
        col_Idx = 0
        for letter in line:
            if (letter == '-' or letter == '<' or letter == '>'):
                tempConstraints.append(letter)
            elif (letter != '\n'):
                value = None
                if (letter == '1'):
                    value = 1
                elif (letter == '2'):
                    value = 2
                elif (letter == '3'):
                    value = 3
                elif (letter == '4'):
                    value = 4
                elif (letter == '5'):
                    value = 5
                elif (letter == '6'):
                    value = 6
                temp = Futoshiki(scope, value, row_Idx, col_Idx)
                
                if value is not None:
                    temp.isSet = True
                tempValues.append(temp)
                col_Idx += 1
        constraints.append(tempConstraints)
        if (len(tempValues) > 0):
            list.append(tempValues)
            row_Idx += 1
            
    for row in list:
        for elem in row:
            if type(elem) is int:
                elem.scope = [elem]
            else:
                elem.getScope(constraints, list)

    return constraints, list

def printPuzzle(puzzle):
    for row in puzzle:
        for futo in row:
            print(futo.value, end=', ')
        print()

def containsNone(puzzle):
    for row in puzzle:
        for elem in row:
            if elem.value == None:
                return True

def b_check_row_sum(puzzle, r):
    row0Sum = 0
    row1Sum = 0
    for elem in puzzle[r]:
        if (elem.value == 0):
            row0Sum+=1
        elif (elem.value == 1):
            row1Sum+=1
    # print("check_row_sum, r: ", row0Sum, row1Sum)
    return row0Sum, row1Sum 
    
def b_check_col_sum(puzzle, n, c):
    col0Sum = 0
    col1Sum = 0
    for row in range(n):
        if (puzzle[row][c].value == 0):
            col0Sum+=1
        elif (puzzle[row][c].value == 1):
            col1Sum+=1
            
    # print("check_col_sum, r: ", col0Sum, col1Sum)
    return col0Sum, col1Sum

def b_check_sv_row(puzzle, n, r):
    rptd_Idx = -1
    val = -2
    for col in range(n - 2):
        if (puzzle[r][col].value != None and puzzle[r][col+1].value != None and puzzle[r][col+2].value == None and puzzle[r][col].value == puzzle[r][col+1].value and puzzle[r][col].value != None):
            rptd_Idx = col+2
            val = puzzle[r][col].value

    # print("check_sv_row, r: ", rptd_Idx, val)
    return rptd_Idx, val

def b_check_sv_col(puzzle, n, c):
    rptd_Idx = -1
    val = -2
    for row in range(n - 2):
        if (puzzle[row][c].value == puzzle[row + 1][c].value and puzzle[row][c].value != None and puzzle[row+1][c].value != None and puzzle[row+2][c].value == None):
            rptd_Idx = row+2
            val = puzzle[row][c].value

    # print("check_sv_col, r: ", rptd_Idx, val)  
    return rptd_Idx, val

def f_check_sv_row(puzzle, scopes, n, r, c):
    temp_scope = scopes[r][c]
    for elem in puzzle[r]:
        if elem.value != None and elem.value in temp_scope:
            temp_scope.remove(elem.value)
    return temp_scope

def f_check_sv_col(puzzle, scopes, n, r, c):
    temp_scope = scopes[r][c]
    for row_Idx in range(n):
        if puzzle[row_Idx][c].value != None and puzzle[row_Idx][c].value in temp_scope:
            temp_scope.remove(puzzle[row_Idx][c].value)
    return temp_scope

def f_check_ineq(puzzle,scopes,n,r,c,listConstraints):
    temp_scope = scopes[r][c]

    if (c >= 0 and c < n-1):
        if (type(puzzle[r][c+1].value) is int and temp_scope != []):
            if (listConstraints[(2*r)][c] == '>'):
                for s in temp_scope:
                    if (s <= puzzle[r][c+1].value):
                        temp_scope.remove(s)
            elif (listConstraints[(2*r)][c] == '<'):
                for s in temp_scope:
                    if (s >= puzzle[r][c+1].value):
                        temp_scope.remove(s)

    if (c > 0 and c <= n-1):
        if (type(puzzle[r][c-1].value) is int and temp_scope != []):
            if (listConstraints[(2*r)][c-1] == '>'):
                for s in temp_scope:
                    if (s >= puzzle[r][c-1].value):
                        temp_scope.remove(s)
            elif (listConstraints[(2*r)][c-1] == '<'):
                for s in temp_scope:
                    if (s <= puzzle[r][c-1].value):
                        temp_scope.remove(s)

    if (r >= 0 and r < n-1):
        if (type(puzzle[r+1][c].value) is int and temp_scope != []):
            if (listConstraints[(2*r)+1][c] == '>'):
                for s in temp_scope:
                    if (s <= puzzle[r+1][c].value):
                        temp_scope.remove(s)
            elif (listConstraints[(2*r)+1][c] == '<'):
                tempScope = []
                for s in temp_scope:
                    if (s >= puzzle[r+1][c].value):
                        temp_scope.remove(s)
                temp_scope = tempScope

    if (r > 0 and r <= n-1):
        if (type(puzzle[r-1][c].value) is int and temp_scope != []):
            if (listConstraints[(2*r)-1][c] == '>'):
                for s in temp_scope:
                    if (s >= puzzle[r-1][c].value):
                        temp_scope.remove(s)
            elif (listConstraints[(2*r)-1][c] == '<'):
                for s in temp_scope:
                    if (s <= puzzle[r-1][c].value):
                        temp_scope.remove(s)
    return temp_scope
