import os #needed to get file path
import sys #needed to quit upon error
from trials2 import * #needed to run trials

#-----------------------------------------------------------------------------------------------------------------
#main method runs group of trial batches, calculates, lsrl info for each one, and stores it in a file
#must have slopes.txt file and yints.txt file in the SAME DIRECTORY as the script file
if __name__ == "__main__":
    scriptDir = os.path.dirname(os.path.abspath(__file__)) #path of the code file
    resultsFilePath = os.path.join(scriptDir, "results.txt") #path of the file to store all results infornation

    #creating the scenario that we want to run
    numTrialsInBatch = 150
    maxStepsPerTrial = 250
    gridWidth = 5 #num columns in grid
    gridHeight = 5 #num columns in grid
    randStartLoc = False
    randStartDir = False
    startingLocX = 1 #optional
    startingLocY = 5 #optional
    startingDir = 2 #optional
    barLocX = 5 #optional
    barLocY = 1 #optional
    dirBar = 2 #optional
    innerWalls = [
        (2, 5, 2), (3, 5, 4), #1
        (2, 4, 2), (3, 4, 4), #2
        (4, 5, 3), (4, 4, 1), #3
        (5, 5, 3), (5, 4, 1), #4
        (2, 1, 2), (3, 1, 4), #5
        (3, 2, 3), (3, 1, 1), #6
        (3, 1, 2), (4, 1, 4) #7
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
        results = tb.runBatch()
        #create a brand new file for this batch (e.g. "batch 1.txt") and write the
        #number of steps taken in each trial
        batchFilePath = os.path.join(scriptDir, f"batch{i}.txt")
        with open(batchFilePath, "w") as batchFile:
            for stepsTaken in results:
                batchFile.write(f"{stepsTaken}\n")
