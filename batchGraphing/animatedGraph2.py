import os #for pathnames
import time #for frame delay
import matplotlib.pyplot as plt #for graphing

#turn on interactive mode
plt.ion()
fig, ax = plt.subplots() #separating the tuple to get the axes object

#putting all data files in a list
scenarioName = ""
dataFiles = []
dirPath = "/Users/ladavolkov/Desktop/analysisPunishment4/3x3MazeVision/visionInversePun0.05/data/nonPunishedProportions"
lastBatchNum = 39
for i in range(0, lastBatchNum + 1):
    fileName = f"nonPunishedProportions{i}.txt"
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
    #clear previous file's graph
    ax.clear()
    #generate the new graph
    ax.plot (xVals, yVals, linewidth=0.4)
    ax.set_title(f"{scenarioName}: Batches 0 - {lastBatchNum}")
    ax.set_ylim(0, 1)
    ax.set_xlim(0, 100)
    ax.set_xlabel("trial")
    ax.set_ylabel("proportion of non punished actions")
    #drawing the new graph
    plt.draw()
    plt.pause(0.1) #how many seconds per file

#leave the last frame open on screen when done
plt.ioff()
plt.show()
