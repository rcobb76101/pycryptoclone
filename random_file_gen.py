import os
import random
import uuid

base_path = 'C:/Users/robertl'

locations = [
    '/Desktop/',
    '/Downloads/',
    '/Documents/'
]

doc_types = [
    ('document_', '.docx'),
    ('presentation_', '.pptx'),
    ('spreadsheet_', '.xlsx')
]

for location in locations:
    directory = base_path + location
    for prefix, extension in doc_types:
        number_of_docs = random.randint(25,50)
        for i in range(number_of_docs):
            doc_uuid = str(uuid.uuid1())
            doc_name = directory + prefix + doc_uuid + extension
            file_size = random.randint(1, 2048 * 1024)
            with open(doc_name, 'w') as output_file:
                output_file.write('UNENCRYPTED' * file_size)