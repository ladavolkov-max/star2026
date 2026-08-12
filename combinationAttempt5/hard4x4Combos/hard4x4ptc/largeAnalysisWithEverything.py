import os #needed to get file path
import sys #needed to quit upon error
from trialsWithEverything import * #needed to run trials

#-----------------------------------------------------------------------------------------------------------------
#main method runs group of trial batches, calculates, lsrl info for each one, and stores it in a file
#must have slopes.txt file and yints.txt file in the SAME DIRECTORY as the script file
if __name__ == "__main__":
    scriptDir = os.path.dirname(os.path.abspath(__file__)) #path of the code file
    resultsFilePath = os.path.join(scriptDir, "results.txt") #path of the file to store all results infornation

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
        (2, 1, 2), (3, 1, 4) #4
        (4, 3, 3), (4, 2, 1) #5
        ] #optional

    #creating directories for data
    dataDir = os.path.join(scriptDir, "data")
    visionPretrainingDir = os.path.join(dataDir, "visionPretraining")
    spatialPretrainingDir = os.path.join(dataDir, "spatialPretraining")
    combinationResultsDir = os.path.join(dataDir, "combinationResults")
    os.makedirs(dataDir, exist_ok=True)
    os.makedirs(visionPretrainingDir, exist_ok=True)
    os.makedirs(spatialPretrainingDir, exist_ok=True)
    os.makedirs(combinationResultsDir, exist_ok=True)

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
        visionPreTrainingResults, spatialPretrainingResults, results = tb.runBatch()

        #creating the file for each of the results
        visionPretrainingFilePath = os.path.join(visionPretrainingDir, f"visionPretrainingResults{i + 6}.txt")
        spatialPretrainingFilePath = os.path.join(spatialPretrainingDir, f"spatialPretrainingResults{i + 6}.txt")
        combinationResultsFilePath = os.path.join(combinationResultsDir, f"batch{i + 6}.txt")

        #putting the data into the files
        with open(visionPretrainingFilePath, "w") as batchFile:
            for ii in range(len(visionPreTrainingResults)):
                batchFile.write(f"{visionPreTrainingResults[ii]}\n")

        with open(spatialPretrainingFilePath, "w") as batchFile:
            for ii in range(len(spatialPretrainingResults)):
                batchFile.write(f"{spatialPretrainingResults[ii]}\n")

        with open(combinationResultsFilePath, "w") as batchFile:
            for ii in range(len(results)):
                batchFile.write(f"{results[ii]}\n")

