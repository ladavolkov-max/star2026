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

9) analysisBase: the 


A) getting initial files on tux: if you want to access the original CA files, they can be copied over from the bls directory using the instructions in the cause file in the reading folder: The cybernetic automaton model has been reimplemented in Go and is currently available on tux. The directory: /home/bls96/ca has the source code, configurations, and driver scripts for most of the examples described in the dissertation on the subject. In addition to that directory, there’s a copy of the executable in the /home/bls96/bin directory.

B) running the files in tux: if you want to run any of the initialCA python 2 driver programs, you run the driver with ./ and pass it the configuration file that you want to use as a commanf line argument, so the command is in the format: ./pythonFile.py configurationFile.cfg and it will give you the output and error of the python program as it runs a CA experiment with a CA behaving according to the behavior specified in its configuration file. For any the skinner.py driver use skinner.cfg, for all others use basic.cfg. If you want to run any of the python3translations programs, you use the command in the format: python3 pythonFile.py configurationFile.cfg and it will give you the appropriate output. You can also graph the outputs of these programs, run either the python 2 or python 3 command and then put the output into another file with > outputFile.out for example: python3 d1.py > d1.out which will create an output file in your directory. Then run the command: gnuplot -e "set terminal dumb; plot 'outputFile.out' with lines" and it will generate a pictore of the graph for that run with ascii characters.

C) bluej basics: bluej is a platform that lets you run java files and link them to graphics. You can download it for free at https://www.bluej.org/ and run it on your computer. To use it with the files here, download the folder with all of the files onto your computer, open it, and find the package.bluej file, it should have the bluej logo on it. Double click it to open up the bluej project for that folder. There, you will see all of the files available as orange boxes. To see and edit the code, double click on any of the boxes. To run the code, right click on any of the boxes and click the void main(String[] args) option. To save any code changes, click the compile button in the top left of the editor or the compile button in the top left of the main window, which also compiles any related files that also need to be updated as a result of your changes.

D) configuration files: the details of how a configuration file is structured are outlined in the cause file in the reading folder. The contents of the file dictate the initial state of the CA when the experiment begins. The basic configuration is used for the non-skinner conditioning experiments. The skinner configuration is the one used for the skinner box in the dissertation. With it, the mouse keeps track of its location and direction internally. The skinnerVision configuration changes that mechanism so that the mouse doesn't inherently know what position it's in, just what it sees around itself (if it's at a corner, facing a wall, near the bar, etc). 
