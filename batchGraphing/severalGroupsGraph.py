import matplotlib.pyplot as plt

#organize files by groups, which ones you want to have the same color
#right click on ur file, hold option key, and click "Copy "__" as Pathname"
group1paths = [
    "/Users/ladavolkov/Desktop/analysisPunishment2/harder4x4/analysis4x4MazePun0.5/batch0.txt",
    "/Users/ladavolkov/Desktop/analysisPunishment2/harder4x4/analysis4x4MazePun0.5/batch1.txt",
    "/Users/ladavolkov/Desktop/analysisPunishment2/harder4x4/analysis4x4MazePun0.5/batch2.txt"
    ]
group2paths = [
    "/Users/ladavolkov/Desktop/analysisPunishment2/harder4x4/analysis4x4MazePun0.25/batch0.txt",
    "/Users/ladavolkov/Desktop/analysisPunishment2/harder4x4/analysis4x4MazePun0.25/batch1.txt",
    "/Users/ladavolkov/Desktop/analysisPunishment2/harder4x4/analysis4x4MazePun0.25/batch2.txt"
]
group3paths = [
    "/Users/ladavolkov/Desktop/analysisPunishment2/harder4x4/analysis4x4MazeReg/batch0.txt",
    "/Users/ladavolkov/Desktop/analysisPunishment2/harder4x4/analysis4x4MazeReg/batch1.txt",
    "/Users/ladavolkov/Desktop/analysisPunishment2/harder4x4/analysis4x4MazeReg/batch2.txt"
]

#dictionary associating each group with its color
file_groups = {
    "blue": group1paths,
    "red": group2paths,
    "green": group3paths,
}

#looping thorugh each color group
for color, file_list in file_groups.items():
    #loop through each file in the group
    for file_name in file_list:
        try:
            with open(file_name, "r") as file:
                #read numbers, skipping empty lines
                y_values = [float(line.strip()) for line in file if line.strip()]

            #linewidth=0.5 makes it skinnier, default line width is 1.5
            #color=color manually forces the line color
            plt.plot(y_values, color=color, linewidth=0.25, label=file_name)

        except FileNotFoundError:
            print(f"Warning: {file_name} not found. Skipping.")

#graph setup
plt.xlabel("Trial")
plt.ylabel("Steps")
plt.title("Grouped Data Comparison")
#plt.grid(True, alpha=0.3)  # alpha lowers grid opacity
#plt.legend()
plt.show()