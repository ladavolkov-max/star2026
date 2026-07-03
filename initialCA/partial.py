#!/usr/bin/python
from subprocess import *
import random

pid = Popen(["/home/bls96/bin/ca", "basic.cfg"], stdin=PIPE, stdout=PIPE)

print "100%"

print 0, 0
for i in xrange(4):
	n = 0
	for j in xrange(10):
		pid.stdin.write("3/1\n")
		x = pid.stdout.readline()
		if x[0] == "1":
			n += 1
		pid.stdin.write("1/1\n")
		pid.stdout.readline()
		pid.stdin.write("4/1\n")
		pid.stdout.readline()
		pid.stdin.write("2/1\n")
		pid.stdout.readline()
		pid.stdin.write("0/1\n")
		pid.stdout.readline()
	print i+1, n

print
print 0, n
for i in xrange(10):
	n = 0
	for j in xrange(10):
		pid.stdin.write("3/1\n")
		x = pid.stdout.readline()
		if x[0] == "1":
			n += 1
		pid.stdin.write("4/1\n")
		pid.stdout.readline()
		pid.stdin.write("0/1\n")
		pid.stdout.readline()
	print i+1, n

pid.stdin.close()

pid = Popen(["/home/bls96/bin/ca", "basic.cfg"], stdin=PIPE, stdout=PIPE)

print "75%"

print 0, 0
for i in xrange(4):
	n = 0
	for j in xrange(10):
		pid.stdin.write("3/1\n")
		x = pid.stdout.readline()
		if x[0] == "1":
			n += 1
		d = random.random()
		if d <= 0.75:
			pid.stdin.write("1/1\n")
			pid.stdout.readline()
		pid.stdin.write("4/1\n")
		pid.stdout.readline()
		if d <= 0.75:
			pid.stdin.write("2/1\n")
			pid.stdout.readline()
		pid.stdin.write("0/1\n")
		pid.stdout.readline()
	print i+1, n

print
print 0, n
for i in xrange(10):
	n = 0
	for j in xrange(10):
		pid.stdin.write("3/1\n")
		x = pid.stdout.readline()
		if x[0] == "1":
			n += 1
		pid.stdin.write("4/1\n")
		pid.stdout.readline()
		pid.stdin.write("0/1\n")
		pid.stdout.readline()
	print i+1, n

pid.stdin.close()

pid = Popen(["/home/bls96/bin/ca", "basic.cfg"], stdin=PIPE, stdout=PIPE)

print "50%"

print 0, 0
for i in xrange(4):
	n = 0
	for j in xrange(10):
		pid.stdin.write("3/1\n")
		x = pid.stdout.readline()
		if x[0] == "1":
			n += 1
		d = random.random()
		if d <= 0.50:
			pid.stdin.write("1/1\n")
			pid.stdout.readline()
		pid.stdin.write("4/1\n")
		pid.stdout.readline()
		if d <= 0.50:
			pid.stdin.write("2/1\n")
			pid.stdout.readline()
		pid.stdin.write("0/1\n")
		pid.stdout.readline()
	print i+1, n

print
print 0, n
for i in xrange(10):
	n = 0
	for j in xrange(10):
		pid.stdin.write("3/1\n")
		x = pid.stdout.readline()
		if x[0] == "1":
			n += 1
		pid.stdin.write("4/1\n")
		pid.stdout.readline()
		pid.stdin.write("0/1\n")
		pid.stdout.readline()
	print i+1, n

pid.stdin.close()

pid = Popen(["/home/bls96/bin/ca", "basic.cfg"], stdin=PIPE, stdout=PIPE)

print "25%"

print 0, 0
for i in xrange(4):
	n = 0
	for j in xrange(10):
		pid.stdin.write("3/1\n")
		x = pid.stdout.readline()
		if x[0] == "1":
			n += 1
		d = random.random()
		if d <= 0.25:
			pid.stdin.write("1/1\n")
			pid.stdout.readline()
		pid.stdin.write("4/1\n")
		pid.stdout.readline()
		if d <= 0.25:
			pid.stdin.write("2/1\n")
			pid.stdout.readline()
		pid.stdin.write("0/1\n")
		pid.stdout.readline()
	print i+1, n

print
print 0, n
for i in xrange(10):
	n = 0
	for j in xrange(10):
		pid.stdin.write("3/1\n")
		x = pid.stdout.readline()
		if x[0] == "1":
			n += 1
		pid.stdin.write("4/1\n")
		pid.stdout.readline()
		pid.stdin.write("0/1\n")
		pid.stdout.readline()
	print i+1, n

pid.stdin.close()

