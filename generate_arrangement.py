#!/usr/bin/env python

import random

class RandomNonRepeat():
	def __init__(self, elements):
		self.elements = elements
		self.shuffled = []
		self.pos = 0

	def next(self):
		if self.pos == 0:
			self.shuffled = random.sample(self.elements, len(self.elements))

		v = self.shuffled[self.pos]
		self.pos += 1
		if self.pos == len(self.elements):
			self.pos = 0

		return v


import sys
import os

panOptions = RandomNonRepeat([0.875,0.625,0.375,0.125,-0.125,-0.375,-0.625,-0.875])
workingDir = sys.argv[1]
sampleOptions = RandomNonRepeat(os.listdir(os.path.join(workingDir, "stems")))
secondsPerBeat = 1.0 / (60 * float(sys.argv[2]))
durationSecs = int(sys.argv[3])

timeElapsed = 0.0

while timeElapsed < durationSecs:
	timeIncr = 1.5
	print("%08.4f,%.3f,%s" % (timeElapsed, panOptions.next(), sampleOptions.next()))
	timeElapsed += timeIncr





