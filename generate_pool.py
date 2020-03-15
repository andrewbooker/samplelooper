#!/usr/bin/env python

import soundfile as sf
import sys
import os
from math import floor
import re

regex = re.compile(r'\d+')


if len(sys.argv) < 6:
	print("./generate_pool.py <dir> <source file> <tempo> <beats per sample> <samples>")
	print("eg ./generate_pool.py /samples input.wav 120 4 6")
	exit()

subDir = "pool"
workingDir = sys.argv[1]

inFileName = sys.argv[2]
srcFn = os.path.join(workingDir, inFileName)
if not os.path.isfile(srcFn):
	print("source file '%s' not found" % srcFn)
	exit()

secsPerBeat = 60.0 / int(sys.argv[3])
beatsPerBar = int(sys.argv[4])
beatsOverlap = 0.05
required = int(sys.argv[5])

data, sampleRate = sf.read(srcFn)
sampleLength = int(floor(sampleRate * (beatsPerBar + beatsOverlap) * secsPerBeat))

for i in range(required):
	startTime = i * beatsPerBar * secsPerBeat
	fnOut = os.path.join(workingDir, "%s\\%s_%08.4f_%05.2f.wav" % (subDir, inFileName.split(".")[0], startTime, beatsPerBar * secsPerBeat))
	startSample = int(floor(sampleRate * startTime))
	print("generating %s" % fnOut)
	with sf.SoundFile(fnOut, mode="x", samplerate=sampleRate, channels=1, subtype="PCM_24") as outFile:
		outFile.write(data[startSample:(sampleLength + startSample)])
		

print("done")


