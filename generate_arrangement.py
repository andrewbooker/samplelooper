#!/usr/bin/env python

import sys
import os

panOptions = [0.875,0.625,0.375,0.125,-0.125,-0.375,-0.625,-0.875]
workingDir = sys.argv[1]
samples = os.listdir(os.path.join(workingDir, "stems"))
secondsPerBeat = 1.0 / (60 * float(sys.argv[2]))
durationSecs = int(sys.argv[3])

timeElapsed = 0.0
sampleIdx = 0
panIdx = 0

arrFile = open(os.path.join(workingDir, "arrangement.txt"), "w+")

while timeElapsed < durationSecs:
	timeIncr = 1.5
	arrFile.write("%08.4f,%.3f,%s\n" % (timeElapsed, panOptions[panIdx], samples[sampleIdx]))
	timeElapsed += timeIncr
	
	panIdx += 1
	if panIdx == len(panOptions):
		panIdx = 0

	sampleIdx += 1
	if sampleIdx == len(samples):
		sampleIdx = 0

arrFile.close()



