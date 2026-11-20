import os

import kagglehub as kh
import pandas as pd

def parseBTCData():
    path = kh.dataset_download("felixvo/15m-btcusdt")
    file = os.path.join(path, "15m_BTCUSDT.csv")
    data = pd.read_csv(file)
    return data
def upsOrDowns(data):
    #Indexes starting at period 1, not 0
    arr = [0] * (data.shape[0]-1)
    for i in range (data.shape[0]-1):
        if data.iloc[i+1,4] > data.iloc[i,4]:
            arr[i] = 'U'
        else:
            arr[i] = 'D'
    return arr