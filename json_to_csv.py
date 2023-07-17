import pandas as pd
import requests
import sys
import json
from pathlib import Path

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 250)

def getJsonLocation():
    return sys.argv[1]
    
def getCsvLocation():
    return sys.argv[2]

class Experiment:
    template_key = ""
    date = ""
    a = 0.0
    b = 0.0
    c = 0.0
    d = 0.0
    position = ""
    weight = 0.0
    
def createExperiment(df, index):
    ex = Experiment()
    ex.template_key = getTemplateKey(df)
    ex.date = getDate(df)
    (ex.a, ex.b, ex.c, ex.d, ex.p) = getABCDP(df, index)
    ex.weight = getWeight(df, index)
    return ex

def getTemplateKey(df):
    df_meta = pd.json_normalize(df.QuantitativeResponseAssay.Meta)
    return df_meta["Template.Key"][0]
 
def getDate(df):
    df_meta = pd.json_normalize(df.QuantitativeResponseAssay.Meta)
    return df_meta["Creation.Time"][0][0:10]

def getWeight(df, index):
    df1 = pd.json_normalize(df.QuantitativeResponseAssay.AssayResults, max_level=0)
    df2 = pd.json_normalize(df1[df1.keys()[index]], max_level=0)
    df3 = pd.json_normalize(df2["StatisticTestResults"], max_level=0)
    df_weight = pd.json_normalize(df3["StatisticTestResult[3]"], max_level=0)
    return df_weight["Value"][0]
    
def getSize(df):
    return len(pd.json_normalize(df.QuantitativeResponseAssay.AssayResults, max_level=0).keys())
    
def getABCDP(df, index):
    df1 = pd.json_normalize(df.QuantitativeResponseAssay.AssayResults, max_level=0)
    df2 = pd.json_normalize(df1[df1.keys()[index]], max_level=0)
    df3 = pd.json_normalize(pd.json_normalize(df2["FullModel"], max_level=0)["FitResult"], max_level=0)

    a = 0
    b = 0
    c = 0
    d = 0
    p = ""

    for key in df3.keys():
        if "ParameterEstimate" in key:
            df4 = pd.json_normalize(df3[key], max_level=0)
            
            parameter = df4["ParameterName"][0]
            name = df4["AssayElementName"][0]
            value = df4["Value"][0]
            #std_error = df4["StdError"][0]
            
            if "Position" in str(name):
                if parameter == "A":
                    a = value
                if parameter == "B":
                    b = value
                if parameter == "C":
                    c = value
                if parameter == "D":
                    d = value
                p = name[9:]
    return (a, b, c, d, p)

def getExperiments(df):
    exs = []
    for i in range(getSize(df)):
        try:
            exs.append(createExperiment(df, i))
        except:
            print()
            #print("Failed to get P" + str(i) + ", most likely due to the fact that it doesn't exist.")
    return exs
    
def writeExperimentsToCsvFile(exs):
    elements = []
    for i in range(len(exs)):
        elements.append([])
        elements[i].append(exs[i].template_key)
        elements[i].append(exs[i].date)
        elements[i].append(exs[i].p)
        elements[i].append(exs[i].a)
        elements[i].append(exs[i].b)
        elements[i].append(exs[i].c)
        elements[i].append(exs[i].d)
        elements[i].append(exs[i].weight)
        
    columns = ['template_key', 'date', 'position', 'a', 'b', 'c', 'd', 'weight']
    df = pd.DataFrame(elements, columns=columns)
    df.to_csv(Path(getCsvLocation()), index=False)

jf = open(getJsonLocation(), "r")
js = jf.read().replace("INF", "0")

df = pd.read_json(js)

if list(df.index.values).count("AssayResults") == 1:
    experiments = getExperiments(df)

    writeExperimentsToCsvFile(experiments)
else:
    print("\n__________________________________________________\n")
    print("The json \"" + getJsonLocation() + "\" did not follow the proper structure.")
    print("\n__________________________________________________\n")
