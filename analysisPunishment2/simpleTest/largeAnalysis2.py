import os #needed to get file path
import sys #needed to quit upon error
from trials2 import * #needed to run trials

#-----------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    scriptDir = os.path.dirname(os.path.abspath(__file__)) #path of the code file

    #main loop of running batches and storing info
    numBatchesToRun = 10
    numTrials = 50

    for i in range(numBatchesToRun):
        #starting a new ca each time (explicit keyword arguments allow us to ignore order)
        tb = TrialBatch(numTrials)
        print(f"BATCH {i}----------------")
        #running the actual trials
        choices = tb.runBatch()