import numpy as np
import pandas as pd
import random
import kagglehub as kh
import os
from itertools import product
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

# segmentSize = len(testData) // 10

# for i in range(10):
#     start = i * segmentSize

#     if i == 9:
#         end = len(testData)
#     else:
#         end = (i + 1) * segmentSize

#     segment = testData[start:end]

#     accuracy = testModel(segment, p)
#     print(f"Period {i+1}: {accuracy * 100:.2f}%")
for n in range(1, 10):
    p = nOrderTransitionMatrix(n, trainData)
    accuracy = testNDModel(testData, p, n)
    print(f"Order {n}: {accuracy:.4%}")