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

#pid = Popen(["/Users/lenas/Desktop/STARca", "/Users/lenas/Desktop/STAR Scholars/skinner.cfg"], stdin=PIPE, stdout=PIPE, bufsize=0)

results = []

random.seed()
for i in range(300):
        loc = random.randint(1, 2)
        d = random.random()
        if d > 0.5:
                loc = 2
        else:
                loc = 1
        dir = random.randint(1, 4)
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
                pid.stdin.write((str((loc - 1) * 4 + dir) + '/1\n').encode('utf-8'))
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
                        if loc == 1 and dir == 2:
                                loc = 2
                        elif loc == 2 and dir == 4:
                                loc = 1
                elif x[0:1] == b'4':
                        if loc == 2 and dir == 2:
                                pid.stdin.write(b"9/1\n")
                                pid.stdout.readline()
                                break
        pid.stdin.write(b"0/1\n")
        pid.stdout.readline()
        print (i, j)
        results.append(j)

trials = np.arange(300)
resultsArray = np.array(results)

plt.figure()
plt.plot(trials, resultsArray,label="Steps")

# creating trendline
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