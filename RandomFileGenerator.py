import os
import random
import uuid
import argparse

def generate_files(output_paths):
    files_created = 0
    
    doc_types = [
        ('document_', '.docx'),
        ('presentation_', '.pptx'),
        ('spreadsheet_', '.xlsx')
    ]

    for location in output_paths:
        for prefix, extension in doc_types:
            number_of_docs = random.randint(15,30)
            for i in range(number_of_docs):
                doc_uuid = str(uuid.uuid1())
                doc_name = os.path.join(os.path.abspath(location), prefix + doc_uuid + extension)
                file_size = random.randint(1, 2048 * 1024)
                with open(doc_name, 'w') as output_file:
                    print('Generating {}'.format(doc_name))
                    files_created += 1
                    output_file.write('UNENCRYPTED' * file_size)
                    
    return files_created
                
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a random number of documents for ransomware encryption demonstrations')
    parser.add_argument('output_paths', help='Directories where randomly generated documents will be created', nargs='+')
    args = parser.parse_args()
    files_created = generate_files(args.output_paths)
    print('Finished - created {} files'.format(files_created))
    
