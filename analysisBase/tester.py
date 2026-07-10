from trials import *
if __name__ == "__main__":
    """
    print("1) Number of trials to run in the batch")
    print("2) Max steps per trial")
    print("3) Grid width (number of columns)")
    print("4) Grid height (number of rows)")
    print("5) Randomize starting location (True/False)")
    print("6) Randomize starting direction (True/False)")
    print("7) Starting location X (col) (optional, 1-indexed, default is 1 for top left corner)")
    print("8) Starting location Y (row) (optional, 1-indexed, default is Grid Height for top left corner)")
    print("9) Starting Direction (optional, default is 2) (N=1, E=2, S=3, W=4)")
    print("10) Bar location X (col) (optional, 1-indexed, default is Grid Width for bottom right corner)")
    print("11) Bar location Y (row) (optional, 1-indexed, default is 1 for bottom right corner)")
    print("12) Bar direction (optional, default is 2) (N=1, E=2, S=3, W=4)")
    print("13) Inner walls (optional, default is none) (list of lists w/ 1-indexed (x, y, dir))")
    """
    testBatch = TrialBatch(1, 1, 2, 2, False, False, 2, 2, 2)
    testBatch.runBatch()