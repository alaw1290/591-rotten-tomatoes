import movie_reviews_compiler
import random

path = '../data/'

movieToCritics, criticToMovies, matrix, movieKeys, criticKeys = movie_reviews_compiler.import_pickle()

def getLength(l):
    count = 0
    for x in l:
        if x != 0:
            count += 1
    return count

lengths = list(map(getLength, matrix))

testCritics = []
reviews     = 5
while(True):
    for x in range(0,len(lengths)):
        if(lengths[x] == reviews):
            testCritics.append(criticKeys[x])
            if(len(testCritics) == 600):
                break;
            
    if(len(testCritics) == 600):
        break;   
    reviews += 1

realTestCritics = []
for x in range(0, 100):
    r   = int(random.random()*len(testCritics))
    realTestCritics.append(testCritics.pop(r))

##theOthers = []
##for x in range(0, len(lengths)):
##    if criticKeys[x] not in realTestCritics:
##        theOthers.append(criticKeys[x])

toReturn = []
for x in realTestCritics:
    toReturn.append(criticKeys.index(x))

print(len(toReturn))
