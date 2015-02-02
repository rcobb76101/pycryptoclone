import os
import random

document 		= 'document_'
powerpoint 	= 'presentation_'
spreadsheet 	= 'spreadsheet_'

docs 			= [document, powerpoint, spreadsheet]

locations 		= [r'C:\Users\murrysa\Documents', r'C:\Users\murrysa\Desktop', r'K:']

for location in locations:
	for doctype in docs:
		
		if doctype == 'document_':
			extension = '.docx'
		elif doctype == 'presentation_':
			extension = '.pptx'
		elif doctype == 'spreadsheet_':
			extension = '.xlsx'
		else:
			extension = '.txt'
			
		if location == 'K:':
			number_of_docs = random.randint(5000, 10000)
		else:
			number_of_docs = random.randint(25, 50)
		
		for i in range(number_of_docs):
			doc_num = random.randint(1, 100)
			
			doc_name = '{0}{1}{2}'.format(doctype, doc_num, extension)
			doc_name = os.path.join(location, doc_name)
			
			file_size = random.randint(1, 2048 * 1024)
			
			with open(doc_name, 'wb') as file:
				file.write(os.urandom(file_size))
