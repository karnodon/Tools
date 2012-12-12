import base64
import os
import sys

__author__ = 'Frostbite'
from Crypto.Cipher import AES
padding =  '{'
def pad(s):
    return s + (16 - len(s) % 16) * padding
def unpad(s):
    return s.rstrip(padding)

if len(sys.argv) == 5 and sys.argv[1] == '-k' and sys.argv[3] == '-f':
    filename = sys.argv[4]
    key = sys.argv[2]
    input = open(filename, 'rb').read(os.path.getsize(filename))#read all file
    obj = AES.new(key, AES.MODE_CBC, 'This is an IV456')
    ciphertext = obj.encrypt(pad(input))
    ciphertext = base64.b64encode(ciphertext)
    open(filename+'.enc', 'wb').write(ciphertext)
    obj2 = AES.new(key, AES.MODE_CBC, 'This is an IV456')
    ciphertext = base64.b64decode(ciphertext)
    opentext = unpad(obj2.decrypt(ciphertext))
    open(filename+".new", 'wb').write(opentext)
    if os.path.getsize(filename) == os.path.getsize(filename+'.new'):
        print 'BINGO'
    else:
        print 'SIZES ARE NOT EQUAL, SMTH BAD HAS HAPPENED'
else:
    print 'usage: python crypt.py -k <key> -f <filename>'
