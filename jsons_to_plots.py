import sys
from pathlib import Path
import os
import subprocess as sp

def getJsonLocations():
    return sys.argv[1]
    
def getPlotLocations():
    return sys.argv[2]

def getJsonsInDirectory(directory):
    jsons = []
    for dI in os.listdir(directory):
        combinedPath = os.path.join(directory, dI)
        if os.path.isdir(combinedPath):
            for json in getJsonsInDirectory(combinedPath):
                jsons.append(json)
        if combinedPath.endswith(".json"):
            jsons.append(combinedPath.replace(getJsonLocations(), ""))
    return jsons
    
def getXmlsInDirectory(directory):
    xmls = []
    for dI in os.listdir(directory):
        combinedPath = os.path.join(directory, dI)
        if os.path.isdir(combinedPath):
            for xml in getXmlsInDirectory(combinedPath):
                xmls.append(xml)
        if combinedPath.endswith(".xml"):
            xmls.append(combinedPath.replace(getJsonLocations(), ""))
    return xmls
    
def getCsvsInDirectory(directory):
    csvs = []
    for dI in os.listdir(directory):
        combinedPath = os.path.join(directory, dI)
        if os.path.isdir(combinedPath):
            for csv in getCsvsInDirectory(combinedPath):
                csvs.append(csv)
        if combinedPath.endswith(".csv"):
            csvs.append(combinedPath.replace(getPlotLocations(), ""))
    return csvs
    
def createCsvsFromJsons(jsons):
    for json in jsons:
        script = "\"G:\\Mit drev\\Projects\\Command Line\\Data Analyst\\workspace\\json_to_csv.py\""
        arg1 = "\"" + getJsonLocations()+json + "\""
        arg2 = "\"" + getPlotLocations()+json[0:len(json)-4] + "csv" + "\""
        
        if not Path(arg2[1:len(arg2)-1]).is_file():
            sp.call(script + " " + arg1 + " " + arg2, shell=True)
            
            if Path(arg2[1:len(arg2)-1]).is_file():
                print("Done with json \"" + json + "\"")
            else:
                print("Failed with json \"" + json + "\"")
        else:
            print("Skipping \"" + json + "\"")
            
def createCsvsFromXmls(xmls):
    for xml in xmls:
        script = "\"G:\\Mit drev\\Projects\\Command Line\\Data Analyst\\workspace\\xml_to_csv.py\""
        arg1 = "\"" + getJsonLocations()+xml + "\""
        arg2 = "\"" + getPlotLocations()+xml[0:len(xml)-3] + "csv" + "\""
        
        if not Path(arg2[1:len(arg2)-1]).is_file():
            sp.call(script + " " + arg1 + " " + arg2, shell=True)
            
            if Path(arg2[1:len(arg2)-1]).is_file():
                print("Done with xml \"" + xml + "\"")
            else:
                print("Failed with xml \"" + xml + "\"")
        else:
            print("Skipping \"" + xml + "\"")

def createPlotsFromCsvs(csvs):
    for csv in csvs:
        script = "\"G:\\Mit drev\\Projects\\Command Line\\Data Analyst\\workspace\\csv_to_plot.py\""
        arg1 = "\"" + getPlotLocations()+csv + "\""
        arg2 = "\"" + getPlotLocations()+csv[0:len(csv)-4] + "\""
        
        sp.call(script + " " + arg1 + " " + arg2, shell=True)
    
jsons = getJsonsInDirectory(getJsonLocations())
createCsvsFromJsons(jsons)

xmls = getXmlsInDirectory(getJsonLocations())
createCsvsFromXmls(xmls)

csvs = getCsvsInDirectory(getPlotLocations())
createPlotsFromCsvs(csvs)