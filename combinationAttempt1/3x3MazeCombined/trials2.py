#this file creates a ca scenario and runs trials on it
import random #for random number generation
import os #needed to get file path
import platform #needed to check if windows
from subprocess import Popen, PIPE #for running the ca process

class TrialBatch:

    #-----------------------------------------------------------------------------------------------------------------
    #prints all the inputs needed for the constructor
    @staticmethod
    def printConstructorParamsInfo():
        #iiiiiiiiiiiii
        print("1) Number of trials to run in the batch")
        #iiiiiiiiiiiii
        print("2) Max steps per trial")
        print("3) Grid width (number of columns)")
        print("4) Grid height (number of rows)")

        print("5) Randomize starting location (True/False)")
        print("6) Randomize starting direction (True/False)")
        #iiiiiiiiiiiii
        print("7) Starting location X (col) (optional, 1-indexed, default is 1 for top left corner)")
        #iiiiiiiiiiiii
        print("8) Starting location Y (row) (optional, 1-indexed, default is Grid Height for top left corner)")
        print("9) Starting Direction (optional, default is 2) (N=1, E=2, S=3, W=4)")
        #iiiiiiiiiiiii
        print("10) Bar location X (col) (optional, 1-indexed, default is Grid Width for bottom right corner)")
        #iiiiiiiiiiiii
        print("11) Bar location Y (row) (optional, 1-indexed, default is 1 for bottom right corner)")
        print("12) Bar direction (optional, default is 2) (N=1, E=2, S=3, W=4)")
        #iiiiiiiiiiiii
        print("13) Inner walls (optional, default is none) (list of lists w/ 1-indexed (x, y, dir))")

    #-----------------------------------------------------------------------------------------------------------------
    #constructor takes in into for the details of the maze and the experiment
    #iiiiiiiiiiiii(starting loc x, starting loc y, bar x, bar y)
    def __init__(self,
                 numTrials, maxSteps,
                 gridWidth, gridHeight,
                 randomizeLoc, randomizeDir, 
                 startingLocX=1, startingLocY=None, startingDir=2, 
                 locBarX=None, locBarY=1, dirBar=2, innerWalls=[]):
        #establishes all of our instance variables
        self.__numTrials = numTrials
        self.__numSteps = maxSteps
        self.__gridWidth = gridWidth
        self.__gridHeight = gridHeight
        self.__randomizeLoc = randomizeLoc
        self.__randomizeDir = randomizeDir
        self.__startLocX = startingLocX
        self.__startLocY = startingLocY
        self.__locX = self.__startLocX
        self.__locY = self.__startLocY

        if startingLocY is None:
            self.__locY = gridHeight
        else:
            self.__locY = startingLocY
        
        self.__startDir = startingDir
        self.__dir = self.__startDir

        if locBarX is None:
            self.__locBarX = gridWidth
        else:
            self.__locBarX = locBarX
        
        self.__locBarY = locBarY
        self.__dirBar = dirBar
        self.__innerWalls = innerWalls
        self.__walls = self.establishWalls()
        self.__see = "" #variable for debugging

        #instance variables for the CA setup
        #runs if the ca and config files are in the SAME DIRECTORY as the code
        self.__scriptDir = os.path.dirname(os.path.abspath(__file__)) #path of the code file
        if platform.system() == "Windows":
            self.__caPath = os.path.join(self.__scriptDir, "caNew.exe") #path of the CA executable
        else:
            self.__caPath = os.path.join(self.__scriptDir, "caNew") #path of the CA executable
    
        #starting up the different CAs
        self.__cfgPathVision = os.path.join(self.__scriptDir, "skinnerVisionMaze.cfg") #path of the configuration file
        self.__pidVision = Popen([self.__caPath, self.__cfgPathVision], stdin=PIPE, stdout=PIPE, bufsize=0) #starting up the ca process
        self.__cfgPathSpatial = os.path.join(self.__scriptDir, "skinnerSpatial.cfg") #path of the configuration file
        self.__pidSpatial = Popen([self.__caPath, self.__cfgPathSpatial], stdin=PIPE, stdout=PIPE, bufsize=0) #starting up the ca process
        self.__cfgPathDecision = os.path.join(self.__scriptDir, "skinnerDecision.cfg") #path of the configuration file
        self.__pidDecision = Popen([self.__caPath, self.__cfgPathDecision], stdin=PIPE, stdout=PIPE, bufsize=0) #starting up the ca process

    #-----------------------------------------------------------------------------------------------------------------
    #method to run a batch of trials according to the number of trials and max steps
    #returns the results of each trial
    def runBatch(self):
        results = []
        #---------------------------------------outer loop
        for trial in range(self.__numTrials): 
            print(f"trial {trial + 1}")
            #random location and dir setup
            #resetting ca to start the new trial
            if self.__randomizeLoc:
                self.generateRandLoc()
            else:
                self.__locX = self.__startLocX
                self.__locY = self.__startLocY
            if self.__randomizeDir:
                self.generateRandDir()
            else:
                self.__dir = self.__startDir
            #tracking if a successful press has been made
            successfulPress = False
            #tracking the number of steps taken in the trial
            stepsTaken = 0
            #print for debugging
            #print(f"starting trial {trial}*********")
            #---------------------------------------inner loop
            for step in range(self.__numSteps): 
                #getting information for the 2 sensor CAs
                visionScenario = self.getVisionScenario()
                spatialScenario = self.getSpatialScenario()
                #writing input to the 2 sensor CAs
                #self.__pid.stdin.write((str(visionScenario) + '/1\n').encode('utf-8'))
                try:
                    self.__pidVision.stdin.write((str(visionScenario) + '/1\n').encode('utf-8'))
                except BrokenPipeError:
                    print("broken pipe error, vision ca exited early")
                    raise
                try:
                    self.__pidSpatial.stdin.write((str(spatialScenario) + '/1\n').encode('utf-8'))
                except BrokenPipeError:
                    print("broken pipe error, spatial ca exited early")
                    raise
                #getting the responses and confidences from both senson CAs
                responseVisionFullLine = self.__pidVision.stdout.readline()
                responseVision = responseVisionFullLine[0:1]
                confidenceVision = float(responseVisionFullLine.split()[1])
                responseSpatialFullLine = self.__pidSpatial.stdout.readline()
                responseSpatial = responseSpatialFullLine[0:1]
                confidenceSpatial = float(responseSpatialFullLine.split()[1])

                #sending input and getting output to the decision CA
                #vision inputs are 1-5, spatial inputs are 6-10
                # Convert decoded strings to integers first, then add the offsets
                inputVision = int(responseVision.decode()) + 1
                inputSpatial = int(responseSpatial.decode()) + 6
                inputString = f"{inputVision}/{confidenceVision} {inputSpatial}/{confidenceSpatial}\n"
                try:
                    self.__pidDecision.stdin.write((inputString).encode('utf-8'))
                except BrokenPipeError:
                    print("broken pipe error, decision ca exited early")
                    raise
                responseFullLine = self.__pidDecision.stdout.readline()
                response = responseFullLine[0:1]
                
                #print statements for debugging
                """
                print(f"taking step {step}--------")
                print(f"currently at: {self.__locX}, {self.__locY}, facing {self.__dir}")
                print(f"vision says do: {responseVision} with strength {confidenceVision}")
                print(f"spatial says do: {responseSpatial} with strength {confidenceSpatial}")
                print(f"decision: {response}")
                """
                #next step, keeping track for trial results
                #iiiiiiiiiiiii (do it before so that 1 indexing applies to both the min and max trials)
                stepsTaken += 1
                if response == b'0': #do nothing
                    pass
                elif response == b'1': #turn left
                    self.__dir -= 1
                    #wrap around if necessary
                    if self.__dir == 0:
                        self.__dir = 4
                elif response == b'2': #turn right
                    self.__dir += 1
                    #wrap around if necessary
                    if self.__dir == 5:
                        self.__dir = 1
                elif response == b'3': #move forward
                    canMove = self.canMoveForward()
                    if canMove:
                        self.move()
                elif response == b'4': #press bar
                    if (self.__locX == self.__locBarX and
                        self.__locY == self.__locBarY and
                        self.__dir == self.__dirBar):
                        successfulPress = True
                        #print("reward achieved!!!!")
                        # lever pressed, send reward signal
                        #send reward to all 3
                        self.__pidVision.stdin.write(b"21/1\n")
                        self.__pidVision.stdout.readline()
                        self.__pidSpatial.stdin.write(b"17/1\n")
                        self.__pidSpatial.stdout.readline()
                        self.__pidDecision.stdin.write(b"11/1\n")
                        self.__pidDecision.stdout.readline()
                        break #breaks out of the step loop, goes to next trial
                else:
                    print("Error: Invalid response from CA: " + str(response))
                
            #---------------------------------------inner loop
            #print statement for debugging
            print("Trial: " + str(trial) + ", Steps Taken: " + str(stepsTaken) + ", Successful Press: " + str(successfulPress))
            #add to results list
            #iiiiiiiiiiiii
            results.append(stepsTaken)
            #reset ca (all 3)
            self.__pidVision.stdin.write(b"0/1\n")
            self.__pidVision.stdout.readline()
            self.__pidSpatial.stdin.write(b"0/1\n")
            self.__pidSpatial.stdout.readline()
            self.__pidDecision.stdin.write(b"0/1\n")
            self.__pidDecision.stdout.readline()
        #---------------------------------------outer loop
        #stop the ca and give the results
        return results

    #-----------------------------------------------------------------------------------------------------------------
    #lookup table mapping a 6-bit mask of
    #(wallFront, wallLeft, wallRight, barFront, barLeft, barRight)
    #-> bit weights: 
    #   wallFront=1, 
    #   wallLeft=2, 
    #   wallRight=4,
    #   barFront=8, 
    #   barLeft=16, 
    #   barRight=32.
    # ex: wallFront=True, wallLeft=True, everything else False (your "corner front left" case):
            #key = 1 + 2*1 + 4*0 + 8*0 + 16*0 + 32*0 = 3
    visionKeys = {
        0: 1,    # 0  = none set                                          -> none
        1: 2,    # 1  = wallFront                                         -> wall in front
        2: 3,    # 2  = wallLeft                                          -> wall left
        4: 4,    # 4  = wallRight                                         -> wall right
        3: 5,    # 3  = wallFront + wallLeft            (1+2)             -> corner front left
        5: 6,    # 5  = wallFront + wallRight           (1+4)             -> corner front right
        6: 7,    # 6  = wallLeft + wallRight            (2+4)             -> hallway
        7: 8,    # 7  = wallFront + wallLeft + wallRight (1+2+4)          -> dead end
        9: 9,    # 9  = wallFront + barFront            (1+8)             -> bar front
        11: 10,  # 11 = wallFront + wallLeft + barFront (1+2+8)           -> bar front + wall left
        13: 11,  # 13 = wallFront + wallRight + barFront (1+4+8)          -> bar front + wall right
        15: 12,  # 15 = wallFront + wallLeft + wallRight + barFront (1+2+4+8) -> bar front + wall both
        18: 13,  # 18 = wallLeft + barLeft              (2+16)            -> bar left
        19: 14,  # 19 = wallFront + wallLeft + barLeft  (1+2+16)          -> bar left + wall front
        22: 15,  # 22 = wallLeft + wallRight + barLeft  (2+4+16)          -> bar left + wall right
        23: 16,  # 23 = wallFront + wallLeft + wallRight + barLeft (1+2+4+16) -> bar left + wall front + wall right
        36: 17,  # 36 = wallRight + barRight            (4+32)            -> bar right
        38: 18,  # 38 = wallLeft + wallRight + barRight (2+4+32)          -> bar right + wall left
        37: 19,  # 37 = wallFront + wallRight + barRight (1+4+32)         -> bar right + wall front
        39: 20,  # 39 = wallFront + wallLeft + wallRight + barRight (1+2+4+32) -> bar right + wall front + wall left
}

    #-----------------------------------------------------------------------------------------------------------------
    #method to get the vision scenario code for the agent's current position/direction
    def getVisionScenario(self):
        dirFront = self.__dir
        dirLeft = self.__dir - 1
        #wrap aound if necessary
        if dirLeft == 0:
            dirLeft = 4
        dirRight = self.__dir + 1
        #wrap aound if necessary
        if dirRight == 5:
            dirRight = 1

        walls = self.__walls
        x, y = self.__locX, self.__locY
        wallFront = walls[(x, y, dirFront)]
        wallLeft = walls[(x, y, dirLeft)]
        wallRight = walls[(x, y, dirRight)]

        onBar = (x == self.__locBarX and y == self.__locBarY)
        barFront = onBar and dirFront == self.__dirBar
        barLeft = onBar and dirLeft == self.__dirBar
        barRight = onBar and dirRight == self.__dirBar

        #pack the six booleans into a single integer key (True/False act as 1/0)
        key = (wallFront + wallLeft * 2 + wallRight * 4
               + barFront * 8 + barLeft * 16 + barRight * 32)

        code = self.visionKeys.get(key, -1)
        if code == -1:
            print(f"unexpected vision response at: {x}, {y}, {self.__dir}")
        return code
    
    #-----------------------------------------------------------------------------------------------------------------
    #method to get the spatial scenario code for the agent's current position/direction
    def getSpatialScenario(self):
        wordsToNum = {
            "region1dir1" : 1,
            "region1dir2" : 2,
            "region1dir3" : 3,
            "region1dir4" : 4,
            "region2dir1" : 5,
            "region2dir2" : 6,
            "region2dir3" : 7,
            "region2dir4" : 8,
            "region3dir1" : 9,
            "region3dir2" : 10,
            "region3dir3" : 11,
            "region3dir4" : 12,
            "region4dir1" : 13,
            "region4dir2" : 14,
            "region4dir3" : 15,
            "region4dir4" : 16
        }
        regionNum = 0
        if(1 <= self.__locX <= 2 and 2 <= self.__locY <= 3):
            regionNum = 1
        elif(self.__locX == 3 and 2 <= self.__locY <= 3):
            regionNum = 2
        elif(self.__locX == 1 and self.__locY == 1):
            regionNum = 3
        elif(self.__locX == 3 and self.__locY == 1):
            regionNum = 4
        else:
            print(f"unexpected region at: {self.__locX}, {self.__locY}, {self.__dir}")
            return -1
        scenarioString = f"region{regionNum}dir{self.__dir}"
        return wordsToNum[scenarioString]



    #-----------------------------------------------------------------------------------------------------------------
    #method to get the dictionary of which edges are walls and which are not
    def establishWalls(self):
        #creates a dictionary for all wall information
        #(x, y, dir) : wall?T/F
        walls = {}

        #initially all walls are set as False
        #iiiiiiiiiiiii
        for x in range(1, self.__gridWidth + 1):
            for y in range(1, self.__gridHeight + 1):
                for dir in range(1, 5):
                    walls[(x, y, dir)] = False

        #creates all outer walls with loops
        #leftmost wall
        #iiiiiiiiiiiii
        for y in range(1, self.__gridHeight + 1):
            walls[(1, y, 4)] = True
        #rightmost wall
        #iiiiiiiiiiiii
        for y in range(1, self.__gridHeight + 1):
            walls[(self.__gridWidth, y, 2)] = True
        #top wall
        #iiiiiiiiiiiii
        for x in range(1, self.__gridWidth + 1):
            walls[(x, self.__gridHeight, 1)] = True
        #bottom wall
        #iiiiiiiiiiiii
        for x in range(1, self.__gridWidth + 1):
            walls[(x, 1, 3)] = True

        #creates all inner walls based on the instance varuable
        for innerWall in self.__innerWalls:
            walls[(innerWall[0], innerWall[1], innerWall[2])] = True

        return walls

    #-----------------------------------------------------------------------------------------------------------------
    #method to randomize starting location
    def generateRandLoc(self):
        #iiiiiiiiiiiii
        self.__locX = random.randint(1, self.__gridHeight)
        #iiiiiiiiiiiii
        self.__locY = random.randint(1, self.__gridWidth)

    #-----------------------------------------------------------------------------------------------------------------
    #method to randomize starting location
    def generateRandDir(self):
            self.__dir = random.randint(1, 4)

    #-----------------------------------------------------------------------------------------------------------------
    #method to determine if it can move forward or not based on the wall in front of it
    def canMoveForward(self):
        #checks if the wall in front of the agent is a wall or not
        if self.__walls[(self.__locX, self.__locY, self.__dir)]:
            return False
        else:
            return True

    #-----------------------------------------------------------------------------------------------------------------
    #method for applying the movement
    def move(self):
        #moves the agent forward based on its current direction
        if self.__dir == 1: #N
            self.__locY += 1 #move up = increase y
        elif self.__dir == 2: #E
            self.__locX += 1 #move right = increase x
        elif self.__dir == 3: #S
            self.__locY -= 1 #move down = decrease y
        elif self.__dir == 4: #W
            self.__locX -= 1 #move left = decrease x