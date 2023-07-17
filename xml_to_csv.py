import pandas as pd
import requests
import sys
import json
from pathlib import Path
from xml.sax import ContentHandler, parse

# Reference https://goo.gl/KaOBG3
class ExcelHandler(ContentHandler):
    def __init__(self):
        self.chars = [  ]
        self.cells = [  ]
        self.rows = [  ]
        self.tables = [  ]
    def characters(self, content):
        content = content.strip()
        self.chars.append(content)
    def startElement(self, name, atts):
        if name=="Cell":
            self.chars = [  ]
        elif name=="Row":
            self.cells=[  ]
        elif name=="Table":
            self.rows = [  ]
    def endElement(self, name):
        if name=="Cell":
            self.cells.append(''.join(self.chars))
        elif name=="Row":
            self.rows.append(self.cells)
        elif name=="Table":
            self.tables.append(self.rows)


pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)

def getXmlLocation():
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
    
def createExperiment(df, group, indiv):
    ex = Experiment()
    ex.template_key = getTemplateKey(df)
    ex.date = getDate(df)
    (ex.a, ex.b, ex.c, ex.d, ex.p) = getABCDP(df, group, indiv)
    ex.weight = getWeight(df, group, indiv)
    return ex

def getTemplateKey(df):
    return df["Meta[1]/Template[1]/Key[1]"][0]
 
def getDate(df):
    return df["Meta[1]/Creation[1]/Time[1]"][0]

def getWeight(df, group, indiv):
    return df["AssayResults["+str(group)+"]/AssayResult["+str(indiv)+"]/StatisticTestResults[1]/StatisticTestResult[3]/Value[1]"][0]
    
def getABCDP(df, group, indiv):
    a = 0
    b = 0
    c = 0
    d = 0
    p = ""
    
    i = 1
    end = False
    while not end:
        base = "AssayResults["+str(group)+"]/AssayResult["+str(indiv)+"]/FullModel[1]/FitResult[1]/ParameterEstimate["+str(i)+"]"
        try:
            p = df[base+"/AssayElementName[1]"][0]
            if "Position" in p:
                pn = df[base+"/ParameterName[1]"][0]
                pv = df[base+"/Value[1]"][0]
                if pn == "A":
                    a = pv
                if pn == "B":
                    b = pv
                if pn == "C":
                    c = pv
                if pn == "D":
                    d = pv
        except:
            end = True
        i = i+1
    
    p = p[9:]
    return (a, b, c, d, p)

def getExperiments(df):
    exs = []
    
    i = 1
    endOuter = False
    while not endOuter:
        j = 1
        endInner = False
        while not endInner:
            try:
                exs.append(createExperiment(df, i, j))
            except:
                print("Got nothing from \"AssayResults["+str(i)+"]/AssayResult["+str(j)+"]\"")
                if j == 1:
                    endOuter = True
                endInner = True
            j = j+1
        i = i+1
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
    #print("Writing the following DataFrame to CSV:")
    #print(df)
    df.to_csv(Path(getCsvLocation()), index=False)

excelHandler = ExcelHandler()
parse(getXmlLocation(), excelHandler)

df = pd.DataFrame(excelHandler.tables[0][4:], columns=excelHandler.tables[0][3])
print(df.keys())
df.set_index("Meta[1]/Type[1]/CanonicalName[1]", inplace=True)
df = df.transpose()

#for col in df.keys():
    #print(col)
exs = getExperiments(df)

writeExperimentsToCsvFile(exs)