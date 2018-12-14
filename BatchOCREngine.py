'''
	This Single file is for OCR Batch processing of pdfs.
	Its dependency is 'EntityExtractor.py'.(The file should be in its directory)
	To Run the file Command is:-

	python BatchOCREngine.py test.pdf SetA.txt Period[\'\',\'\']w Interest[\'\',\'\']f

	IN THIS test.pdf is the pdf file on which the extraction is to be done.
	SetA.txt is the Set formed by the User by the Python code SetFormer.py
	The format of the rules are:

	<Entity>[\'<start>'\,\'<end>\']<whole or filtered>
	Beware of passing the entities which consists of many words.
	Solution is to replace ' ' between them by '_'.
	
	python3 BatchOCREngine.py test.pdf SetA.txt Period[\'\',\'herein.^l\']f Attaching_To_Delegated_Underwriting_Contract_Number[\'\',\'\']w Unique_Market_Reference[\'\',\'\']w Insured[\'\',\'and/or^s\']w Type[\'\',\'\']w Interest[\'consisting^s\',\'handled^l\']f 

'''
import io
#from PIL import Image
#import pytesseract
#from wand.image import Image as wi
import sys
from EntityExtractor import EntityEx
import spacy
from spacy import displacy
from collections import Counter
from pprint import pprint
import en_core_web_sm

pdf_path = sys.argv[1]

file_ = pdf_path
in1 = file_.find('/')
file_ = file_[in1+1:-1]
in2 = file_.find('.')
file_ = file_[0:in2]
fileocr=file_+'.txt'
'''
print('Preparing for OCR.')

l = []

pdf = wi(filename=pdf_path,resolution=300)
pdfImage=pdf.convert('jpeg')

imageBlobs=[]

for img in pdfImage.sequence:
	imgPage=wi(image=img)
	imageBlobs.append(imgPage.make_blob('jpeg'))

print('Extracting text.')

i=0
for imgBlob in imageBlobs:
	im=Image.open(io.BytesIO(imgBlob))
	text=pytesseract.image_to_string(im,lang='eng',config='-psm 6')
	i+=1	
	print("Page "+str(i)+" Completed.")
	l.append(text)
	
final_l=[]
for string in l:
	string=string.replace('\n',' ')
	string=string.replace('  ',' ')
	final_l.append(string)

final_txt = " ".join(final_l)

print('Text Extraction Completed.')	
'''
fread = open(fileocr,'r')
final_txt = fread.readline()

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

lookup = Lookup(sys.argv[2] , final_txt)

Index = []
for index in lookup:
	Index.append(lookup[index])

Index.sort()
Index.append(-1)

length = len(sys.argv)

nlp = en_core_web_sm.load()

fwrite = open('Res_'+file_+".csv",'w')

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
		ExResult = EntityEx(param,s2)
		inc = ExResult.find(':')
		ExResult = ExResult[inc+2:]
		if s4=='f':
			doc = nlp(ExResult)
			for X in doc.ents:
				l.append(X.text)
			file_cont = ",".join(l)
		elif s4=='w':
			file_cont = s1+","+ExResult
		print(file_cont)
		fwrite.write(file_cont+"\n")

print('Done')
