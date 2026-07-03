#!/usr/bin/python3
from subprocess import *

pid = Popen(["/home/bls96/bin/ca", "basic.cfg"], stdin=PIPE, stdout=PIPE, bufsize=0)

print (0, 0)
for i in range(10):
	n = 0
	for j in range(10):
		pid.stdin.write(b"3/1\n")
		x = pid.stdout.readline()
		if x[0:1] == b"1":
			n = n + 1
		pid.stdin.write(b"1/1\n")
		x = pid.stdout.readline()
		pid.stdin.write(b"4/1\n")
		x = pid.stdout.readline()
		pid.stdin.write(b"2/1\n")
		x = pid.stdout.readline()
		pid.stdin.write(b"0/1\n")
		x = pid.stdout.readline()
	print (i+1, n)
pid.stdin.write(b"D\n")
pid.stdin.close()
