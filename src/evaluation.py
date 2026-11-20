def testNDModel(testData, probabilities, n):
    correct = 0
    total = 0
    for i in range(n, len(testData)):
        pattern = ''.join(testData[i-n:i])
        prediction = ''
        if probabilities[pattern][0] > probabilities[pattern][1]:
                prediction = 'U'
        else: prediction = 'D'
        if (prediction==testData[i]):
            correct += 1
        total += 1
    return correct / total
def baselineAccuracy(trainData,testData):
    uFreq = 0
    dFreq = 0
    for i in range(len(trainData)):
        if trainData[i] == "U":
            uFreq += 1
        else: dFreq += 1  
    testFreq = 0
    if uFreq > dFreq:
        for i in range(len(testData)):
            if (testData[i]=='U'):
                testFreq+=1
    else:
        for i in range(len(testData)):
            if (testData[i]=='D'):
                testFreq+=1
    return testFreq / len(testData)
