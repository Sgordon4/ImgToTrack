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
		self.pt = pt		#The point in the image this represents
		self.children = []	#Points that followed this one in BFS
		self.depth = -1		#Depth of this node in the tree	
		self.farthestLeaf = -1	#Distance to farthest leaf node from this node
		self.parent = None
	
	
	def __str__(self):
		ret = "({}, {})".format(self.pt.r, self.pt.c)
		return ret
		
	def brack(self):
		ret = "[{}, {}]".format(self.pt.r, self.pt.c)
		return ret
		
		
	def __repr__(self, depth=0):
		ret = ": "*depth+"({}, {}) {}".format(self.pt.r, self.pt.c, self.farthestLeaf)+"\n"
		for child in self.children:
			ret += child.__repr__(depth+1)
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
	root.depth = 0
	
	#Keep track of the maximum depth
	maxDepth = 0


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
				adjPoint.depth = curr.depth+1	#Update our depth
				
				maxDepth = max(maxDepth, adjPoint.depth)
				
				#Enqueue it and add it to the tree
				q.append(adjPoint)
				curr.children.append(adjPoint)
				adjPoint.parent = curr
	
	
	return root, maxDepth


#------------------------------------------------------------------------------

#Perform a postorder traversal, record farthest child depth and 
# sort node children on that rather than printing 
def Postorder(root: Node):
	#Create stacks for postorder traversal
	stack = [] 
	stack2 = []
	
	#Add the root node to the stack
	stack.append(root) 
	
	while(len(stack)): 
		#Pop the next node
		curr = stack.pop()
		stack2.append(curr)
		children = curr.children
		
		for child in children:
			stack.append(child)
	
	return stack2


#------------------------------------------------------------------------------


def SortTree(stack: list): 
	#Stack holds the postorder traversal of our tree
	stack.reverse()
	
	for node in stack:
		if (len(node.children) == 0):
			node.farthestLeaf = 0
		
		node.children = sorted(node.children, key=lambda child: child.farthestLeaf, reverse=True)
		
		parent = node.parent
		
		#If this is the root node, we're done
		if (node.parent == None):
			return
		
		parent.farthestLeaf = max(node.farthestLeaf + 1, parent.farthestLeaf)


#------------------------------------------------------------------------------


# This method may produce more appealing results with the use of two stacks, 
#  one for parents and one for children, to remove this bobbing effect:
#(0, 0)
#: (1, 0)
#: : (2, 0)
#: (1, 0)
#: : (2, 1)
#: : : (2, 2)
#: : (2, 1)
#: : : (1, 2)
#
# Also, this needs to be fixed, as the conditions for return are if the parent
#  node has no more children and was the parent of a node at maxDepth
# There is a chance that two lines are equally long and end at maxDepth, and
#  as such only one of them will be printed, potentially causing MAJOR issues



def TreeToTrack(root: Node, maxDepth: int):
	stack = []
	stack.append(root)
	
	while(len(stack)):
		curr = stack[len(stack)-1]
		children = curr.children
		
		ret = ": "*(len(stack)-1)+"{}".format(curr)
		TRACK.append(Node.brack(curr))
		
		#If this node has more children...
		if (len(children) > 0):
			#Move the last child to the stack
			stack.append(children.pop())
		
		else: #Remove it
			stack.pop()
			#If this is the parent of the last node(s), end
			if (curr.depth == maxDepth-1):
				return
		
		#And print it
		#print(ret)
	


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
	
	tree, maxDepth = BFS(mat, source)
	
	endTime = time.time()
	print("BFS Runtime:",endTime-startTime)
	
	
	startTime = time.time()
	
	stack = Postorder(tree)
	SortTree(stack)
	
	endTime = time.time()
	print("Sort Runtime:",endTime-startTime)
	
	
	startTime = time.time()
	
	TreeToTrack(tree, maxDepth)
	
	endTime = time.time()
	print("Track Runtime:",endTime-startTime)
	
	
	#Write results to file
	filehandle = open("track.txt", "w")
	filehandle.writelines(TRACK)
	filehandle.close()


main()
