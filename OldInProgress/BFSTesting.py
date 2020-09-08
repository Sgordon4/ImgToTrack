import sys
import skimage
from skimage import io, filters, feature
import numpy as np
import math
import scipy
from scipy import spatial  #For cKDTree

import time

from collections import deque 




# To store image pixel cordinates 
class Point: 
	def __init__(self, r: int, c: int): 
		self.r = r	#Row
		self.c = c 	#Col


class Node:
	def __init__(self, pt: Point):
		self.pt = pt				#The point in the image this represents
		self.children = []			#Points that followed this one in BFS
		
		#The depth of the child farthest away
		#from root that this node is a parent of
		self.maxChildDepth = -1
		
		
	def __str__(self, level=0):
		#ret = "\t"*level+repr(self.value)+"\n"
		ret = ": "*level+"({}, {}) {}".format(self.pt.r, self.pt.c, self.maxChildDepth)+"\n"
		for child in self.children:
			ret += child.__str__(level+1)
		return ret



#Is this point in bounds
def inBounds(row: int, col: int, ROW: int, COL: int):
	return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL) 


# These arrays are used to get row and column  
# numbers of 8 neighbours of a given cell  
ROWDELTA = [-1, -1, -1,
			 0,      0,
			 1,  1,  1]
COLDELTA = [-1,  0,  1,
			-1,      1,
			-1,  0,  1]

#Final track
TRACK = []

#------------------------------------------------------------------------------


def BFS(img, start: Point):
	
	ROW = len(img)
	COL = len(img[0])
	
	visited = [[False for i in range(COL)] for j in range(ROW)] 
	
	#Mark the start pixel as visited
	visited[start.r][start.c] = True
	
	#Create a queue to hold points to be visited
	q = deque()
	
	node = Node(start)
	
	#Enqueue and set this node to the root of our BFS result tree
	q.append(node)
	root = node
	
	
	#While the queue still has more nodes...
	while q:
		#Dequeue the next point
		curr = q.popleft()
		
		#Enqueue the adjacent points
		for i in range(8):
			#Calculate the coordinates of the next point
			row = curr.pt.r + ROWDELTA[i]
			col = curr.pt.c + COLDELTA[i]
			
			
			#If this point is in bounds, is a valid edge,
			#and hasn't been visited yet...
			if(inBounds(row, col, ROW, COL) and (img[row][col] > 0) and (not visited[row][col])):
				visited[row][col] = True
				adjPoint = Node(Point(row, col))
				
				#Enqueue it and add it to the tree
				q.append(adjPoint)
				curr.children.append(adjPoint)
	
	
	return root


#------------------------------------------------------------------------------

#DFS to sort tree
def SortTree(node: Node):
	children = node.children
	
	if(len(children) == 0):
		node.maxChildDepth = 0
		return 1
	
	
	maxDepth = 0
	
	for child in children:
		depth = SortTree(child)
		maxDepth = max(depth, maxDepth)
		
		
	node.maxChildDepth = maxDepth
	
	#Sort the list in order of maxChildDepth
	node.children = sorted(children, key=lambda child: child.maxChildDepth)
	
	return maxDepth+1
	

#------------------------------------------------------------------------------

#Run through the tree and output it to a txt file
def TreeToTrack(node: Node, rootDepth: int, depth: int=0):
	children = node.children
	
	ret = ": "*depth+"({}, {})".format(node.pt.r, node.pt.c)+"\n"
	print(ret, end="")
	TRACK.append("[{}, {}] ".format(node.pt.r, node.pt.c))
	
	maxDepthReached = depth
	
	for child in children:
		childDepth = TreeToTrack(child, rootDepth, depth+1)
		maxDepthReached = max(childDepth, maxDepthReached)
	
	if(len(children) > 0 and rootDepth != maxDepthReached):
		print(ret, end="")
		TRACK.append("[{}, {}] ".format(node.pt.r, node.pt.c))
	
	return maxDepthReached
	


#------------------------------------------------------------------------------
	
	
def main():
	mat =  [[ 1, 0, 1, 1, 1, 1, 0, 1, 1, 1 ],
			[ 1, 0, 1, 0, 1, 1, 1, 0, 1, 1 ],
			[ 1, 1, 1, 0, 1, 1, 0, 1, 0, 1 ],
			[ 0, 0, 0, 0, 1, 0, 0, 0, 0, 1 ],
			[ 1, 1, 1, 0, 1, 1, 1, 0, 1, 0 ],
			[ 1, 0, 1, 1, 1, 1, 0, 1, 0, 0 ],
			[ 1, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
			[ 1, 0, 1, 1, 1, 1, 0, 1, 1, 1 ],
			[ 1, 1, 0, 0, 0, 0, 1, 0, 0, 1 ]]
	source = Point(0,0)
	
	
	
	startTime = time.time()
	
	tree = BFS(mat, source)
	
	endTime = time.time()
	print("BFS Runtime:",endTime-startTime)
	
	
	startTime = time.time()
	
	depth = SortTree(tree)
	
	endTime = time.time()
	print("SortTree Runtime:",endTime-startTime)
	
	
	
	print(depth)
	print()
	
	for col in mat:
		print(col)
	print()
	print(tree)
	
	TreeToTrack(tree, tree.maxChildDepth)
	
	print(TRACK)
	
	#Write results to file
	filehandle = open("track.txt", "w")
	filehandle.writelines(TRACK)
	filehandle.close()
	
main()
