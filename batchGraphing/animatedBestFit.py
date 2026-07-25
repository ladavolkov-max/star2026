import os #for pathnames
import time #for frame delay
import matplotlib.pyplot as plt #for graphing
import numpy as np #for b val summation

#turn on interactive mode
plt.ion()
fig, ax = plt.subplots() #separating the tuple to get the axes object

#putting all data files in a list
scenarioName = "beta 0.25"
dataFiles = []
dirPath = "/Users/ladavolkov/Desktop/analysisBeta/analysis4x4Maze0.25"
lastBatchNum = 39
for i in range(0, lastBatchNum + 1):
    fileName = f"batch{i}.txt"
    filePath = os.path.join(dirPath, fileName)
    dataFiles.append(filePath)

#looping through all files in a list
for filePath in dataFiles:
    #if the file isn't found just skip it
    if not os.path.exists(filePath):
        continue
    #load data from current file
    yVals = []
    with open(filePath, "r") as file:
        yVals = [float(line.strip()) for line in file]
        xVals = list(range(1, len(yVals) + 1))
    #b val calculation
    a = 200
    x = np.array(xVals) #converting list to numpy array
    y = np.array(yVals) #converting list to numpy array
    numerator = np.sum(x * np.log(y / a))
    denominator = np.sum(x ** 2)
    b = - (numerator / denominator)
    #clear previous file's graph
    ax.clear()
    #generate the new graph
    ax.plot (xVals, yVals, linewidth=0.4)
    ax.set_title(f"{scenarioName}: Batches 0 - {lastBatchNum}")
    ax.set_ylim(0, 200)
    ax.set_xlim(0, 150)
    ax.set_xlabel("trial")
    ax.set_ylabel("steps")
    #generate the line of best fit
    xSmooth = np.linspace(1, 150, 200) #make 200 smooth points
    yFit = a * np.exp(-b * xSmooth)
    ax.plot(xSmooth, yFit, color = "red", linewidth = 1)
    #drawing the new graph
    plt.draw()
    plt.pause(0.1) #how many seconds per file

#leave the last frame open on screen when done
plt.ioff()
plt.show()
