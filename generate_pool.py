#!/usr/bin/env python

import soundfile as sf
import sys
import os

if len(sys.argv) < 5:
	print("./generate_pool.py <dir> <source file> <tempo> <beats per sample> <number of samples>")
	print("eg ./generate_pool.py /samples input.wav 120 4 10")
	exit()

srcFn = os.path.join(sys.argv[1], sys.argv[2])
if not os.path.isfile(srcFn):
	print("source file '%s' not found" % srcFn)
	exit()

print("done")


