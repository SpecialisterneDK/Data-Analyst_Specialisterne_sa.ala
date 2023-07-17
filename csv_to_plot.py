import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
from pathlib import Path

plt.style.use('_mpl-gallery')

def getCsvLocation():
    return sys.argv[1]
    
def getPlotLocation():
    return sys.argv[2]
   
def getDataFrame(path):
    return pd.read_csv(path)

def makePlot(df):
    for i in range(len(df.index)):
        a = df.a[i]
        b = df.b[i]
        c = df.c[i]
        d = df.d[i]
        
        print(str(a))
        print(str(b))
        print(str(c))
        print(str(d))
        
        x = np.linspace(c-c*2, c*2, 1000)
        y = d + ((a-d) / (1+((x/c)**b)))
        
        fig, ax = plt.subplots()

        ax.plot(x, y, linewidth=2.0)

        savePlot(i)

def showPlot():
    plt.show()
    
def savePlot(i):
    plt.savefig(getPlotLocation()+"-"+str(i))

df = getDataFrame(getCsvLocation())
makePlot(df)