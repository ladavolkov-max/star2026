#!/usr/bin/python3
from subprocess import *
import random

pid = Popen(["/home/bls96/bin/ca", "basic.cfg"], stdin=PIPE, stdout=PIPE, bufsize=0)

print ("100%")

print (0, 0)
for i in range(4):
	n = 0
	for j in range(10):
		pid.stdin.write(b"3/1\n")
		x = pid.stdout.readline()
		if x[0:1] == b"1":
			n += 1
		pid.stdin.write(b"1/1\n")
		pid.stdout.readline()
		pid.stdin.write(b"4/1\n")
		pid.stdout.readline()
		pid.stdin.write(b"2/1\n")
		pid.stdout.readline()
		pid.stdin.write(b"0/1\n")
		pid.stdout.readline()
	print (i+1, n)

print
print (0, n)
for i in range(10):
	n = 0
	for j in range(10):
		pid.stdin.write(b"3/1\n")
		x = pid.stdout.readline()
		if x[0:1] == b"1":
			n += 1
		pid.stdin.write(b"4/1\n")
		pid.stdout.readline()
		pid.stdin.write(b"0/1\n")
		pid.stdout.readline()
	print(i+1, n)

pid.stdin.close()

pid = Popen(["/home/bls96/bin/ca", "basic.cfg"], stdin=PIPE, stdout=PIPE, bufsize=0)

print ("75%")

print (0, 0)
for i in range(4):
	n = 0
	for j in range(10):
		pid.stdin.write(b"3/1\n")
		x = pid.stdout.readline()
		if x[0:1] == b"1":
			n += 1
		d = random.random()
		if d <= 0.75:
			pid.stdin.write(b"1/1\n")
			pid.stdout.readline()
		pid.stdin.write(b"4/1\n")
		pid.stdout.readline()
		if d <= 0.75:
			pid.stdin.write(b"2/1\n")
			pid.stdout.readline()
		pid.stdin.write(b"0/1\n")
		pid.stdout.readline()
	print (i+1, n)

print ()
print (0, n)
for i in range(10):
	n = 0
	for j in range(10):
		pid.stdin.write(b"3/1\n")
		x = pid.stdout.readline()
		if x[0:1] == b"1":
			n += 1
		pid.stdin.write(b"4/1\n")
		pid.stdout.readline()
		pid.stdin.write(b"0/1\n")
		pid.stdout.readline()
	print (i+1, n)

pid.stdin.close()

pid = Popen(["/home/bls96/bin/ca", "basic.cfg"], stdin=PIPE, stdout=PIPE, bufsize=0)

print ("50%")

print (0, 0)
for i in range(4):
	n = 0
	for j in range(10):
		pid.stdin.write(b"3/1\n")
		x = pid.stdout.readline()
		if x[0:1] == b"1":
			n += 1
		d = random.random()
		if d <= 0.50:
			pid.stdin.write(b"1/1\n")
			pid.stdout.readline()
		pid.stdin.write(b"4/1\n")
		pid.stdout.readline()
		if d <= 0.50:
			pid.stdin.write(b"2/1\n")
			pid.stdout.readline()
		pid.stdin.write(b"0/1\n")
		pid.stdout.readline()
	print (i+1, n)

print ()
print (0, n)
for i in range(10):
	n = 0
	for j in range(10):
		pid.stdin.write(b"3/1\n")
		x = pid.stdout.readline()
		if x[0:1] == b"1":
			n += 1
		pid.stdin.write(b"4/1\n")
		pid.stdout.readline()
		pid.stdin.write(b"0/1\n")
		pid.stdout.readline()
	print (i+1, n)

pid.stdin.close()

pid = Popen(["/home/bls96/bin/ca", "basic.cfg"], stdin=PIPE, stdout=PIPE, bufsize=0)

print ("25%")

print (0, 0)
for i in range(4):
	n = 0
	for j in range(10):
		pid.stdin.write(b"3/1\n")
		x = pid.stdout.readline()
		if x[0:1] == b"1":
			n += 1
		d = random.random()
		if d <= 0.25:
			pid.stdin.write(b"1/1\n")
			pid.stdout.readline()
		pid.stdin.write(b"4/1\n")
		pid.stdout.readline()
		if d <= 0.25:
			pid.stdin.write(b"2/1\n")
			pid.stdout.readline()
		pid.stdin.write(b"0/1\n")
		pid.stdout.readline()
	print (i+1, n)

print ()
print (0, n)
for i in range(10):
	n = 0
	for j in range(10):
		pid.stdin.write(b"3/1\n")
		x = pid.stdout.readline()
		if x[0:1] == b"1":
			n += 1
		pid.stdin.write(b"4/1\n")
		pid.stdout.readline()
		pid.stdin.write(b"0/1\n")
		pid.stdout.readline()
	print (i+1, n)

pid.stdin.close()

