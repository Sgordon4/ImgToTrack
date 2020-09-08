import sys
import skimage
from skimage import io, filters, feature
import numpy as np
import math
import scipy
from scipy import spatial  #For cKDTree

import time


DEBUG = False
DEBUG2 = False
totalStartTime = time.time()

edges = skimage.io.imread(fname="edges.png", as_gray=True)
map = np.zeros(shape=(len(edges),len(edges[0]))).astype(int)

#Current group ID number
segment = 1

#Dictionary for equivalent tags
tags = dict()


#------------------------------------------------------------------------------
# Given a binary image, make a map that assigns each edge (non-0) pixel
#  to a 'connected component' #, linking adjacent pixels as a component
#
# Create a dictionary to keep track of which resulting edge component #s
#  are equivalent, e.g.   1 and 3   or   2 and 4   in the example below
'''
. . . . . . . .			. . . . . . . .
. 1 . . . . 1 .			. 1 . . . . 2 .
. 1 . 1 1 . 1 .   ..\	. 1 . 3 3 . 2 .
. . 1 . . . 1 .   ''/	. . 1 . . . 2 .
. . . . 1 1 . .			. . . . 4 2 . .
. . . . . . . .			. . . . . . . .
'''


startTime = time.time()


##    TODO   update the comments in between lines here to increase readability

#For every pixel...
for row in range(1, len(map)-1):
	for col in range(1, len(map[0])-1):
		
		#If this is an edge pixel
		if(edges[row][col] != 0):
			#														1 2 3
			#Check surrounding 8 pixels for already found (non-0)	4 X .
			#pixels, disregard bottom right 4 for efficiency		. . .
			neighbors = [map[row-1][col-1], map[row-1][col  ], map[row-1][col+1], 
						 map[row  ][col-1]]
			
			
			for pix in neighbors:
				if(pix != 0):
					
					#If we haven't already found a value...
					if(map[row][col] == 0):
						map[row][col] = pix
					
					#If this pix value isn't a duplicate, record it
					elif(pix != map[row][col]):
						tags[ map[row][col] ].add(pix)
						
			
			#If there was no non-zero pixel in neighbors...
			if(map[row][col] == 0):
				map[row][col] = segment
				segment += 1
			
			#If this key doesn't yet exist...
			if(map[row][col] not in tags):
				tags[ map[row][col] ] = set()


endTime = time.time()
print("Connected component assignment:",endTime-startTime)
#------------------------------------------------------------------------------


if(DEBUG):
	#Print the dictionary
	for tag in tags:
	    print (tag,":",tags[tag])


#------------------------------------------------------------------------------
# Taking the dictionary created in the last step, consolidate it so that all
#  equivalent #s point to a single parent #
'''
. . . . . . . .			. . . . . . . .		 ...
. 1 . . . . 2 .			. 3 . . . . 4 .		1: {3}
. 1 . 3 3 . 2 .   ..\	. 3 . 3 3 . 4 .		2: {4}
. . 1 . . . 2 .   ''/	. . 3 . . . 4 .		3: { }
. . . . 4 2 . .			. . . . 4 4 . .		4: { }
. . . . . . . .			. . . . . . . .		 ...

This example is different than the one used throughout this file

1: {2, 5}		6: { }			1: {9}		6: { }
2: {3}			7: {8}	  ..\   2: {9}		7: {9}
3: { }			8: {9}	  ''/	3: {9}		8: {9}
4: { }			9: { }			4: { }		9: {1, 2, 3, 5, 7, 8}
5: {7}			 ...			5: {9}		 ...

'''
startTime = time.time()


#For every component #...
for compNum in tags:
	
	#Grab the list of numbers this compNum is equivalent to
	lst = list(tags[compNum])
	
	index = 0
	while index < len(lst):
		#For every number this compNum is equivalent to...
		equiv = lst[index]
		
		#Grab the list of numbers THAT is equivalent to
		children = tags[equiv]
		
		#Remove compNum if it exists in this set (we don't want 2 -> 2, ...)
		children.discard(compNum)
		#And add the set to the current running list, minus duplicates
		children.difference_update(lst)
		lst = lst + list(children)
		
		#Point the child # to only this compNum
		tags[equiv] = set([compNum])
		
		index += 1
	
	#Finally, update this compNum in the dictionary with the new extended list
	tags[compNum] = set(lst)


endTime = time.time()
print("Connected component consolidation:",endTime-startTime)
#------------------------------------------------------------------------------

if(DEBUG):
	print("\n")

	for tag in tags:
	    print (tag,":",tags[tag])


	if(True):
		#Print the old map
		for row in range(0, len(map)):
			print()
			for col in range(0, len(map[0])):
				if(map[row][col] != 0):
					print("{:^3}".format(map[row][col]), end="")
				else:
					print("-|-", end="")

	print("\n")

	for tag in tags:
	    print (tag,":",tags[tag])
		
	print("\n")

	if(True):
		#Print the new map
		for row in range(0, len(map)):
			print()
			
			for col in range(0, len(map[0])):
				
				if(map[row][col] != 0):
					
					key = map[row][col]
					s = tags[key]
					if (len(s) != 0):
						
						arbitratryVal = next(iter( tags[key] ))
						if (key < arbitratryVal):
							key = arbitratryVal
					
					print("{:^3}".format(key), end="")
				else:
					print("-|-", end="")

	print("\n")


#------------------------------------------------------------------------------
# For ease of use and readability, trim the dictionary so that 
#  parent component #s always point to an empty set
#
# This can easily be combined with the step below for a slight increase in
#  efficiency, but is made separate for readability
#
# A parent component # will always point to either:
#  - An empty set
#  - A list of child component #s, all of which will be < parent
'''

1: {9}		6: { }						  1: {9}		6: { }
2: {9}		7: {9}					..\   2: {9}		7: {9}
3: {9}		8: {9}					''/	  3: {9}		8: {9}
4: { }		9: {1, 2, 3, 5, 7, 8}		  4: { }		9: { }
5: {9}		 ...						  5: {9}		 ...
 
'''

startTime = time.time()

for key in tags:
	if (len( tags[key] ) > 0):
		if (key > next(iter( tags[key] ))):
			tags[key] = set()


if (DEBUG):
	for tag in tags:
	    print (tag,":",tags[tag])
		
	print("\n")

endTime = time.time()
print("Connected component dictionary trimming:",endTime-startTime)
#------------------------------------------------------------------------------
# Make a list of all coordinates per component
'''
. . . . . . . .			...
. 3 . . . . 4 .			...
. 3 . 3 3 . 4 .   ..\	3: (1,1), (2,1), (2,3), (2,4), (3,2)
. . 3 . . . 4 .   ''/	4: (1,6), (2,6), (3,6), (4,4), (4,5)
. . . . 4 4 . .			...
. . . . . . . .			...
'''

startTime = time.time()


#Create a new dictionary
components = dict()

for row in range(0, len(map)):
	for col in range(0, len(map[0])):
		
		#If this pixel is part of a component...
		if(map[row][col] != 0):
			
			#Use the tag dictionary to find if this is a parent component #.
			#If it is a child #, we need to find the parent #.
			key = map[row][col]
			s = tags[key]
			
			
			# The step above can be inserted here for efficiency
			
			#If this component points to an empty set, it is a parent
			if (len(s) != 0):
				#Grab the parent #
				key = next(iter( s ))
			
			
			#Add this coordinate to the dictionary
			coord = (row, col)
			
			if(key in components):
				components[key].append([row, col])
			else:
				components.setdefault(key, [[row, col]])




if (DEBUG):			
	for comp in components:
	    print (comp,":",len(components[comp]),":",components[comp])
	print("\n")
	

if (DEBUG2):			
	for comp in components:
	    print(comp, np.array(components[comp]))
	print("\n")


endTime = time.time()
print("Coordinates per connected component:",endTime-startTime)

	
#------------------------------------------------------------------------------
# Using the list of coordinates per component created above, build individual 
#  2d-trees (kd-tree) for each component to speed up nearest-neighbor searches

startTime = time.time()


trees = dict()
for comp in components:
	trees[comp] = spatial.cKDTree(components[comp])
	
	
endTime = time.time()
print("Building KDTrees:",endTime-startTime)


#------------------------------------------------------------------------------
# Build an adjacency matrix between all components, using the shortest
#  distance between two respective components as an edge
#
# Could also weight the cost based on whether the start and end points are 
#  a line segment end or not here
# This would likely require redefining euclideanDistance, as that is what
#  cKDTree uses to determine distance
# Example: http://code.activestate.com/recipes/578434-a-simple-kd-tree-example-with-custom-euclidean-dis/
'''												  _______3__________ ...
3: (1,1), (2,1), (2,3), (2,4), (3,2)	..\		4| [(2,4), (2,6), 2]
4: (1,6), (2,6), (3,6), (4,4), (4,5)	''/		5| [(2,4), (2,9), 5]
5: (2,9), (3,9)								  ...|	Start   End  Dist
'''

startTime = time.time()


size = len(trees.keys())
adjacency = np.zeros(shape=(size, size)).astype(tuple)

i, j = 0, 0
comps = list(components.keys())


#For every component
for i, startingComp in enumerate(comps):
	coords = components[startingComp]
	#print("Querying from component", startingComp)
	
	#Find closest points between this component and    lst: 1, *3*, 7, 11, 9, 2
	#those components ahead of it in the list					  | ->
	for j in range(i+1, len(comps)):
		endingComp = comps[j]
		tree = trees[endingComp]
		
		#Query tree with each point from startingComp
		distances, indices = tree.query(coords, k=1)
		
		#Find the index of the shortest distance
		minDistanceIndex = np.argmin(distances)
		minDistance = distances[minDistanceIndex]
		
		#Find the respective points
		start = coords[minDistanceIndex]
		end = tree.data[ indices[minDistanceIndex] ].astype(int)
		
		
		#Add these points to the adjacency list
		adjacency[i][j]= adjacency[j][i]= (tuple(start),tuple(end),minDistance)




endTime = time.time()
print("Adjacency matrix creation:",endTime-startTime)


#------------------------------------------------------------------------------
# Using the adjacency matrix from the last step, create a minimum spanning 
#  tree with distance as the edge cost
#
# The below is Prim's algorithm

startTime = time.time()


numVertices = len(adjacency)
visited = [False] * numVertices
numEdges = 0

#List to store the MST
MST = []


#Set the first vertex to 'visited'
visited[0] = True

while (numEdges < numVertices - 1):
	min = sys.maxsize
	x = 0
	y = 0
	
	for i in range(numVertices):
		if (visited[i]):
			
			for j in range(numVertices):
				if (not visited[j]):
					if (min > adjacency[i][j][2]):
						min = adjacency[i][j][2]
						x = i
						y = j
	
	
	MST.append(adjacency[x][y])
	visited[y] = True
	numEdges += 1

if (DEBUG):
	print("\n")
	print(visited)
	for edge in MST:
		print(edge)


endTime = time.time()
print("MST creation:",endTime-startTime)
#------------------------------------------------------------------------------
# Using the MST created above, draw lines along the
#  edges between closest points to link components
#
# The below is Bresenham's Line Generation algorithm
'''
. . . . . . . .
. 3 . . . . 4 .
. 3 . 3 3 = 4 .
. . 3 . . . 4 .
. . . . 4 4 . .
. . . . . . . .
'''


startTime = time.time()


for edge in MST:
	#Set up initial conditions
	x1, y1 = edge[0]
	x2, y2 = edge[1]
	dx = x2 - x1
	dy = y2 - y1
	
	#Determine if the line slopes vertically or horizontally
	slopedVertically = abs(dy) > abs(dx)
	
	
	
	#Rotate if vertically sloped
	if (slopedVertically):
		x1, y1 = y1, x1
		x2, y2 = y2, x2
	
	#Swap points to keep things positive
	swapped = False
	if (x1 > x2):
		x1, x2 = x2, x1
		y1, y2 = y2, y1
		swapped = True
	
	
	#Recalculate slopes
	dx = x2 - x1
	dy = y2 - y1
	
	#Calculate error
	error = int(dx / 2)
	ystep = 1 if (y1 < y2) else -1
	
	#Generate points
	y = y1
	for x in range(x1, x2+1):
		
		if (slopedVertically):
			map[y][x] = 255
		else:
			map[x][y] = 255
		
		error -= abs(dy)
		if (error < 0):
			y += ystep
			error += dx
	
	
	
	
endTime = time.time()
print("Bresenham line generation:",endTime-startTime)
#------------------------------------------------------------------------------


totalEndTime = time.time()
print("\n")
print("Total Script Runtime:", totalEndTime - totalStartTime)
print("\n")

io.imsave(fname='final.png', arr=skimage.img_as_int(map))
#Display edges
io.imshow(map)
io.show()



if(False):
	#Print the new map
	for row in range(0, len(map)):
		print()
		
		for col in range(0, len(map[0])):
			
			if(map[row][col] != 0):
				
				print(" O ", end="")
			else:
				#print("-|-", end="")
				print("   ", end="")

print("\n")