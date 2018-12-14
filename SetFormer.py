'''
	This file is used to make the the set files in the Backend.

	Command
	python SetFormer.py Marine.txt Period Unique_Market_Reference

	First is the python file.
	Second is the File in which the Set of entities is to be Formed.
	Rest all After this are the Features.
	Beware of passing the entities which consists of many words.
	Solution is to replace ' ' between them by '_'.
'''
import sys

length = len(sys.argv)

fwrite = open(sys.argv[1],'w')

for i in range(2,length):
	string = sys.argv[i].replace('_',' ')	
	l = string.split(" ")
	i = 0
	for s in l:
		l[i]=s.capitalize()
		i+=1
	string = " ".join(l)
	fwrite.write(string+':\n')

print('Set Created.')
