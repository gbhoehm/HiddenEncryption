# Author: Gage Boehm
# Date: 11/20/2019

# Description
# This program is ran once for every new file being encrypted.
# The purpose of this program is to add one 128 bit block of dead text to the users file.
# The reason for this is during the decryption process the very first block is not decrypted.

def BufferBlock(fIn):
    """ Append a buffer block to the file that will be encrypted.
        This is done do to the very first block of the file not be decrypted."""
    bufferB = "                "
    try:
        with open(fIn, "r") as sFile:
            originalLine = sFile.read()
            with open(fIn, "w+") as wsFile:
                wsFile.write(bufferB + originalLine)

        return "g"
    except:
        return "b"
