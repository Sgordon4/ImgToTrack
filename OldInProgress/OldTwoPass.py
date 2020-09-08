import sys
import skimage
from skimage import io, filters, feature
import numpy as np


'''
This program uses the Hoshen–Kopelman algorithm to connect all adjacent 
components considering 8 neighbors.
The binary image produced by ImgToEdges is already padded by 1 pixel around
the edges, so we need not do it again.
'''



#------------------------------------------------------------------------------
# Make the first pass

edges = skimage.io.imread(fname="edges.png")

print(len(edges))
print(len(edges[0]))

#Current tag to assign
current = 1

#Dictionary for equivalent tags
tagDict = dict()


for row in range(1, len(edges)):
	for col in range(1, len(edges[0])):
		
		#If this is an edge pixel...
		if(edges[row][col] == 255):
			
			#												234
			#Grab the surrounding pixels					1X_
			#We only check the top right 4 for efficiency:	___
			neighbors = [edges[row][col-1], edges[row-1][col-1],
                		 edges[row-1][col], edges[row-1][col+1]]
			
			#If array is all zero (No edge pixels)...
			if(np.count_nonzero(neighbors) == 0):
				#We have a new component
				edges[row][col] = current
				current += 1
				
			
			#If array only has one non-zero (One edge pixel)...
			elif(np.count_nonzero(neighbors) == 1):
				index = np.nonzero(neighbors)[0][0]
				edges[row][col] = neighbors[index]
				
			
			#If there are more than one non-zero (Multiple edge pixel)...
			else:
				#Find the non-zero elements
				nonZero = list(filter(lambda x: x > 0, neighbors))
				m = min(nonZero)
				
				#Set the current pixel to the minimum
				edges[row][col] = m
				
				#Record equivalent tags: _ _ 1 _ _ 2	=>  1 -> 3
				#						 _ 3 3 _ 4 _ 		2 -> 4
				for tag in nonZero:
					
					if(tag == m):
						continue
						
					#If the tag is not already in the dictionary...
					if(m not in tagDict):
						tagDict[m] = set([tag])
						
					else:
						tagDict[m].add(tag)


#------------------------------------------------------------------------------
# Consolidate the dictionary so that no key is a value and no value is a key
# This is a form of union-find
io.imsave(fname='passed.png', arr=skimage.img_as_int(edges))
	
keyyy = sorted(tagDict.keys())
for key in keyyy:
	#Grab the set of equivalence values this key contains
	s = tagDict[key]
	print(key,":",s)



print("\n")
print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")
print("\n")
DEBUG = False

keys = tagDict.keys()

for key in keys:
	#Grab the set of equivalence values this key contains
	s = list(tagDict[key])
	
	
	if(DEBUG):
		print()
		print(key,":",s)
		print("-------------")
	
	#Start at the beginning of the set
	index = 0
	
	#Loop over the set...
	while index < len(s):
		#Pull out a value
		val = s[index]

		#If this value is a key too...
		if(val in tagDict):
			#Grab the set from that
			set2 = tagDict[val]
			if(DEBUG):
				print(key,"-",val,":",set2, end='')
			
			#Remove duplicates
			set2.difference_update(s)
			#And remove our current key if it exists in this new set
			set2.discard(key)
			
			#Tack this set onto the end of our list
			s = s + list(set2)
			if(DEBUG):
				print(" => ",s)
			
			#Replace the second set with our origional key
			tagDict[val] = set([key])
			if(DEBUG):
				print(val,"==",key)
		
		
		index += 1


	#Update the dictionary
	tagDict[key] = set(s)
	
	
	
	
#Turn the set into an array to loop through it and such, and when adding new
#sets, use a difference update then tack it onto the array


#Keep long ass lists, but when looking through later,
# assume any set len()>1 is empty

	
print("\n")
print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")
print("\n")
	
	
for key in tagDict.keys():
	#Grab the set of equivalence values this key contains
	s = tagDict[key]
	print(key,":",s)