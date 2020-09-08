keys = tagDict.keys()

for key in keys:
	#Grab the set of equivalence values this key contains
	s = tagDict[key]
	print()
	print(key,":",s)
	print("-------------")
	
	#Start at the beginning of the set
	index = 0
	
	#Loop over the set...
	while len(s) != 0:
		#Pull out a value
		val = s.pop()
		
		#If this value is our current key (2->2)...
		if(key == val):
			print("Skipping...")
			continue
		
		#If this value is a key too...
		if(val in tagDict):
			#Grab the set from that
			set2 = tagDict[val]
			print(val,":",set2, end='')
			
			#Tack this set onto the origional one
			s.update(set2)
			tagDict[key] = s
			print(" => ",s)
			
			#Replace the second set with our origional key
			tagDict[val] = set([key])
	
	
	#If the set is empty, we no longer need the current key. Remove it
	print("Final: ",key,":",s)

	
	
#Turn the set into an array to loop through it and such, and when adding new
#sets, use a difference update then tack it onto the array
	
print("\n")
print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")
print("\n")
	
	
for key in tagDict.keys():
	#Grab the set of equivalence values this key contains
	s = tagDict[key]
	print(key,":",s)
	
	
	
	
	
	
	
	
	
#===============================================================================



keys = tagDict.keys()

for key in keys:
	#Grab the set of equivalence values this key contains
	s = list(tagDict[key])
	print()
	print(key,":",s)
	print("-------------")
	
	#Start at the beginning of the set
	index = 0
	
	#Loop over the set...
	while index <= len(s):
		#Pull out a value
		val = s[index]

		#If this value is a key too...
		if(val in tagDict):
			#Grab the set from that
			set2 = tagDict[val]
			print(val,":",set2, end='')
			
			#Remove duplicates
			set2.difference_update(s)
			#And remove our current key if it exists
			set2.discard(key)
			
			#Tack this set onto the end of our list
			s = s + list(set2)
			
			#Update the dictionary
			tagDict[key] = set(s)
			print(" => ",s)
			
			#Replace the second set with our origional key
			tagDict[val] = set([key])
	
	
	#If the set is empty, we no longer need the current key. Remove it
	print("Final: ",key,":",s)

	
	
#Turn the set into an array to loop through it and such, and when adding new
#sets, use a difference update then tack it onto the array
	
print("\n")
print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")
print("\n")
	
	
for key in tagDict.keys():
	#Grab the set of equivalence values this key contains
	s = tagDict[key]
	print(key,":",s)
	
	
	
	
#==============================================================================

	
	
	
keys = tagDict.keys()

for key in keys:
	#Grab the set of equivalence values this key contains
	s = tagDict[key]
	print()
	print(key,":",s)
	print("-------------")
	
	
	#Loop over the set...
	while len(s) > 0:
		
		#If this key only contains a smaller element,
		# it means it has already been visited
		if(len(s) == 1 and s.pop() < key):
			print("Skipping...")
			break
			
		#Pull out a value
		val = s.pop()
		
		#If this value is a key too...
		if(val in tagDict):
			#Grab the set from that
			set2 = tagDict[val]
			print(val,":",set2, end='')
			
			#Tack this set onto the origional one
			s.update(set2)
			s.discard(key)
			
			#Update the dictionary
			tagDict[key] = s
			print(" => ",s)
			
			#Replace the second set with our origional key
			tagDict[val] = set([key])
			
			
			
#==============================================================================
			
			





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
	
	
	




