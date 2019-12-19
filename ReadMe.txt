Hidden Encryption through the uses of Steganography
User Handbook

      Modern steganography has opened the door to many novel and fascinating encryption 
like protocol.  Through the use of the python PyCrypto's AES encryption, Steganography 
algorithm LSB, and connecting piece we have formed a form of concealed encryption.  By 
encoding the encrypted form of a text file into a PNG image with LSB, we can leave no visible 
trace of encryption.  In order not to make passwords difficult we made a simple multiple 
layered matrix based encryption for AES�s key.  This allows any 16 character string that is 
memorable be used to add some protection to the key being stored.  

High-level notes:
	The PyCrypto application program will always take in a text file and produce a file text.
	The encryption for the AES's encryption key is done with matrix multiplication of three 
	matrices.  Based on the idea of using large prime to for factoring difficulty and idea of inverse 
	matrices to "cancel out" the unneeded matrices.  
	LSB algorithm is a standard single bit change to every pixel of an image implementation.

Platform:
	Concealed encryption is written for python 2.7 and can run on most operating system 
	like Windows, Mac os, and Linux. 

Installation:
	After downloading or clone the executable it is a simple as double clicking on the file.
	After downloading or clone the source code these libraries will need to be installed:
	-	PIL (Python Image Library)
	-	PyCrypto (This can be installed with: "pip install pycryptodome")
	-	numPy (This can be installed with: "pip install numpy")

Instructions:
Script will start by asking for one of the following options to be chosen: 
e) Enter in 'e' if you want to encrypt a text file into an image.
d) Enter in 'd' if you want to decrypt an image to pullout the text file.
h) Enter in 'h' if you needed help with an error message or needed the instructions again.
   exit) Enter in 'exit' when you would like to leave the software.

   Encryption:
    When encryption is selected a file window will open asking for a .txt file."
    Select the text file that you would like to encrypt into an image in this window."
    After you select a text file a new window will open asking for a .png file."
    Select the image file that you would like the text file to be encrypted into within this window."
    Once the two files have been selected you will be prompted to enter a 16 character long pin."
    This pin will act as a password to the text file that you have selected to encrypt."
    After the pin is entered the software will attempt to encrypt the text file into the image."
    It HIGHLY recommend that you try decrypting the image after the encryption process has finished.
    
   Decryption:
    When decryption is selected a file window will open asking for a .png file.
    Select the image file in the window that you would like to decrypt the text out of.
    Once the image file is selected you will be prompted to enter the 16 character long pin for the text 
	within the image.
    This is the same pin which you entered when you encrypted into the image.
    After the pin is entered the software will begin decrypting the image.
  
    Help:
    When you request help you will be asked for one of the two following options:
    i) Enter in 'i' to display these instruction once again.
    m) Enter in 'm' to get quick information about an error message.
         Error message help:
         When you enter the error message help section you will be asked for one of the following to 
options:
         e) Enter in 'e' if the error message comes from the encryption process.
         d) Enter in 'd' if the error message comes from the decryption process.
         Once one is selected you will be asked for the error message.
         After you enter in the message a short description of what caused the error will be displayed.
         For more information about the error and some resolution options check the handbook.

Error messages and troubleshooting ideas:
=============================================================================================================
Error message         | Meaning                                                                             |
======================|=====================================================================================|
======================|=====================================================================================|
Encryption message    |                                                                                     |
======================|=====================================================================================|
image                 | The image chose cannot be opened.  Please try a again with a .png file.             |
======================|=====================================================================================|
text                  | The text file could not be open or buffered.  Double check that the                 |
                      | chosen text file is not corrupt and try again.                                      |
keyMask               | Key masking process failed.  Most likely do the generated key. Try running again.   |
======================|=====================================================================================|
aes                   | AES encryption has failed.  Most likely to do with the generated key                |
                      | and or file length. Try running again to generate new key and                       |
                      | buffering the file once more.                                                       |
======================|=====================================================================================|
lsb                   | During the image encoding process an error occurred.  Most likely due               |
                      | to the size of the cipher file being very large and not fitting in                  |
                      | memory.  Try running again and/or braking up the text file into                     |
                      | smaller pieces.                                                                     |
======================|=====================================================================================|
key                   | A check was made to make sure that the text file would be                           |
                      | recoverable and an error was encountered during the AES decryption                  |
                      | step.  If the script had been running for a long time try a bigger image            |
                      | file or braking the text file into smaller piece.  Otherwise just try               |
                      | running again.                                                                      |
======================|=====================================================================================|
deCode                | A check was made to make sure that the text file would be                           |
                      | recoverable and a general error was encountered.  This most likely                  |
                      | comes from the decoding process where the image was not of                          |
                      | adequate size. Try a bigger image file or braking the text file into                |
                      | smaller piece and running again.                                                    |
======================|=====================================================================================|
======================|=====================================================================================|
Decryption messages                                                                                         |
======================|=====================================================================================|
lsb                   | During the image decoding phase an error occurred.  Check that the                  |
                      | right image and pin where used, then try a again.                                   |
======================|=====================================================================================|
info                  | A problem with a file information string was encountered.  Check that               |
                      | the right images was selected and try again.                                        |
======================|=====================================================================================|
key                   | Key unmasking process failed.  Check that the right image was                       |
                      | selected and double check the pin, then try a again.                                |
======================|=====================================================================================|
aes                   | AES decryption failed and probably do to a bad key unmask.   Double                 |
                      | check the pin and try a again.                                                      |
============================================================================================================|
============================================================================================================|
