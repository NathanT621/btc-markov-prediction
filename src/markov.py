from itertools import product
def nOrderTransitionMatrix(n,trainData):
    counts = {}
    patterns = product(['U', 'D'], repeat=n)
    for pattern in patterns:
        seen = ''.join(pattern)
        counts[seen] = [0,0]
    probabilities = {}
    for i in range(len(trainData)-n):
        if trainData[i+n] == 'U':
            counts[''.join(trainData[i:i+n])][0] += 1 
        else:
            counts[''.join(trainData[i:i+n])][1] += 1 
    for pattern in counts:
        probabilities[pattern]=[0,0]
        probabilities[pattern][0] = counts[pattern][0] / (counts[pattern][0]+counts[pattern][1])
        probabilities[pattern][1] = counts[pattern][1] / (counts[pattern][0]+counts[pattern][1])
    return probabilities