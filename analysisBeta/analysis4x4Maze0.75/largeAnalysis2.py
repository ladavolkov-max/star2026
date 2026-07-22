import os #needed to get file path
import sys #needed to quit upon error
from trials2 import * #needed to run trials

#-----------------------------------------------------------------------------------------------------------------
#main method runs group of trial batches, calculates, lsrl info for each one, and stores it in a file
#must have slopes.txt file and yints.txt file in the SAME DIRECTORY as the script file
if __name__ == "__main__":
    #get the path of where the files should be
    #runs if the text files are in the SAME DIRECTORY as the code
    scriptDir = os.path.dirname(os.path.abspath(__file__)) #path of the code file

    #creating the scenario that we want to run
    numTrialsInBatch = 150
    maxStepsPerTrial = 200
    gridWidth = 4 #num columns in grid
    gridHeight = 4 #num columns in grid
    randStartLoc = False
    randStartDir = False
    startingLocX = 1 #optional
    startingLocY = 4 #optional
    startingDir = 2 #optional
    barLocX = 4 #optional
    barLocY = 1 #optional
    dirBar = 2 #optional
    innerWalls = [
        (1, 4, 3), (1, 3, 1), #1
        (2, 4, 3), (2, 3, 1), #2
        (2, 3, 2), (3, 3, 4), #3
        (4, 3, 3), (4, 2, 1), #4
        (1, 2, 2), (1, 3, 4) #5
        ] #optional

    #main loop of running batches and storing info
    numBatchesToRun = 2

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

