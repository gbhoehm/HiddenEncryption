# Author: Gage Boehm
# Date: 12/04/2019

# Description
# Set up an environment for AES and LSB along with the key modification 
# to perform the encryption into an image and decryption out of an image processes.
#
# The main routine in the file asks the user to pick either encryption, decryption, exit, or help.  The main routine is only exited when exit is entered.
# The help option will asks if the user want to display the instruction again or if they want to learn more about an error message. 
# Exit option does exactly what you would expect, exits the software.
# Encryption option will get a clean text file, png file and pin from the user.
#   Generate a key, key seed, and IV.
#   Mask the key seed and run AES encryption with the key and IV on the clean text file.
#   Create an info string that will have the masked key, clean text file length, and cipher file length.
#   Use LSB to encode the cipher text and info string into the provided png file. 
# Decryption option will get a stego image and pin from the user.
#   LSB will be used to decoded the cipher text and info string out of the stego image.
#   Brake the info string back into its components and unmask the key.
#   With the unmasked key and IV from the cipher text use AES to decrypt the text.
   


# Import libraries
from PIL import Image
import Tkinter as tk
import tkFileDialog
import os
import ast

# Import funcationalies
import LSBhinding as LSB
import preFileProcess as appendBuf
import pycroptoEcrDecr as AES
import KeyModifer as keyMod

def Instructions():
    """ Display the instructions to the user """
    print
    print "First please enter one of the following options: "
    print "e) Enter in 'e' if you want to encrypt a text file into an image."
    print "d) Enter in 'd' if you want to decrpt an image to pullout the text file."
    print "h) Enter in 'h' if you needed help with an error message or needed the instructions again."
    print "exit) Enter in 'exit' when you would like to leave the software."
    print
    print
    print "Encryption:"
    print "When encryption is selected a file window will open asking for a .txt file."
    print "Select the text file that you would like to encrypt into an image in this window."
    print "After you select a text file a new window will open asking for a .png file."
    print "Select the image file that you would like the text file to be encrypted into within this window."
    print "Once the two files have been selected you will be promted to enter a 16 charater long pin."
    print "This pin will act as a password to the text file that you have selected to encrypt."
    print "After the pin is entered the software will attempt to encrypt the text file into the image."
    print "It HIGHLY recommend that you try decrypting the image after the encryption process has finshed."
    print
    print
    print "Decryption:"
    print "When decryption is selected a file window will open asking for a .png file."
    print "Select the image file in the window that you would like to decrypt the text out of."
    print "Once the image file is selected you will be promted to enter the 16 charater long pin for the text within the image."
    print "This is the same pin which you entered when you encrypted into the image."
    print "After the pin is entered the software will begain decrypting the image."
    print
    print
    print "Help:"
    print "When you request help you will be asked for one of the two following options:"
    print "i) Enter in 'i' to display these instruction once again."
    print "m) Enter in 'm' to get quick infomation about an error message."
    print
    print "     Error message help:"
    print "     When you enter the error message help section you will be asked for one of the following to options:"
    print "     e) Enter in 'e' if the error message comes from the encryption process."
    print "     d) Enter in 'd' if the error message comes from the decryption process."
    print "     "
    print "     Once one is selected you will be asked for the error message."
    print "     After you enter in the message a short description of what caused the error will be displayed."
    print "     For more infomation about the error and some resolution options check the handbook."
    print
    print

def messageMeaning(errorMessage, phase):
    """ Display the meaning of the provided error message """

    encryptionDic = {"image":"The image chose cannot be opened. ", "text":"The text file could not be open or buffered. ", "keyMask":"Key masking process failed. ", "aes":"AES encryption has failed. ", "lsb":"During the image encoding process an error occurred.", "key":"A check was made to make sure that the text file would be recoverable and a error was encountered during the AES decryption step.", "deCode":"A check was made to make sure that the text file would be recoverable and a general error was encountered."}
    decryptionDic = {"info":"A problem with a file information string was encountered.", "aes":"AES decryption failed. ", "lsb":"During the image decoding phase an error occurred. ", "key":"Key unmasking process failed."}

    if phase == 'e' or phase == 'E':
        if errorMessage in encryptionDic:
            print encryptionDic[errorMessage]
        else:
            print "Invalid error message given"
    elif phase == 'd' or phase == 'D':
        if errorMessage in decryptionDic:
            print decryptionDic[errorMessage]
        else:
            print "Invalid error message given"
    else:
        print "Invalid letter provided"

def helpPromp():
    """ Display either the instructions or the meaning of an enteried error message to the user """
    
    print
    print "Enter 'i' for instructions and 'm' for error message infomation."
    chosen = str(raw_input("> "))
    print
    print

    if chosen == 'i' or chosen == "I":
        Instructions()
    elif chosen == 'm' or chosen == "m":
        print "Enter 'e' if the message comes from the encryption process"
        print "or"
        print "Enter 'd' if the message comes from the decryption process"
        phase = str(raw_input("> "))
        print
        print "Enter the error message"
        message = str(raw_input("> "))
        messageMeaning(message, phase)
    


def ImageInsert(tFileName, iFileName, reRun, pin):
    """ Encrypt the file and then insert the cipher text into the image
    
    Steps:
    1) Validate the image file and buffer the text file.
    2) Generate a key for AES and get a pin from the user, then run the key masking routine on the keySeed
    3) Encrypt the text file with the AES encryption routine
    4) Create an infomation string out of the masked keySeed, original file text file size, and the cipher file size.
    5) Encoded the cipher file and infomation string into the provided image useing LSB
    6) Test the insertion step results in a clean extraction.
    """
    
    # 1)
    # ---------------------------------------------------------------------------------------------------------------------------
    if not reRun:
        # Vaildate the Image file
        try:
            Image.open(iFileName)
        except:
            return 'image', ''

        # Append the buff to the inputted text file
        messageBack = appendBuf.BufferBlock(tFileName)

        # Check if the inputted text file didn't exist and/or there was an error appending the buffer to the text file
        if messageBack == 'b':
            return 'text', ''

    # 2)
    # ---------------------------------------------------------------------------------------------------------------------------

    # Generate a key for the AES encryption
    key, keySeed = AES.generateKey()

    if not reRun:
        print
        print "Enter a 16 character long pin/password for the text being hidden in the image"
    
    invertable = 'f'

    while invertable != 't':
        if not reRun:
            pin = str(raw_input("> "))
            
            if pin == "exit":
                return "exit", ""

            while len(pin) != 16:
                print
                print "Wrong length" 
                print "Please enter a pin that is 16 characters long"
                pin = str(raw_input("> "))

            pin = [ord(pin[i]) for i in range(16)]

        try:
            invertable, storageKey = keyMod.maskKey(keySeed, pin)
        except:
            return "keyMask", ''

    # 3)
    # ---------------------------------------------------------------------------------------------------------------------------

    # Set the size of blocks read from the input file
    # Name the outputted cipher file
    readBlockSize = 2048
    cFileName = tFileName[:-4] + "_cipher" + tFileName[-4:]

    try:
        # Encrypt the user's file
        AES.encrypt(tFileName, cFileName, readBlockSize, key)
    except:
        return "aes", ''

    # 4)
    # ---------------------------------------------------------------------------------------------------------------------------
    fsz = os.path.getsize(cFileName)
    fsz += 100
    text = open(cFileName, "rb").read(fsz)
    info = str(storageKey) + "|" + str(os.path.getsize(tFileName)) + "|" + str(fsz)

    # 5)
    # ---------------------------------------------------------------------------------------------------------------------------
    try:
        messageBack = LSB.encode(iFileName, text, info)
    except:
        return "lsb", ''

    if messageBack == "Completed!":

        # 6)
        # -----------------------------------------------------------------------------------------------------------------------        
        extractMessage = ImageExtract(iFileName, pin, True)
        if extractMessage == "cleared":
            return 'Done', ''
        elif extractMessage == "aes":
            reBuffer = appendBuf.BufferBlock(tFileName)
            return 'key', ''
        else:
            return 'deCode', pin
    else:
        print messageBack
        return 'type', ''


def ImageExtract(iFileName, pin, test):
    """ Pull the cipher text out of the image and then decrypt the file.
    
        Steps:
        1) Decode the image with LSB to pullout the cipher text and infomation string.
        2) Pull apart the infomation string and unmask the keySeed.
        3) Writeout the cipher file and then decrypted the file using the AES decryption routine.
    """


    # 1)
    # ---------------------------------------------------------------------------------------------------------------------------
    try:
        output, info = LSB.decode(iFileName[:-4] + "_encode" + iFileName[-4:])
    except:
        return "lsb"

    # 2)
    # ---------------------------------------------------------------------------------------------------------------------------
    try:
        infoParts = info.split("|")
        storageKey = ast.literal_eval(infoParts[0])
        ogSize = int(infoParts[1])
        fsz = int(infoParts[2])
    except:
        return "info"

    try:
        keySeed = keyMod.unMaskKey(storageKey, pin)
        key = [chr(keySeed[i]) for i in range(16)]
        key = "".join(map(str, key))
    except:
        return "key"

    # 3)
    # ---------------------------------------------------------------------------------------------------------------------------
    try:
        n = len(output)
        testOut = open("1Test.txt", "wb+")
        if fsz > n:
            testOut.write(output)
        else:
            testOut.write(output[:fsz])
        testOut.close()
    except:
        return "file cipher file stetup"

    try:
        outfile = "TextFromImage.txt"
        AES.decrypt("1Test.txt", outfile, key, 2048, ogSize)
    except:
        return "aes"

    if test:
        # Delete the clean textfile as we just wanted to check that the user's file will be recoverable in the future
        if os.path.exists(outfile):
            os.remove(outfile)

    return "cleared"


def setupAndRunInsertion():
    """ Setup the infomation and run the test for the text into image routine.
    
    Steps
    1) Get the text file path and image file path from the user.
    2) Run the insertion routine and check that a valid extraction will be performable in the future.
        Try three time and none are successful tell the user to try a large file.
    """

    tk.Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    print "Select a Text file"

    textFileName = tkFileDialog.askopenfilename(title = "Select text file",filetypes = (("txt files","*.txt"),("all files","*.*"))) 
    print
    print "Select a Image file"
    
    imageFileName = tkFileDialog.askopenfilename(title = "Select image file",filetypes = (("png files","*.png"),("all files","*.*")))

    runCount = 0
    waiting, pin = ImageInsert(textFileName, imageFileName, False, '')
    while waiting == 'deCode' and runCount < 3:
        waiting, pin = ImageInsert(textFileName, imageFileName, True, pin)
        runCount += 1

    # Clean up
    
    cipherFileName = textFileName[:-4] + "_cipher" + textFileName[-4:]    
    if os.path.exists(cipherFileName):
        os.remove(cipherFileName)
    #if waiting == "Done":
        #if os.path.exists(textFileName):  <-- displayed in source code for testing purposes
        #    os.remove(textFileName)       <-- displayed in source code for testing purposes

    return waiting


def setupAndRunExtraction():
    """ Setup and run the image extraction routine.
    
    Steps
    1) Get the cover image file path from the user.
    2) Get the pin from the user.
    3) Run the image extraction routine.
    """

    print "Select a Image file to pull text out of"
    tk.Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    imageFileName = tkFileDialog.askopenfilename(title = "Select image file",filetypes = (("png files","*.png"),("all files","*.*")))
    
    invertable = 'f'
    print 
    print "Enter a 16 character long pin/password for the text being hidden in the image"
    
    while invertable != 't':
        pin = str(raw_input("> "))
        if pin == "exit":
            return "exit"
        while len(pin) != 16:
            print
            print "Wrong length" 
            print "Please enter a pin that is 16 characters long"
            pin = str(raw_input("> "))

        pin = [ord(pin[i]) for i in range(16)]

        if keyMod.invertable(pin):
            print
            print "This pin will not work"
            print "Please try another"
        else:
            invertable = 't'


    messageBack = ImageExtract(imageFileName, pin, False)

    # Clean up 1Test.txt
    if os.path.exists("1Test.txt"):
        os.remove("1Test.txt")

    if messageBack == "cleared":
        return "Done"
    else:
        return messageBack

def main():
    """ Run the steganography process.  
        
        Get chosen operation form user and run the proper process.
    """

    print
    print "Welcome to consealed encryption"

    Instructions()
    print
    print
    print "Enter 'e' for encryption or 'd' for decryption or 'h' for help"
    chosen = str(raw_input("> "))
    print
    print

    waiting = 'w'

    while waiting == "w":
        if chosen == "e" or chosen == "E":
            waiting = setupAndRunInsertion()
            if waiting != "Done" and waiting != "exit":
                print waiting            


        elif chosen == "d" or chosen == "D":
            waiting = setupAndRunExtraction()
            if waiting != "Done" and waiting != "exit":
                print waiting


        elif chosen == "h" or chosen == "H":
            helpPromp()
            print
            print "Enter e for encryption or d for decryption or h for help"
            chosen = str(raw_input("> "))
            print
            print

        elif chosen == "exit":
            waiting = 'exit'
        
        else:
            print "Enter e, d, h or exit"
            chosen = str(raw_input(">"))
            print
            print

        if waiting == 'Done':
            print
            print "Finished"
            waiting = 'w'
            print
            print
            print "Enter 'e' for encryption or 'd' for decryption or 'h' for help"
            chosen = str(raw_input("> "))
            print
            print

        elif waiting == "exit":
            print "Exiting"

        else:
            print
            print "Error: " + waiting
            waiting = 'w'
            print
            print
            print "Enter 'e' for encryption or 'd' for decryption or 'h' for help"
            chosen = str(raw_input("> "))
            print
            print

if __name__ == '__main__':
    main()
