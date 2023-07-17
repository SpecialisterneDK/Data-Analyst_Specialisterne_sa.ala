import sys
from pathlib import Path
import os
import subprocess as sp
import pandas as pd
import matplotlib.pyplot as plt

def getLocation():
    return sys.argv[1]

def getCsvsInDirectory(directory):
    csvs = []
    for dI in os.listdir(directory):
        combinedPath = os.path.join(directory, dI)
        if os.path.isdir(combinedPath):
            for csv in getCsvsInDirectory(combinedPath):
                csvs.append(csv)
        if combinedPath.endswith(".csv"):
            csvs.append(combinedPath.replace(getLocation(), ""))
    return csvs

def createDataFrame(csvs):
    df = pd.DataFrame({'template_key': [], 'date': [], 'position': [], 'a': [], 'b': [], 'c': [], 'd': [], 'weight': []})
    for csv in csvs:
        df = df._append(pd.read_csv(getLocation()+csv))
    return df
    
def getTemplateKeys(df):
    keys = []
    for key in df["template_key"]:
        keys.append(key)
    keys = list(dict.fromkeys(keys))
    return keys

def getPositions(df):
    positions = []
    for position in df["position"]:
        positions.append(position)
    positions = list(dict.fromkeys(positions))
    return positions

def saveScattersFromCsvs(df):
    for k in getTemplateKeys(df):
        df_keyed = df.loc[df["template_key"] == k]
        for p in getPositions(df):
            df_positioned = df.loc[df["position"] == p]
            for v in ["a", "b", "c", "d", "weight"]:
                saveScatterFromCsvs(df_positioned, k, p, v)

def saveScatterFromCsvs(df, templateKey, position, valueName):
    x = df["date"]
    y = df[valueName]
    fig, ax = plt.subplots()
    ax.scatter(x, y, alpha=0.5)
    average = df[valueName].mean()
    std = df[valueName].std()
    ax.axhline(y = average, color = 'r', linestyle='dotted')
    ax.axhline(y = average+std, color = 'g', linestyle='dotted')
    ax.axhline(y = average-std, color = 'g', linestyle='dotted')
    plt.xlabel("Dato")
    plt.ylabel("Værdien af " + valueName)
    savePlot(templateKey, position, valueName)
    
def savePlot(templateKey, position, valueName):
    filePath = getLocation() + "/" + templateKey + "-" + position + "-" + valueName
    print("saving \"" + filePath + "\"")
    plt.savefig(filePath)

csvs = getCsvsInDirectory(getLocation())
df = createDataFrame(csvs)
df.date = pd.to_datetime(df.date, format="ISO8601")

saveScattersFromCsvs(df)