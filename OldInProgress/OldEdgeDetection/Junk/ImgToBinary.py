import sys
import skimage
from skimage import io, filters, feature
import numpy as np


img = skimage.io.imread(fname="C.png")

myArr = np.empty((len(img),len(img[0])))


threshold = 250 

for row in range(0, len(img)):
	for col in range(0, len(img[0])):
		if(img[row][col][0] < threshold):
			myArr[row][col] == 0
		else:
			myArr[row][col] == 255
			
io.imsave(fname='C2.png', arr=skimage.img_as_int(myArr))
io.imshow(myArr)
io.show()


'''
for row in range(0, len(img)):
	for col in range(0, len(img[0])):
		if(all(i < threshold for i in img[row][col])):
			myArr[row][col] == 0
		else:
			myArr[row][col] == 255
'''