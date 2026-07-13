import os #needed to get file path
import sys #needed to quit upon error
from trials import * #needed to run trials
from pathlib import Path #needed to get path info

#-----------------------------------------------------------------------------------------------------------------
#calculates the slope and y int of the lsrl for a set of points
#using ONE INDEXING for both trial and step number
#to change to 1 indexing --> all x and y values are +1
def calcLineInfo(points):
    #m = (N Σ(xy) - Σx Σy) / (N Σ(x^2) - (Σx)^2)
    sumX = 0
    sumY = 0
    sumXY = 0
    sumXsq = 0
    n = len(points)
    m = None
    b = None
    for i in range(0, n): #go through every entry in points array
        sumX += i + 1
        sumY += points[i]
        sumXY += (i + 1) * (points[i])
        sumXsq += (i + 1) * (i + 1)
    #slope
    m = (n * sumXY - sumX * sumY) / (n * sumXsq - sumX * sumX)
    #y int
    b = (sumY - m * sumX) / n
    #retun them as a list
    return [m, b]


#-----------------------------------------------------------------------------------------------------------------
#main method runs group of trial batches, calculates, lsrl info for each one, and stores it in a file
#must have slopes.txt file and yints.txt file in the SAME DIRECTORY as the script file
if __name__ == "__main__":
    #get the path of where the files should be
    #runs if the text files are in the SAME DIRECTORY as the code
    scriptDir = Path(__file__).resolve().parent #path of the code file
    slopesFilePath = scriptDir / "slopes.txt"  #path of the file to store all slope information
    yintsFilePath = scriptDir / "yints.txt" #path of the file to store all yint infornation
        
    #try to open the necessary files
    #openning with append mode so that we can add text to them
    try:
        slopesFile = open(slopesFilePath, "a")
    except FileNotFoundError:
        print(f"Error: could not find slopes file at {slopesFilePath}")
        print("Make sure it's in the same directory as the script file")
        sys.exit()
    try:
        yintsFile = open(yintsFilePath, "a")
    except FileNotFoundError:
        print(f"Error: could not find yints file at {yintsFilePath}")
        print("Make sure it's in the same directory as the script file")
        slopesFile.close()
        sys.exit()

    #creating the scenario that we want to run
    numTrialsInBatch = 300
    maxStepsPerTrial = 100
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
        (1, 4, 2), (2, 4, 4), #1
        (1, 3, 2), (2, 3, 4), #2
        (1, 4, 3), (1, 3, 1), #3
        (1, 2, 3), (1, 1, 1), #4
        (2, 2, 3), (2, 1, 1), #5
        (2, 2, 2), (3, 2, 4), #6
        (2, 5, 2), (3, 5, 4), #7
        (2, 4, 2), (3, 4, 4), #8 
        (3, 5, 3), (3, 4, 1), #9

        (4, 4, 3), (4, 3, 1), #10
        (4, 3, 2), (5, 3, 4), #11
        (4, 3, 3), (4, 2, 1), #12
        (4, 2, 2), (5, 2, 4), #13
        (4, 2, 3), (4, 1, 1), #14
        (3, 1, 2), (4, 1, 4), #15
        (5, 5, 3), (5, 4, 1) #16
        ] #optional

    #main loop of running batches and storing info
    numBatchesToRun = 50

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
        print(f"BATCH {i + 1}----------------")
        #running the actual trials
        results = tb.runBatch()
        lsrl = calcLineInfo(results)
        slopesFile.write(f"{lsrl[0]}\n")
        slopesFile.flush()
        yintsFile.write(f"{lsrl[1]}\n")
        yintsFile.flush()


    slopesFile.close()
    yintsFile.close()

