#!/usr/bin/env python

import soundfile as sf
import sys
import os
import csv

workingDir = sys.argv[1]
stemsDir = os.path.join(workingDir, "stems")
arrangement = sys.argv[2]
outFn = os.path.join(workingDir, "audio.wav")


class Src():
	def __init__(self, fn, pan, startAt):
		data, sampleRate = sf.read(fn)
		self.data = data
		self.startAt = startAt
		self.endAt = (len(data) / sampleRate) + startAt
		self.pan = pan
		self.pos = 0
		
	def hasData(self):
		return self.pos < len(self.data)
		
	def read(self, n):
		p = self.pos
		self.pos += n
		return self.data[p:(p + n)]
		
		
def addToStereoBuffer(buffer, fromArr, pan, length):
	right = 0.5 * (1.0 + pan)
	left = 1.0 - right
	
	for l in range(length):
		av = fromArr[l]
		bv = buffer[l]
		buffer[l] = [bv[0] + (left * av), bv[1] + (right * av)]
		
srcs = []
with open(arrangement) as csvFile:
	rows = csv.reader(csvFile, delimiter=',')
	for row in rows:
		src = Src(os.path.join(stemsDir, row[2]), float(row[1]), float(row[0]))
		srcs.append(src)
		
events = []
for s in srcs:
	events.append(s.startAt)
	events.append(s.endAt)

events.sort()

base = 0.0
blockLengths = []
for t in events:
	if (t > 0.0) and (t - base > 0.0):
		blockLengths.append(t - base)
		base = t
		

pt = 0.0
sampleRate = 44100
os.remove(outFn)

with sf.SoundFile(outFn, mode="x", samplerate=sampleRate, channels=2, subtype="PCM_16") as outFile:
	for b in blockLengths:
		print("writing to %ss" % (pt + b))
		l = int(b * sampleRate)
		audio = [[0.0, 0.0]] * l
		for src in srcs:
			if pt >= float(src.startAt) and src.hasData():
				addToStereoBuffer(audio, src.read(l), src.pan, l)
		pt += b
		outFile.write(audio)
	

