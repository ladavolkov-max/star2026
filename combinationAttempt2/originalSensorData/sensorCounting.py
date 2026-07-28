if __name__ == "__main__":

    filePath = "batch1.txt"
    individualCounts = []
    cumulativeCounts = []
    individualProportions = []
    cumulativeProportions = []

    try:
        file = open(filePath, "r")
    except FileNotFoundError:
        print(f"Error! file not found at path: {filePath}")

    lines = file.readlines()
    ii = 0
    while (ii < len(lines)):
        #start of a new trial
        if lines[ii].startswith("TRIAL"):
            #establish variables
            visionCount = 0
            spatialCount = 0
            ii += 1
            #go until the start of the next trial or end of file
            while (ii < len(lines) and not lines[ii].startswith("TRIAL")):
                decision = lines[ii].split()[-1]
                if(decision == "vision"):
                    visionCount += 1
                elif(decision == "spatial"):
                    spatialCount += 1
                else:
                    print(f"unknown decision string: {decision}")
                ii += 1
            #updating the counts in the list
            individualCounts.append((visionCount, spatialCount))

    #calculations
    cumulativeCounts.append(individualCounts[0])
    for ii in range(1, len(individualCounts)):
        cumulativeCounts.append(
            (
            cumulativeCounts[ii - 1][0] + individualCounts[ii][0],
            cumulativeCounts[ii - 1][1] + individualCounts[ii][1]
            )
            )

    for ii in range(0, len(individualCounts)):
        individualProportions.append(
                (
                individualCounts[ii][0] / (individualCounts[ii][0] + individualCounts[ii][1]), 
                individualCounts[ii][1] / (individualCounts[ii][0] + individualCounts[ii][1])
                )
                )
        cumulativeProportions.append(
                (
                cumulativeCounts[ii][0] / (cumulativeCounts[ii][0] + cumulativeCounts[ii][1]), 
                cumulativeCounts[ii][1] / (cumulativeCounts[ii][0] + cumulativeCounts[ii][1])
                )
                )

    #printing results
    print(f"{ii}")
    print(cumulativeProportions)
