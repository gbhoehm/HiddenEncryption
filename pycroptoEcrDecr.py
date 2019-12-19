# Author: Gage Boehm
# Date: 11/25/2019

# Description
# This program has two pieces: a file encryption piece and a file decryption piece.
# The encryption and decryption is done with AES in CBC mode from the python library PyCrypto.
# This program is the second step of the encryption phase and the last step of the decryption phase in the main routine.
# The interaction between the file and AES comes from the online written tutorial by Jay Sridar.
# The structure and interaction between this program and the main program was done by the author.
# 
# The key generation function returns the in both numeric list form and ascii value form.
# The key in ascii form is instantly used for the encryption of the file.
# The key in numeric list form is "masked" by KeyModifer.py for long term storage.  
# 
#
# Sridhar, Jay. "Using AES for Encryption and Decryption in Python Pycrypto." Novixys Software 
# Dev Blog, 8 Feb. 2018, https://www.novixys.com/blog/using-aes-encryption-decryption-python-pycrypto/.

import os, random, struct
from Crypto.Cipher import AES
from Crypto import Random


def encrypt(infile, encfile, sz, key):
    """ With AES encryption in CBC mode, encrypt the provided file.
    
    Steps:
    1) Setup AES for encryption:
        - Initialize AES with a 16 ascii character initialization vector and the provided key
        
    2) Encrypt the provided file:
        - Open the provided text file and create the cipher file.
        - Read the clean text file in blocks on size sz
            - test that the size of the block read in is a multiple of 16, pad with white space otherwise
        - Encrypt the block and write the cipher text to the cipher file 
        """

    # 1)
    # ---------------------------------------------------------------------------------------------
    iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])
    aes = AES.new(key, AES.MODE_CBC, iv)

    # 2)
    # ---------------------------------------------------------------------------------------------

    # Both files must be in byte read/write mode
    with open(encfile, 'wb') as fout:
        with open(infile, "rb") as fin:
            while True:
                
                # Read in one block of data from the text file at a time
                # This is not the AES encryption block size, but the size of block that will be encrypted
                # We break the file read into blocks as AES encryption requires each block being encrypted to be a multiple of 16
                data = fin.read(sz)
                n = len(data)
                if n == 0:
                    break
                elif n % 16 != 0:
                    data += ' ' * (16 - n % 16) # <- padded the block with spaces to by 16 chars
                
                encd = aes.encrypt(data)
                fout.write(encd)

    fout.close()
    fin.close()


def decrypt(encfile, verfile, key, sz, fsz):
    """ Decrypted the given cipher file using AES in CBC mode.
    
    Steps:
    1) Set up AES for decryption:
        - Open provided cipher file and pull the initialization vector from the start of the first line. 
        - Then initialize AES in CBC mode with the IV pulled from the file.
    
    2) Decrypt the Provided cipher file:
        - Create and open a clean text file. 
        - Then read in the cipher text in blocks of size sz:
            - Decrypt each block
            - Write the clean text into the the created file
        - Remove the padding from the last deciphered block based on the original clean text file size.
    """

    # 1)
    # ---------------------------------------------------------------------------------------------

    # Open the cipher file in byte read mode, byte read/write mode is crucial to the functionality of the AES library
    with open(encfile, "rb") as fin:
        iv = fin.read(16)
        aes = AES.new(key, AES.MODE_CBC, iv)

        # 2)
        # ---------------------------------------------------------------------------------------------
        with open(verfile, 'wb') as fout:
            while True:
                data = fin.read(sz)
                n = len(data)
                if n == 0:
                    break
                decd = aes.decrypt(data)
                n = len(decd)
                if fsz > n:
                    fout.write(decd)
                else:
                    fout.write(decd[:fsz]) # <- remove padding on last block
                fsz -= n
    fout.close()
    fin.close()


def generateKey():
    """ Generate a key and the numeric list that represents the key generated
    
    The key representation is keySeed
    The key itself is the elements of the randomly generated list of ascii values
    """

    key1 = [i for i in os.urandom(16)]
    keySeed = [ord(key1[i]) for i in range(16)]
    key = ''
    for i in range (16):
        key += key1[i]
    return key, keySeed
