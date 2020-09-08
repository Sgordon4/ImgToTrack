import sys
import skimage
from skimage import io, filters, feature

'''
This program takes the binary image output by ImgToEdges.py
It then loops through and connects white pixels to other nearby
white pixels based on surrounding pixel density, with low density
allowing farther reach
255 - True/White, 0 - False/Black
'''

edges = skimage.io.imread(fname='edges.png')
print(edges[2][75])

RADIUS = 2		#RADIUS of sliding window, excluding the center point
CENT = (0,0)	#Tuple representing current center point of sliding window


#------------------------------------------------------------------------------
#Find surrounding pixel density

#Loop through entire image
for x in range (0, len(edges)):
	print('\n')
	for y in range (0, len(edges[0])):
		

		#If this pixel is not an edge...
		if(edges[x][y] == 0):
			#print('-', end = '')
			continue
			
		#Apply sliding window
		numChecked = 0		#Count of the non out-of-bounds pixels read
		numEdges = 0		#Count of edges found when scanning

		for i in range (x - RADIUS, x + RADIUS):
			for j in range (y - RADIUS, y + RADIUS):
				
				#If we are not out of bounds...
				if(i >= 0 and j >= 0):
					numChecked+=1
					
					#If the current pixel is white
					if(edges[i][j] == 255):
						numEdges+=1

		#Remove the center pixel
		numEdges-=1
		numChecked-=1
		
		ratio = numEdges/numChecked
		#print(numChecked, ":", numEdges, end = '')
		print(int(ratio*10), "", end = '')





