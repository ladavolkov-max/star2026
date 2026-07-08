#!/usr/bin/python3
from subprocess import *
import random
import sys
import matplotlib.pyplot as plt
import numpy as np
import os

baseDir = os.path.dirname(os.path.abspath(__file__))
caPath = os.path.join(baseDir, "ca")
cfgPath = os.path.join(baseDir, "skinnerVision.cfg")

pid = Popen([caPath, cfgPath], stdin=PIPE, stdout=PIPE, bufsize=0)

transitions = {
    (1, 2): 2,  # top-left moving E -> top-right
    (2, 4): 1,  # top-right moving W -> top-left
    (3, 2): 4,  # bottom-left moving E -> bottom-right
    (4, 4): 3,  # bottom-right moving W -> bottom-left
    (1, 3): 3,  # top-left moving S -> bottom-left
    (3, 1): 1,  # bottom-left moving N -> top-left
    (2, 3): 4,  # top-right moving S -> bottom-right
    (4, 1): 2,  # bottom-right moving N -> top-right
}

leverLoc = 4   # bottom-right chamber
leverDir = 2   # facing East

results = []

random.seed()
for i in range(300):
    loc = random.choice([1, 2, 3, 4])

    d = random.random()
    if d > 0.75:
        dir = 1
    elif d > 0.5:
        dir = 2
    elif d > 0.25:
        dir = 3
    else:
        dir = 4

    sys.stderr.write(str(i) + '\n')

    for j in range(50):
        # % 11 keeps stateCode safely within bounds (0-10) of skinnerVision.cfg
        stateCode = ((loc - 1) * 4 + dir) % 11
        pid.stdin.write((str(stateCode) + '/1\n').encode('utf-8'))
        x = pid.stdout.readline()

        if x[0:1] == b'1':
            dir -= 1
            if dir == 0:
                dir = 4
        elif x[0:1] == b'2':
            dir += 1
            if dir > 4:
                dir = 1
        elif x[0:1] == b'3':
            loc = transitions.get((loc, dir), loc)
        elif x[0:1] == b'4':
            if loc == leverLoc and dir == leverDir:
                pid.stdin.write(b"9/1\n")
                pid.stdout.readline()
                break

    pid.stdin.write(b"0/1\n")
    pid.stdout.readline()
    print(i, j)
    results.append(j)

trials = np.arange(300)
resultsArray = np.array(results)

plt.figure()
plt.plot(trials, resultsArray, label="Steps")

# trendline
degree = 3
coeffs = np.polyfit(trials, resultsArray, degree)
poly = np.poly1d(coeffs)
trend = poly(trials)
plt.plot(trials, trend, color="red", linewidth=2, label=f"Degree-{degree} trend")

plt.ylim(0, 50)
plt.xlabel("Trial")
plt.ylabel("Steps")
plt.title("Skinner Box (2x2)")
plt.legend()
plt.show()