import matplotlib.pyplot as plt

#provide the path to the file that you want to graph
#right click on ur file, hold option key, and click "Copy "__" as Pathname"
with open("/Users/ladavolkov/Desktop/analysisPunishment2/harder4x4/analysis4x4MazePun0.5/batch2.txt", "r") as file:
    y_values = [float(line.strip()) for line in file]

plt.plot(y_values)
plt.xlabel("Trial")
plt.ylabel("Steps")
plt.show()
