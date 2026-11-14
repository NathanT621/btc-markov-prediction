import numpy as np
import pandas as pd
import random
import kagglehub as kh
import os
def generateSimpleStep(p):
    result = (int) (random.random()<p)
    return result
def simpleRandomWalk(S_0, p, n):
    if p<0 or p>1:
        return
    S = S_0
    for i in range(n):
        S = S + generateSimpleStep(p)
    return S
def parseBTCData():
    path = kh.dataset_download("felixvo/15m-btcusdt")
    file = os.path.join(path, "15m_BTCUSDT.csv")
    data = pd.read_csv(file)

    print(data.head())
    print(data.columns)
    print(data.shape)
    return data
def upsOrDowns(data):
    #Indexes starting at period 1, not 0
    arr = [0] * (data.shape[0]-1)
    for i in range (data.shape[0]-1):
        if data.iloc[i+1,4] > data.iloc[i,4]:
            arr[i] = 'U'
        else:
            arr[i] = 'D'
    for i in range(5):
        print(arr[i])
    return arr
def getTransitionMatrix(trainData):
    uuCount = 0
    udCount = 0
    ddCount = 0
    duCount = 0
    for i in range(len(trainData)-1):
        if trainData[i]=='U':
            if trainData[i+1]=='U':
                uuCount += 1
            else: udCount += 1
        else:
            if trainData[i+1]=='D':
                ddCount += 1
            else: duCount += 1
    p = np.zeros((2,2))
    total1 = udCount + uuCount
    total2 = ddCount + duCount
    p[0][0] = uuCount / total1
    p[0][1] = udCount / total1
    p[1][0] = duCount / total2
    p[1][1] = ddCount / total2
    print(p)
    print(p.sum(axis=1))
    return p
def secondOrderTransitionMatrix(trainData):
    counts = {
        "UU": [0, 0],
        "UD": [0, 0],
        "DU": [0, 0],
        "DD": [0, 0]
    }

    for i in range(len(trainData)-2):
        if trainData[i] == 'U':
            if trainData[i+1] == 'U':
                if trainData[i+2] == 'U':
                    counts["UU"][0] += 1
                else:
                    counts["UU"][1] += 1
            else:
                if trainData[i+2] == 'U':
                    counts["UD"][0] += 1
                else:
                    counts["UD"][1] += 1
        else:
            if trainData[i+1] == 'D':
                if trainData[i+2] == 'D':
                    counts["DD"][1] += 1
                else:
                    counts["DD"][0] += 1
            else:
                if trainData[i+2] == 'D':
                    counts["DU"][1] += 1
                else:
                    counts["DU"][0] += 1

    probabilities = {}

    for pattern in counts:
        total = counts[pattern][0] + counts[pattern][1]

        if total > 0:
            probabilities[pattern] = [
                counts[pattern][0] / total,
                counts[pattern][1] / total
            ]
        else:
            probabilities[pattern] = [0.5, 0.5]

    return probabilities
def test2DModel(testData, probabilities):
     correct = 0
     total = 0
     pointer1 = 0
     pointer2 = 1
     
     for i in range(2, len(testData)):
         pattern = testData[pointer1] + testData[pointer2]
         prediction = ''
         if probabilities[pattern][0] > probabilities[pattern][1]:
             prediction = 'U'
         else: prediction = 'D'
         if (prediction==testData[i]):
             correct += 1
         pointer1 += 1
         pointer2 += 1
         total += 1
     return correct / total
         
        
             
def testModel(testData, p):
    correct = 0
    total = 0

    uPred = ''
    dPred = ''
    if (p[0][0]>p[0][1]):
        uPred = 'U'
    else:
        uPred= 'D'
    if (p[1][0]>p[1][1]):
        dPred='U'
    else:
        dPred='D'
    for i in range(len(testData)-1):
        if testData[i] == 'U':
            if testData[i+1] == uPred:
                correct += 1
        else:
            if testData[i+1] == dPred:
                correct += 1
        total += 1
    return correct / total 
def baselineAccuracy(trainData):
    uFreq = 0
    dFreq = 0
    for i in range(len(trainData)):
        if trainData[i] == "U":
            uFreq += 1
        else: dFreq += 1  
    p = np.zeros((2,2))
    if uFreq > dFreq:
        p[0][0] = 1
        p[1][0] = 1
    else:
        p[0][1] = 1
        p[1][1] = 1
    return p
data = parseBTCData()
movements = upsOrDowns(data)
split = int(len(movements)*0.8)
trainData = movements[:split]
testData = movements[split:]
p = getTransitionMatrix(trainData)
print("1D Accuracy:", testModel(testData, p))
print("2D Accuracy:", test2DModel(testData, secondOrderTransitionMatrix(trainData)))
print("Baseline Accuracy:", testModel(testData,baselineAccuracy(trainData)))
segmentSize = len(testData) // 10

for i in range(10):
    start = i * segmentSize

    if i == 9:
        end = len(testData)
    else:
        end = (i + 1) * segmentSize

    segment = testData[start:end]

    accuracy = testModel(segment, p)
    print(f"Period {i+1}: {accuracy * 100:.2f}%")