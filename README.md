# star2026
A folder to organize all of our files throughout the 2026 STAR program

1) reading: the pdf files given by the professor for information about the project.

1.1) dissertation: the full dissertation on the logic and implementation of the original CA

1.2) algo: explanation of the CA's mathematical algorithm

1.3) cause: instructions for setting up and running the CA

1.4) proto: a description of the blackboard structure and its implementation in a different context
  

2) initialCA: all of the initial files and scripts for the CA, copied over from the bls directory mentioned in the implementation directions pdf. They contain the configuration files for the CA, implementation of the CA in go, and the driver programs to run the CA in python 2. You can also get these files from tux yourself and copy them over into your directory straight in the terminal (see point A, B)


3) python3Translations: all of the driver programs from the initial CA files translated into python 3, along with all of the tools we needed for the translation. They can be run in your tux terminal. (see point B)


4) filesForDesktop: the files related to running the CA on your local computer. These include the CA itself, along with the different configurations that can be used to structure its behavior. These should be kept on your desktop because our current code that uses them tells the coputer to look for them specifically on the desktop.


5) javaInitialGraphics: code to get a basic feel of how the movement of the visual stimulation will work in java. This code can be run through bluej. (see point C) The descriptions are not for the specific files but for the classes that show up when you open the package.bluej file.

5.1) DrawingTester: creates an empty graphics window

5.2) MoveWithKeys: first version of a skinner visual where you can move the mouse around using the wasd or arrow keys

5.3) RotateAndMove: skinner visual where you can move the mouse with wasd or arrow keys and turn it left/right with the 1/2 keys

5.4) SkinnerWithGrid: skinner visual in 4x4 where the movements now follow the action outputs with 1/2 for turn and 3 for moving forward

5.5) CompleteSkinnerMovement: movement with the action output keys in the 1x2 layout


6) javaSkinnerWithGraphics: code to run visual simulations and observe results of skinner trials run with the CA. Make sure that the files from filesForDesktop folder are on your desktop, since the code uses them to run. This code can be run through bluej. (see point C) Note: these files open a CA with different configurations (see point D), so if you want to test it with a different one then you can change the file name that is specified when opening it up within the code at the top. The descriptions are not for the specific files but for the classes that show up when you open the package.bluej file.

6.1) OriginalAlgorithmTranslation: recreates the functionality of the original skinner algorithm to run on your own computer. Writes the same things to the output and error as the python 2 and python 3 versions of the skinner box outlined in the dissertation.

6.2) GraphicsWithKeys: contains the skinner box visuals that will be used for the visualizations of the skinner trials. The mouse is manually controlled by the keyboard with 1/2 for turn and 3 for move.

6.3) Batch3x3: runs the same algorithm as the original skinner box but with the new vision configuration for the mouse, the code to interpret stimuli and respond accordingly in a 3x3 grid envirionment. Writes the same information as the original to the output and the error.

6.4) OneTrial: runs the original skinner box experiment one trial at a time (instead of all 300 immediately one after another). Takes inputs of enter to run the trial and q to quit. On each trial, outputs how many steps it took to complete and whether the trial ended on a successful lever press or not.

6.5) OneTrialForGraphics: runs the same was as OneTrial but with additional mechanics (storing all of the responses and positions in an arraylist) to communicate with the graphics implementation.

6.6) GraphicsConnected: connects to OneTrialForGraphics to show how the mouse acts on a given trial of the original skinner box experiment. It is run by going to the graphics window and pressing enter. The actions are shown in 2 steps: one frame for the current position of the mouse with a text label of what action it's about to take (turnLR/move/press/nothing) and then the resulting position of that action. Continues until the trial is over. Starting another trial resets the graphics to start showing the visuals for the new trial.

6.7) OneTrial3x3: runs the one trial mechanic (with on graphics) in a 3x3 environment using the vision configuration. (see point D)

6.8) OneTrial4x4: runs the one trial mechanic (with on graphics) in a 4x4 environment using the vision configuration. (see point D)

6.9) OneTrial3x3ForG: connects to GridGraphics to show how the mouse acts on a given 3x3 trial. Runs the same was as OneTrial3x3 but with additional mechanics (storing all of the responses and positions in an arraylist) to communicate with the graphics implementation.

6.10) GridGraphics: connects to OneTrialForGraphics3x3ForG to show how the mouse acts on a given trial on a 3x3 environment with the vision configuration (see point D). It is run by going to the graphics window and pressing enter. The actions are shown in 2 steps: one frame for the current position of the mouse with a text label of what action it's about to take (turnLR/move/press/nothing) and then the resulting position of that action. Continues until the trial is over. Starting another trial resets the graphics to start showing the visuals for the new trial.

6.11) BatchForGraphing: runs a batch of original skinner trials the same way that the original algorithm does, sending information necessary to graph the mouse's progress the same way that they were in the dissertation. Plots and connects how many steps it took to complete each trial in the batch and graphs a trend line for that batch based on the least squares regression formula. 

6.12) Batch3x3ForG: runs a batch of skinner trials in a 3x3 grid and the vision configuration (see point D), sending information necessary to graph the mouse's progress. 

6.13) Batch2x2ForG: runs a batch of skinner trials in a 2x2 grid and the vision configuration (see point D), sending information necessary to graph the mouse's progress. 

6.14) BatchGraph: runs whatever batch algorithm it is connected to it, taking the information it sends and graphing it. Plots and connects how many steps it took to complete each trial in the batch and graphs a trend line for that batch based on the least squares regression formula. 


7) blackboardCodeC: the bb.h and bb.c files are the original files provided for the blackboard described in the proto file in the reading folder. The rest of the files are an attempt to use the original blackboard structure, but are not fully fleshed out or functional.


8) blackboardRebuildPython: code that works on reimplementing the general structure of the blackboard described in the proto file in the reading folder for the context of the skinner blackboard. Each attempt

9) analysisBase: the basic structure that we use to run all of our mathematical data generation and analysis. It implements the algorithm to run the ca in a python class, which sets up a ca and its environment through instance variables (trials.py). It sets up a coordinate system (1-indexed) for the grid and establishes where the walls are using a dictionary of (wallX wallY wallDir) : wall?T/F It uses a new configuration that includes additional vision scenarios to consider (skinnerVisionMaze.cfg). It then runs several batches of trials and calculates the slope and y intercept for the line of best fit for each batch (largeAnalysis.py). It writes the results of each batch to specific files within the same directory to store the data (slopes.txt & yints.txt).

10) analysisFirst: the first version of a large scale analysis of running several batches of skinner trials and assessing the learning speed. Contains 4 situations: 3x3 grid, 3x3 maze, 5x5 grid, 5x5 maze. These scenarios all use a more robust configuration file for seeing different possible situations within a maze (see point D). For each one, runs the batches and records the slope and y int of the trend line for each into a separate folder. Note: the 5x5 maze has trials2.py and largeAnalysis2.py, which is a different more optimized implementation of running the trials and recording the results that is then used for later analysis algorithms.

10.1) analysis3x3Grid: sets up to run batches of trials in an empty 3x3 grid environment.

10.2) analysis3x3Maze: sets up to run batches of trials in a 3x3 grid environment with internal walls to make a maze. For details about the maze, you can look at the image files inside the folder.

10.3) analysis5x5Grid: sets up to run batches of trials in an empty 5x5 grid environment.

10.4) analysis5x5Maze: sets up to run batches of trials in a 5x5 grid environment with internal walls to make a maze. For details about the maze, you can look at the image files inside the folder.

11) javaMazeGraphics: connects the python program for the 5x5 maze to bluej (see point C) that creates a visualization of running one trial at a time. This is done through running the main method of the GrigGraphics class, then it runs on the same mechanic of pressing enter and q in the graphics window as the rest of the java graphics. Adjusting the maze by commenting out or adding new walls in the python script in that folder adjusts the maze in the java graphics as well.

12) analysisPunishment1: analyzes 4 scenarios, comparing the CA's performance in a 3x3 maze and a 5x5 maze without vs with punishment input. All the versions run the same as analysisFist, just using the updated implementation of trials2.py and largeAnalysis2.py for better record keeping and speed. The versions with punishments run with a different configuration file (see point D), which includes a punishment state for the CA to go into. Then in the trials, whenever the CA tries to move but there's a wall in front of it, it will recieve a punishment signal to reinforce its leraning. This serves as a representation of a pain response whenever the subject walks into a wall. Note: all scenarios run the program with caNew, an updated faster model of the CA mechanism provided by the professor.

13) analysisPunishment2: collects data for a 4x4 maze scenario under different punishment conditions for 2 slightly different mazes, one harder with all the walls and one easier with less walls. Within both, the regular version uses the previous visionMaze config file (see point D), and the other ones test it with a config file that includes a punishment state. That punishment is applied the same as in analysisPunishment1 for when the subject tries to move into a wall. There are tests to run this experiment with varying strengths of the punishment signal. This folder also contains the explanation for how we are doing the new calculations for the line of best fit. Within each maze scenario, there are scripts that handle entering the data from the batch files into an excel spreadsheet and calculating the b values for each scenario (see point E)

14) analysisBeta: collects data for a 4x4 maze scenario under different values of the beta parameter in the configuration files. Has the code (not the individual data because that would be too many files) for each setting in a separate folder. Uses the same mathematical fit model and method of calculating it through excel as analysisPunishment2 (see point E).

15) batchGraphing: python scripts to run on the batch#.txt files generated from trials. For each of the scripts, provide the file paths for which ones you want to graph. The way to do so is described in the comments: right click on the file, hold option key, and click "Copy "__" as Pathname". It has several different ways to graph different files. Feel free to play around with any of the visual settings such as line thickness/color for better visibility.

15.1) oneFileGraph: give the path to one data file and it will graph it

15.2) severalFilesGraph.py: give the path to multiple data files in a list and it will graph them on top of each other with different colors for each file

15.3) severalGroupsGraph.py: give the path to several files in a few groups (such as different scenarios), adding them to several lists organized by group. Then assign each group a unique color in the dictionary. The program then graphs all of the files on top of each other, with files from the same group being the same color.

15.4) animatedGraph.py: generates an animation of all the data from a specific group, with the individual graphs appearing one right after the other. Provide the name of the scenarion for the graph label, the directory where all of your files are located, and the number of the batch up through which you want to show the results. For this version, make sure to double check the values for the max steps per trial and the trials per batch and change the a and xSmooth values accordingly.

15.5) animatedBestFit.py: works the same way as animatedGraph.py, but for every batch displayed also draws a line of best fit that was calculated for it (in the form of y = a * e^(-bt)).

16) combinationAttempt1: combines several CAs to learn a maze. The overall structure consists of 2 sensor CAs (one for immediate surrounding vision and one for spatial awareness) and one decision maker CA that determines the final action to take. The final decision is made by sending the outputs of the sensor CAs as the simultaneous inputs to the decision CA. The details of the structure are in 3x3MazeCombined/notes.txt, but they aren't entirely comprehensive regarding the spatial CA so if you want any clarification on how that works, lmk! 3x3MazeCombined implements the new multiple CA structure, 3x3MazeVision and 3x3MazeSpatial are used for control to see how the CA learns with just the vision or the spatial sensor. 4x4MazeCombined and 5x5MazeCombined run the multiple CA structure on larger more complicated mazes.

17) combinationAttempt2: sets up tests to see how the combined 3-CA model can be improved. OriginalSensorData tracks how often the CA chooses the final decision based on the vision vs spatial sensor in a given batch. analysisAlpha tests the combined CA with 3 different alpha levels. expandedConfigConfX and expandedConfigConfX test the combined CA where instead of the 2 sensors' suggestions being sent as 2 different simultaneous inputs, each combination of their suggestions is encoded as a different state and sent as 1 input. ConfX uses the average confidence as the input signal strength and Conf1 always sends it with strength 1.

18) analysisPunishment3: sets up tests on individual CAs to sidestep the issue of weird behavior in punishment reinforcement by changing the probabilities through reward only. The basic idea is that rewarding all actions except for running into walls should achieve the same mathematical effect as punishing running into walls. More detailed notes on the setup are included in a text file within each folder, which is recommended to read if you're looking for more information on the reward setup (as always reach out if you have any questions). It has the setups for running a vision and a spatial CA testing different strengths of the new small-scale reward signal.

19) analysisPunishment4: tests out different scenarios of the inverse punishment through reward mechanic on individual CAs instead of the combined one. Also, tracks learning not in terms of solving the maze but in terms of how well the CA learns to not run into walls. It does this through tracking the proportion of non-punished actions out of total actions taken, and the proportion of zero/nothing actions out of non-punished actions. It does calculations with these results for the vision and spatial CAs, trying out small reward strengths of 0.05 and 0.1 for each. General details are described in notes.txt, and calculation details are described in mathImage.jpg.

20) combinationAttempt3: uses the results of analysisPunishment4 to implement more robust combined CAs. combinedSmallReward implements the reward for not running into walls with the strengths determined in analysisPunishment4. combinedMediumReward implements a third level of reward whenever the CA reaches a new region. The strengths for the medium reward have not been tested.

21) analysisPunishment5: Runs a single vision CA with the new CA executable that has the updated punishment equations. Punishments are applied when the CA runs into a wall. Tests various strengths to compare the learning speed.

22) combinationAttempt4: Implements a combined CA structure similar to the one in previous combination attempts, however now pre-trains the individual sensor CAs before using them for the combined version. It runs a set of trials with the vision on its own, the spatial on its own, and then uses these already trained CAs in the combined version. Results show that it performs worse than the individual vision and spatial CAs on its own but better than the previous combined version.

A) getting initial files on tux: if you want to access the original CA files, they can be copied over from the bls directory using the instructions in the cause file in the reading folder: The cybernetic automaton model has been reimplemented in Go and is currently available on tux. The directory: /home/bls96/ca has the source code, configurations, and driver scripts for most of the examples described in the dissertation on the subject. In addition to that directory, there’s a copy of the executable in the /home/bls96/bin directory.

B) running the files in tux: if you want to run any of the initialCA python 2 driver programs, you run the driver with ./ and pass it the configuration file that you want to use as a commanf line argument, so the command is in the format: ./pythonFile.py configurationFile.cfg and it will give you the output and error of the python program as it runs a CA experiment with a CA behaving according to the behavior specified in its configuration file. For any the skinner.py driver use skinner.cfg, for all others use basic.cfg. If you want to run any of the python3translations programs, you use the command in the format: python3 pythonFile.py configurationFile.cfg and it will give you the appropriate output. You can also graph the outputs of these programs, run either the python 2 or python 3 command and then put the output into another file with > outputFile.out for example: python3 d1.py > d1.out which will create an output file in your directory. Then run the command: gnuplot -e "set terminal dumb; plot 'outputFile.out' with lines" and it will generate a pictore of the graph for that run with ascii characters.

C) bluej basics: bluej is a platform that lets you run java files and link them to graphics. You can download it for free at https://www.bluej.org/ and run it on your computer. To use it with the files here, download the folder with all of the files onto your computer, open it, and find the package.bluej file, it should have the bluej logo on it. Double click it to open up the bluej project for that folder. There, you will see all of the files available as orange boxes. To see and edit the code, double click on any of the boxes. To run the code, right click on any of the boxes and click the void main(String[] args) option. To save any code changes, click the compile button in the top left of the editor or the compile button in the top left of the main window, which also compiles any related files that also need to be updated as a result of your changes.

D) configuration files: the details of how a configuration file is structured are outlined in the cause file in the reading folder. The contents of the file dictate the initial state of the CA when the experiment begins. The basic configuration is used for the non-skinner conditioning experiments. The skinner configuration is the one used for the skinner box in the dissertation. With it, the mouse keeps track of its location and direction internally. The skinnerVision configuration changes that mechanism so that the mouse doesn't inherently know what position it's in, just what it sees around itself (if it's at a corner, facing a wall, near the bar, etc). 

E) excel calculations: current location(s) of the excel calculation script: analysisPunishment2/easier4x4, analysisPunishment2/harder4x4, analysisBeta, combinationAttempt1. These are the steps to set up the spreadsheet and scripts to analyze the learning speed of the CA in a given situation. The calculations are to find the b value for a line of best fit with the formula y = a * e^(-bt)
1) Have the data for all of the different scenarios you are testing ready (ex. the scenarios in analysisPunishment2/easier4x4 are regular/no punishment, punishment with strength 1, 0.5, etc.). The data (batch0.txt, batch1.txt, etc. files) for each scenario/parameter setting should be in a separate folder in the same directory as where you're gonna put the spreadsheet and scripts.
2) Copy the script files (dataEntry.py and dataLinearizationCalc.py) from one of the locations they are present in (at the top of point E) onto your computer and put them into the same folder as the folders with the data.
3) Make a new spreadsheet on excel and download it or a copy of it onto your computer, put it into the same folder with all of your folders of data. Now you should have a folder that contains the following: dataEntry.py, dataLinearization.py, yourSpreadsheet.xlsx, dataFolderScenario1, dataFolderScenario2, etc.
4) In the spreadsheet, make a sheet for each scenario that you're testing where the raw data from all the batches will be stored (ex. analysisPunishment2/easier4x4 has sheets for RegData, 1Data, 0.5Data, etc.). Then make another sheet for every schenario where the b value for each batch will be stored (ex. analysisPunishment2/easier4x4 has sheets for RegDataBVals, 1DataBVals, etc.)
5) Go into the dataEntry.py script. Change the spreadSheetPath variable to be the name of your spreadsheet in this folder (ex. analysisPunishment2/easier4x4 has STAR Data Punishment (4x4Easy).xlsx). Then in the sheetToPath dictionary, change all the keys to the names of the sheets for your raw data and all the values to the names of the folders that have that raw data (ex. analysisPunishment2/easier4x4 has 'RegData': 'analysis4x4MazeReg' because we want the data files in the analysis4x4MazeReg to be put into the sheet called RegData).
6) Go into the dataLinearizationCalc.py script. Change the variable a at the top to be the number of max steps allowed per trial. Change the spreadSheetPath variable to be the name of your spreadsheet in this folder (ex. analysisPunishment2/easier4x4 has STAR Data Punishment (4x4Easy).xlsx). Then change the targetSheets list to be a list of all the sheets with the raw data, that is where the program will take the numbers to use for its calculations (ex. analysisPunishment2/easier4x4 has sheets for RegData, 1Data, etc.). Then in the last block (inside the for loop that's in the with statement), change the variable of sheetToStoreIn to match the pattern of how the raw data sheet relates to the b value sheet (ex. analysisPunishment2/easier4x4 has f"{sheet}BVals" because for every raw data sheet, its corresponding b value data sheet is called ___BVals).
7) Make sure to save all your files!
8) Run dataEntry.py and check your spreadsheet to make sure all of the raw data sheets have been appropriately filled in. Each batch should take up one column in the sheet corresponding to its scenario with a label for the batch number in the first row and the results for each trial going down. I would recommend picking a few random batches and making sure the numbers in the text file match the ones in the spreadsheet.
9) Run dataLinearizationCalc.py and check your spreadsheet to make sure all of the b value data sheets have been appropriately filled in. Each batch should take up one column in the sheet corresponding to its scenario with a label for the batch number in the first row and the b value calculated for that batch in the second row.
10) Calculate the average b value for each scenario by going to that scenario's b value sheet and choosing a random empty cell (you can also write a label in the cell above it) and in the cell where you want to store the average, write the formula =AVERAGE(startingCell:endingCell) so that you cover the entire second row that has b values (ex. analysisPunishment2/easier4x4 has =AVERAGE(A2:AN2) for the 2nd row of the first 40 columns representing the 40 batches that were run)
11) Now you have the average b value for a given parameter setting! The larger the b value is, the steeper the downwards curve is, so the faster the ca learned in that situation.
