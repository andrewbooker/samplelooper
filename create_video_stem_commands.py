#!/usr/bin/env python

import sys
import os
import csv

workingDir = sys.argv[1]
arrangement = os.path.join(workingDir, sys.argv[2])
videoFile = os.path.join(workingDir, sys.argv[3])
startOffset = float(sys.argv[4])
ffmpeg = sys.argv[5]
sideLength = int(sys.argv[6])
startW = int(sys.argv[7])


uniqueSamples = []
with open(os.path.join(workingDir, "video_arrangement.txt"), "w+") as arrFile:
	with open(arrangement) as csvFile:
		rows = csv.reader(csvFile, delimiter=',')
		for row in rows:
			#031.5000,-0.375,mono1_007.5000_01.50_8.wav
			stem = row[2].split("_")
			sample = tuple(stem[1:3])
			if sample not in uniqueSamples:
				uniqueSamples.append(sample)
				
			src = "stem_%d.avi" % uniqueSamples.index(sample)
			start = row[0]
			pan = row[1]
			repetitions = int(stem[3].split(".")[0])
			
			arrFile.write("%s,%s,%s,%s,%d\n" % (os.path.join(workingDir, "avi", src), start, stem[2], pan, repetitions))


for i in range(len(uniqueSamples)):
	s = uniqueSamples[i]
	src = "stem_%d.avi" % i
	outFn = (os.path.join(workingDir, "avi", src))
	print("%s -i %s -ss %f -t %s -an -b:v 40M -c:v mpeg4 -vtag XVID -vf \"scale=-1:%d, crop=%d:%d:%d:0\" -y %s" % (ffmpeg, videoFile, startOffset + float(s[0]), s[1], sideLength, sideLength, sideLength, startW, outFn))


