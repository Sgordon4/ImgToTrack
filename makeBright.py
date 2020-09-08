import sys
import skimage
from skimage import io, filters, feature
import numpy as np
import math


dark = skimage.io.imread(fname="final.png", as_gray=True)

for row in range(len(dark)):
	for col in range(len(dark[0])):
		if (dark[row][col] > 0):
			dark[row][col] = 255

io.imsave(fname='finalBright.png', arr=skimage.img_as_int(dark))