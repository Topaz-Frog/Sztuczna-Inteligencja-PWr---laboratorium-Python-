from utilis import readBinaryFile, readFutoFile
from alghoritms import Algorithms
import time


isHeur = False
# isHeur = True

isHeurScope = False
# isHeurScope = True

isForward = False
# isForward = True

isBinary = True
# filename = "binary-futoshiki_dane_v1/binary_6x6"
# filename = "binary-futoshiki_dane_v1/binary_8x8"
# filename = "binary-futoshiki_dane_v1/binary_10x10"

isBinary = False
filename = "binary-futoshiki_dane_v1/futoshiki_4x4"
# filename = "binary-futoshiki_dane_v1/futoshiki_5x5"
# filename = "binary-futoshiki_dane_v1/futoshiki_6x6"

for i in range(4):
    start_time = time.time()
    if i == 1:
        isHeurScope = True
    if i == 2:
        isHeurScope = False
        isHeur = True
    if i == 3:
        isHeurScope = True
    print(isHeur, isHeurScope)

    if isBinary:
        thePuzzle = readBinaryFile(filename)
        alg = Algorithms(thePuzzle, isBinary, isForward, isHeurScope, None)
    else:
        constraints, thePuzzle = readFutoFile(filename)
        alg = Algorithms(thePuzzle, isBinary, isForward, isHeurScope, constraints)

    if isHeur:
        alg.heurTracking()
    else:
        alg.tracking()
    
    print("%s ms" % round(((time.time() - start_time)*1000),2))
    print(len(alg.solutions))
    print(alg.returns_count)
    print(alg.nodes_count)
    print()
