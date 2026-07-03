#!/usr/bin/python2
from subprocess import *
import random
import sys

#
# 1:1N, 2:1E, 3:1S, 4:1W, 5:2N, 6:2E, 7:2S, 8:2W, 9:F
#
# 1:Left, 2:Right, 3:Move, 4:Press
#

pid = Popen(["/home/bls96/bin/ca", "skinner.cfg"], stdin=PIPE, stdout=PIPE)

random.seed()
for i in xrange(300):
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
	for j in xrange(50):
		pid.stdin.write(str((loc - 1) * 4 + dir) + '/1\n')
		x = pid.stdout.readline()
		if x[0] == '1':
			dir -= 1
			if dir == 0:
				dir = 4
		elif x[0] == '2':
			dir += 1
			if dir > 4:
				dir = 1
		elif x[0] == '3':
			if loc == 1 and dir == 2:
				loc = 2
			elif loc == 2 and dir == 4:
				loc = 1
		elif x[0] == '4':
			if loc == 2 and dir == 2:
				pid.stdin.write("9/1\n")
				pid.stdout.readline()
				break
	pid.stdin.write("0/1\n")
	pid.stdout.readline()
	print i, j
	
