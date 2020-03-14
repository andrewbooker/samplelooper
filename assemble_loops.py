#!/usr/bin/env python

import soundfile as sf
import sys
import os
import datetime
import time
from math import floor

class Pos():
	def __init__(self):
		self.p = 0
		
	def pos(self):
		self.p += 1
		return self.p


def vol(p, sampleLength, iterations):
	return 1.0 - (p.pos() / (sampleLength * (iterations - 1.0)))
	
	
if len(sys.argv) < 4:
	print("./assemble_loops.py <working dir with pool subdir> <tempo> <iterations>")
	print("eg ./assemble_loops.py /samples 120 10")
	exit()


workingDir = sys.argv[1]
secsPerBeat = 60.0 / int(sys.argv[2])
beatsOverlap = 0.05
iterations = int(sys.argv[3])


inDir = os.path.join(workingDir, "pool")
availableSamples = os.listdir(inDir)

now = time.time()
outFn = os.path.join(workingDir, "%s.wav" % datetime.datetime.fromtimestamp(now).strftime("%Y-%m-%d_%H%M%S"))

pos = Pos()
for f in availableSamples:
	inFile = os.path.join(inDir, f)
	print("found %s" % inFile)
	data, sampleRate = sf.read(inFile)
	overlap = int(floor(sampleRate * beatsOverlap * secsPerBeat))
	
	print("found %d samples expecting %d overlap" % (len(data), overlap))
	print("writing %s" % outFn)
	sampleLength = len(data) - overlap
	
	with sf.SoundFile(outFn, mode="x", samplerate=sampleRate, channels=1, subtype="PCM_16") as outFile:
		for i in range(iterations):
			if i == 0:
				outFile.write(data[:sampleLength])
			else:
				for o in range(overlap):
					coeff = 1.0 * o / overlap
					outFile.write(vol(pos, sampleLength, iterations) * ((coeff * data[o]) + ((1.0 - coeff) * data[sampleLength + o])))
					
				outFile.write([(vol(pos, sampleLength, iterations) * s) for s in data[overlap:sampleLength]])

print("done")


	