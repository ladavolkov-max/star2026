import matplotlib.pyplot as plt

#list to the paths of all the files that you want to be included in the graph
#right click on ur file, hold option key, and click "Copy "__" as Pathname"
files = [
    "/Users/ladavolkov/Desktop/analysisPunishment2/harder4x4/analysis4x4MazeReg/batch0.txt",
    "/Users/ladavolkov/Desktop/analysisPunishment2/harder4x4/analysis4x4MazeReg/batch1.txt",
    "/Users/ladavolkov/Desktop/analysisPunishment2/harder4x4/analysis4x4MazeReg/batch2.txt"]

for file_name in files:
    with open(file_name, "r") as file:
        #read numbers, skipping empty lines
        y_values = [float(line.strip()) for line in file if line.strip()]

    #plot each file, line number is automatically the x val
    plt.plot(y_values, label=file_name)

#graph setup
plt.xlabel("Trial")
plt.ylabel("Steps")
plt.title("Comparison of Multiple Data Files")
#plt.legend()  #shows which color belongs to which file
plt.grid(True)  #adds a grid
plt.show() #show the combined graph
