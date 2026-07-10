import os #needed to get file path
import sys #needed to quit upon error
from trials import * #needed to run trials

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
    scriptDir = os.path.dirname(os.path.abspath(__file__)) #path of the code file
    slopesFilePath = os.path.join(scriptDir, "slopes.txt") #path of the file to store all slope information
    yintsFilePath = os.path.join(scriptDir, "yints.txt") #path of the file to store all yint infornation
    resultsFilePath = os.path.join(scriptDir, "results.txt") #path of the file to store all results infornation
        
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
    gridWidth = 3 #num columns in grid
    gridHeight = 3 #num columns in grid
    randStartLoc = False
    randStartDir = False
    startingLocX = 3 #optional
    startingLocY = 3 #optional
    startingDir = 1 #optional
    barLocX = 3 #optional
    barLocY = 1 #optional
    dirBar = 2 #optional
    innerWalls = [
        (2, 3, 2), (3, 3, 4) ,
        (2, 2, 2), (3, 2, 4) ,
        (2, 2, 3), (2, 1, 1)
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

