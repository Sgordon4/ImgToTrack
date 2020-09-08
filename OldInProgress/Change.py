import sys
import skimage
from skimage import io, filters, feature
import numpy as np


edges = skimage.io.imread(fname="face.png", as_gray=True)

for row in range(0, len(edges)):
	print()
	for col in range(0, len(edges[0])):
		if(edges[row][col] != 0):
			edges[row][col] == 255
			print("255 ", end="")
		else:
			edges[row][col] == 0
			print("0   ", end="")
			
io.imsave(fname='face.png', arr=skimage.img_as_int(edges))

#Display edges
io.imshow(edges)
io.show()