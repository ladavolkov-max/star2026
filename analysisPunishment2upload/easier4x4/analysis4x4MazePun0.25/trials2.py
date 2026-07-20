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
        self.__cfgPath = os.path.join(self.__scriptDir, "skinnerPunishment.cfg") #path of the configuration file
        self.__pid = Popen([self.__caPath, self.__cfgPath], stdin=PIPE, stdout=PIPE, bufsize=0) #starting up the ca process

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
                visionScenario = self.getVisionScenario()
                #self.__pid.stdin.write((str(visionScenario) + '/1\n').encode('utf-8'))
                try:
                    self.__pid.stdin.write((str(visionScenario) + '/1\n').encode('utf-8'))
                except BrokenPipeError:
                    print("broken pipe error, ca exited early")
                    #print("CA process exited early. Return code:", self.__pid.poll())
                    #print("stderr:", self.__pid.stderr.read().decode('utf-8', errors='replace'))
                    raise
                responseFullLine = self.__pid.stdout.readline()
                response = responseFullLine[0:1]
                #print statements for debugging
                """
                print(f"taking step {step}--------")
                print(f"currently at: {self.__locX}, {self.__locY}, facing {self.__dir}")
                print(f"see: {self.__see}")
                print(f"about to do: {response} ")
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
                    else:
                        #tried to go into a wall, send punishment signal
                        self.__pid.stdin.write(b"22/0.25\n")
                        self.__pid.stdout.readline()
                elif response == b'4': #press bar
                    if (self.__locX == self.__locBarX and
                        self.__locY == self.__locBarY and
                        self.__dir == self.__dirBar):
                        successfulPress = True
                        # lever pressed, send reward signal
                        self.__pid.stdin.write(b"21/1\n")
                        self.__pid.stdout.readline()
                        break #breaks out of the step loop, goes to next trial
                else:
                    print("Error: Invalid response from CA: " + str(response))
                
            #---------------------------------------inner loop
            #print statement for debugging
            print("Trial: " + str(trial) + ", Steps Taken: " + str(stepsTaken) + ", Successful Press: " + str(successfulPress))
            #add to results list
            #iiiiiiiiiiiii
            results.append(stepsTaken)
            #reset ca
            self.__pid.stdin.write(b"0/1\n")
            self.__pid.stdout.readline()
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