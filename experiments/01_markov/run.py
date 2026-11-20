from src.data import parseBTCData, upsOrDowns
from src.markov import nOrderTransitionMatrix
from src.evaluation import testNDModel, baselineAccuracy
from matplotlib.ticker import PercentFormatter
import matplotlib.pyplot as plt
import numpy as np
import os

data = parseBTCData()
movements = upsOrDowns(data)

split = int(len(movements) * 0.8)
trainData = movements[:split]
testData = movements[split:]

baseline = baselineAccuracy(trainData, testData)
yaxis = np.zeros(9)

print(f"Baseline Accuracy: {baseline:.4%}")

for n in range(1, 10):
    p = nOrderTransitionMatrix(n, trainData)
    accuracy = testNDModel(testData, p, n)
    yaxis[n - 1] = accuracy
    print(f"Order {n}: {accuracy:.4%}")

order = np.arange(1, 10)

plt.plot(order, yaxis)
plt.axhline(y=baseline, linestyle='--', label='Baseline')
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.xlabel("Markov Order")
plt.ylabel("Test Accuracy")
plt.ylim(0.40, 0.60)
plt.plot(order, yaxis, marker='o', label='Markov Model')
plt.xticks(order)
plt.title("BTC Direction Prediction Accuracy by Markov Order")
plt.legend()
os.makedirs("experiments/01_markov/figures", exist_ok=True)
plt.tight_layout()
plt.savefig("experiments/01_markov/figures/accuracy.png", dpi=300)
plt.show()