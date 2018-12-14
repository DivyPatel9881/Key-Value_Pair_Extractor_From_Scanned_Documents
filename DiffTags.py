'''
	For single file extraction process only. 

	To be executed after the OCREngine.py

	The command for exceution.

	python DiffTags.py test.txt SetA.txt Period[\'\',\'\']w Interest[\'\',\'\']f

	 python3 DiffTags.py test.txt SetA.txt Period[\'\',\'herein.^l\']f Attaching_To_Delegated_Underwriting_Contract_Number[\'\',\'\']w Unique_Market_Reference[\'\',\'\']w Insured[\'\',\'and/or^s\']w Type[\'\',\'\']w Interest[\'consisting^s\',\'handled^l\']f 

'''
import sys
from EntityExtractor import EntityEx
import spacy
from spacy import displacy
from collections import Counter
from pprint import pprint
import en_core_web_sm

def Lookup (filename , string):
	fread=open(filename,'r')
	l = fread.readlines()
	d = dict()
	for s in l:
		s=s.strip('\n')
		index = string.find(s)
		if index!=-1:
			d[s]=index
	return d

file_txt = sys.argv[1]
fread =  open(file_txt,'r')
final_txt = fread.readline() 
indexd = file_txt.find('.')
o = file_txt[:indexd]

lookup = Lookup(sys.argv[2] , final_txt)

Index = []
for index in lookup:
	Index.append(lookup[index])

Index.sort()
Index.append(-1)

nlp = en_core_web_sm.load()

length = len(sys.argv)

fwrite = open('Res_'+o+".csv",'w')

for i in range(3,length):
	index = sys.argv[i].find('[')
	s1 = sys.argv[i][:index]
	s2 = sys.argv[i][index:-1]
	s4 = sys.argv[i][-1:]
	s3 = s1.replace('_',' ')
	s3=s3+":"
	l = []
	l.append(s1)
	if s3 in lookup.keys():
		start = lookup[s3]
		end = Index[Index.index(start)+1]
		param = final_txt[start:end]
		fwrite1 = open(s1+'.txt','w')
		fwrite1.write(param)
		ExResult = EntityEx(param,s2)
		inc = ExResult.find(':')
		ExResult = ExResult[inc+2:]
		if s4=='f':
			doc = nlp(ExResult)
			for X in doc.ents:
				l.append(X.text)
			file_cont = ",".join(l)
		elif s4=='w':
			file_cont = s1 + "," + ExResult
		print(file_cont)
		fwrite.write(file_cont+"\n")

print('Done')
