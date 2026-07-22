#this file creates a ca scenario and runs trials on it
import random #for random number generation
import os #needed to get file path
import platform #needed to check if windows
from subprocess import Popen, PIPE #for running the ca process

class TrialBatch:

    #-----------------------------------------------------------------------------------------------------------------
    #constructor takes in into for the details of the maze and the experiment
    def __init__(self, numTrials):
        self.__numTrials = numTrials
        #no max steps bc every trial only consists of one step
        #instance variables for the CA setup
        #runs if the ca and config files are in the SAME DIRECTORY as the code
        self.__scriptDir = os.path.dirname(os.path.abspath(__file__)) #path of the code file
        if platform.system() == "Windows":
            self.__caPath = os.path.join(self.__scriptDir, "caNew.exe") #path of the CA executable
        else:
            self.__caPath = os.path.join(self.__scriptDir, "caNew") #path of the CA executable
        self.__cfgPath = os.path.join(self.__scriptDir, "simplePunishment.cfg") #path of the configuration file
        self.__pid = Popen([self.__caPath, self.__cfgPath], stdin=PIPE, stdout=PIPE, bufsize=0) #starting up the ca process

    #-----------------------------------------------------------------------------------------------------------------
    #method to run a batch of trials according to the number of trials and max steps
    #returns the results of each trial
    def runBatch(self):
        #---------------------------------------main loop
        for trial in range(self.__numTrials): 
            print(f"trial {trial + 1}")
            #for the input always send it into the deciding state to see its decision
            try:
                self.__pid.stdin.write('1/1\n'.encode('utf-8'))
                #print("sent to decision state")
            except BrokenPipeError:
                print("broken pipe error, ca exited early")
                raise
            responseFullLine = self.__pid.stdout.readline()
            response = responseFullLine[0:1]
            print(f"Chose option {str(response)}")
            if response == b'0': #do nothing
                pass
            elif response == b'1': #chose the bad option
                #send punishment signal
                self.__pid.stdin.write(b"3/0.5\n")
                self.__pid.stdout.readline()
            elif response == b'2': #chose the good option
                #send reward signal
                self.__pid.stdin.write(b"2/1\n")
                self.__pid.stdout.readline()
            else:
                print("Error: Invalid response from CA: " + str(response))
            #reset ca
            self.__pid.stdin.write(b"0/1\n")
            self.__pid.stdout.readline()
        #---------------------------------------main loop