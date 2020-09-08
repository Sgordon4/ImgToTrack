import sys
import skimage
from skimage import io, filters, feature
import numpy as np
from collections import deque 
import re #Regex

import time



#Super fast 5:30am img plotting thing to test track shit
#Goddamn im tired but im like 2cm away from finishing


edges = skimage.io.imread(fname="edges.png", as_gray=True)
img = np.zeros(shape=(len(edges),len(edges[0]))).astype(int)


with open('track.txt','r') as f:
	for line in f:
		coordinates = re.findall(r'\[(\d+), (\d+)\]', line)
		
		for coord in coordinates:
			x = int(coord[0])
			y = int(coord[1])
			
			img[x][y] = 255
			#print(int(coord[0]), int(coord[1]))

io.imsave(fname='track.png', arr=skimage.img_as_int(img))

