#!/usr/bin/python
from subprocess import *

#
# 1:UCS+, 2:UCS-, 3:CS1+, 4:CS1-, 5:CS2+, 6:CS2-
#

pid = Popen(["/home/bls96/bin/ca", "basic.cfg"], stdin=PIPE, stdout=PIPE)

n = 0
while n < 80:
	pid.stdin.write("3/1\n")
	x = pid.stdout.readline()
	if x[0] == "1":
		n += 1
	else:
		n = 0
	pid.stdin.write("1/1\n")
	pid.stdout.readline()
	pid.stdin.write("4/1\n")
	pid.stdout.readline()
	pid.stdin.write("2/1\n")
	pid.stdout.readline()
	pid.stdin.write("0/1\n")
	pid.stdout.readline()

for i in xrange(20):
	pid.stdin.write("3/1 5/0.9\n")
	pid.stdout.readline()
	pid.stdin.write("4/1 6/0.9\n")
	pid.stdout.readline()
	pid.stdin.write("0/1\n")
	pid.stdout.readline()

for i in xrange(10):
	n = 0
	for j in xrange(10):
		pid.stdin.write("5/1\n")
		x = pid.stdout.readline()
		if x[0] == "1":
			n += 1
		pid.stdin.write("6/1\n")
		pid.stdout.readline()
		pid.stdin.write("0/1\n")
		pid.stdout.readline()
	print i+1, n

pid.stdin.close()
