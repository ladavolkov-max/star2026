import os #needed to get file path
import sys #needed to quit upon error
from trials2 import * #needed to run trials
from pathlib import Path #needed to create directories

#-----------------------------------------------------------------------------------------------------------------
#main method runs group of trial batches, calculates, lsrl info for each one, and stores it in a file
#must have slopes.txt file and yints.txt file in the SAME DIRECTORY as the script file
if __name__ == "__main__":
    scriptDir = os.path.dirname(os.path.abspath(__file__)) #path of the code file

    #creating the scenario that we want to run
    numTrialsInBatch = 100
    maxStepsPerTrial = 100
    gridWidth = 3 #num columns in grid
    gridHeight = 3 #num columns in grid
    randStartLoc = False
    randStartDir = False
    startingLocX = 1 #optional
    startingLocY = 3 #optional
    startingDir = 2 #optional
    barLocX = 3 #optional
    barLocY = 1 #optional
    dirBar = 2 #optional
    innerWalls = [
        (1, 3, 3), (1, 2, 1), #1
        (2, 3, 3), (2, 2, 1), #2
        (1, 1, 2), (2, 1, 4), #3
        (2, 2, 3), (2, 1, 1), #4
        (2, 1, 2), (3, 1, 4) #5
        ] #optional

    #main loop of running batches and storing info
    numBatchesToRun = 40

    for i in range(numBatchesToRun):
        #starting a new ca each time (explicit keyword arguments allow us to ignore order)
        tb = TrialBatch(
            numTrials=numTrialsInBatch,
            maxSteps=maxStepsPerTrial,
            gridWidth=gridWidth,
            gridHeight=gridHeight,
            randomizeLoc=randStartLoc,
            randomizeDir=randStartDir,
            startingLocX=startingLocX,
            startingLocY=startingLocY,
            startingDir=startingDir,
            locBarX=barLocX,
            locBarY=barLocY,
            dirBar=dirBar,
            innerWalls=innerWalls
        )
        print(f"BATCH {i}----------------")
        #running the actual trials
        results, nonPunishedActions, zeroActions = tb.runBatch()

        #creating directories for data
        dataDir = os.path.join(scriptDir, "data")
        batchDir = os.path.join(dataDir, "batches")
        nonPunishedProportionsDir = os.path.join(dataDir, "nonPunishedProportions")
        zeroProportionsDir = os.path.join(dataDir, "zeroProportions")
        os.makedirs(dataDir, exist_ok=True)
        os.makedirs(batchDir, exist_ok=True)
        os.makedirs(nonPunishedProportionsDir, exist_ok=True)
        os.makedirs(zeroProportionsDir, exist_ok=True)

        #create a brand new file for this batch (e.g. "batch 1.txt") and write the
        #number of steps taken in each trial
        batchFilePath = os.path.join(batchDir, f"batch{i}.txt")
        nonPunishedFilePath = os.path.join(nonPunishedProportionsDir, f"nonPunishedProportions{i+1}.txt")
        zeroFilePath = os.path.join(zeroProportionsDir, f"zeroProportions{i+1}.txt")

        with open(batchFilePath, "w") as batchFile:
            for ii in range(len(results)):
                batchFile.write(f"{nonPunishedActions[ii]} / {results[ii]}\n")

        with open(nonPunishedFilePath, "w") as nonPunishedFile:
            for ii in range(len(results)):
                nonPunishedFile.write(f"{nonPunishedActions[ii] / results[ii]}\n")

        with open(zeroFilePath, "w") as zeroFile:
            for ii in range(len(results)):
                zeroFile.write(f"{zeroActions[ii] / nonPunishedActions[ii]}\n")


