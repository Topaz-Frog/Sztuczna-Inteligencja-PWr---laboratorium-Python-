class Futoshiki:
    def __init__(self, scope, value, r, c):
        self.scope = scope
        self.value = value
        self.r = r
        self.c = c
        self.isSet = False

    def getScope(self, listConstraints, values):
        # print(self.r,self.c, type(self.value))
        if (self.c >= 0 and self.c < len(listConstraints[0])):
            if (type(values[self.r][self.c+1].value) is int):
                if (listConstraints[(2 * self.r)][self.c] == '>'):
                    tempScope = []
                    for s in self.scope:
                        if (s > values[self.r][self.c+1].value):
                            tempScope.append(s)
                    self.scope = tempScope
                elif (listConstraints[(2 * self.r)][self.c] == '<'):
                    tempScope = []
                    for s in self.scope:
                        if (s < values[self.r][self.c+1].value):
                            tempScope.append(s)
                    self.scope = tempScope
        if (self.c > 0 and self.c <= len(listConstraints[0])):
            if (type(values[self.r][self.c-1].value) is int):
                if (listConstraints[(2 * self.r)][self.c-1] == '>'):
                    tempScope = []
                    for s in self.scope:
                        if (s < values[self.r][self.c-1].value):
                            tempScope.append(s)
                    self.scope = tempScope
                elif (listConstraints[(2 * self.r)][self.c-1] == '<'):
                    tempScope = []
                    for s in self.scope:
                        if (s > values[self.r][self.c-1].value):
                            tempScope.append(s)
                    self.scope = tempScope

        if (self.r >= 0 and self.r < len(listConstraints[0])):
            if (type(values[self.r+1][self.c].value) is int):
                if (listConstraints[(2 * self.r)+1][self.c] == '>'):
                    tempScope = []
                    for s in self.scope:
                        if (s > values[self.r+1][self.c].value):
                            tempScope.append(s)
                    self.scope = tempScope
                elif (listConstraints[(2 * self.r)+1][self.c] == '<'):
                    tempScope = []
                    for s in self.scope:
                        if (s < values[self.r+1][self.c].value):
                            tempScope.append(s)
                    self.scope = tempScope
        if (self.r > 0 and self.r <= len(listConstraints[0])):
            if (type(values[self.r-1][self.c].value) is int):
                if (listConstraints[(2 * self.r)-1][self.c] == '>'):
                    tempScope = []
                    for s in self.scope:
                        if (s < values[self.r-1][self.c].value):
                            tempScope.append(s)
                    self.scope = tempScope
                elif (listConstraints[(2 * self.r)-1][self.c] == '<'):
                    tempScope = []
                    for s in self.scope:
                        if (s > values[self.r-1][self.c].value):
                            tempScope.append(s)
                    self.scope = tempScope
    