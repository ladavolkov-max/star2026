#!/usr/bin/python3
from subprocess import *

#
# 1: UCS+, 2: UCS-, 3: CS1+, 4:CS1-, 5: CS2+, 6: CS2-
#
pid = Popen(["/home/bls96/bin/ca", "basic.cfg"], stdin=PIPE, stdout=PIPE, bufsize=0)

for i in range(20):
	pid.stdin.write(b"3/1 5/0.9\n")
	x = pid.stdout.readline()
	pid.stdin.write(b"4/1 6/0.9\n")
	x = pid.stdout.readline()
	pid.stdin.write(b"0/1\n")
	x = pid.stdout.readline()

# pid.stdin.write("D\n")

for i in range(100):
	pid.stdin.write(b"3/1\n")
	pid.stdout.readline()
	pid.stdin.write(b"1/1\n")
	pid.stdout.readline()
	pid.stdin.write(b"4/1\n")
	pid.stdout.readline()
	pid.stdin.write(b"2/1\n")
	pid.stdout.readline()
	pid.stdin.write(b"0/1\n")
	pid.stdout.readline()

for i in range(10):
	n = 0
	for j in range(10):
		pid.stdin.write(b"5/1\n")
		x = pid.stdout.readline()
		if x[0:1] == b"1":
			n += 1
		pid.stdin.write(b"6/1\n")
		pid.stdout.readline()
		pid.stdin.write(b"0/1\n")
		pid.stdout.readline()
	print (i+1, n)

pid.stdin.close()
