#!/usr/bin/env python

import soundfile as sf
import sys
import os
from math import floor

if len(sys.argv) < 4:
	print("./generate_pool.py <dir> <source file> <tempo> <beats per sample>")
	print("eg ./generate_pool.py /samples input.wav 120 4")
	exit()

workingDir = sys.argv[1]
srcFn = os.path.join(workingDir, sys.argv[2])
if not os.path.isfile(srcFn):
	print("source file '%s' not found" % srcFn)
	exit()

secsPerBeat = 60.0 / int(sys.argv[3])
beats = int(sys.argv[4])

data, sampleRate = sf.read(srcFn)
sampleLength = int(floor(sampleRate * beats * secsPerBeat))

for i in range(1):
	fnOut = os.path.join(workingDir, "pool\\loop_%.3d.wav" % i)
	print("generating %s" % fnOut)
	with sf.SoundFile(fnOut, mode="x", samplerate=sampleRate, channels=1, subtype="PCM_24") as outFile:
		outFile.write(data[:sampleLength])
		

print("done")


