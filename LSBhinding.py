# Author: Gage Boehm
# Date: 12/01/2019

# Description
# The purpose of this program is to encode or decode two string into or out of a target image
#
# An image in a sense is just a matrix of tuples, where each tuple has three numeric values that represent the intensity of three different light colors.  
# The three values have the range 0-255 and the tuple is formatted as (RED, GREEN, BLUE). 
#
# Encoding:
# To encode the given message and info string into the image convert the message and info string into two sets of ascii values.
# Then convert the two ascii values sets into binary and tack on the bits fifteen 1's and one 0 to act as a delimiter/end point for both bit patterns.
# Then reading the image pixel by pixel we convert the three light color values into binary bit patterns.
# For the message bits look at the last bit in the pattern and check that it is a 0 or 1, if it is we replace that bit with one bit from the message.
# For the info bits look at the end bit of the green light bit pattern, which corresponds to bit 48, if it is a 0 or 1 we replace it with one bit from the info string. 
# Repeat this process until all message bits and info bits have been encoded into the image.
#
# Decoding:
# To decode a stego image the reverse the encoding is basically done.
# Reading the image pixel by pixel we convert the three light color values into binary bit patterns.
# Grab the last bit off the whole patter and added it to the message bit string.
# Grab the 48th bit, which is the last green light bit and add it to the info bit string.
# Stop pulling bits from the green light once the fifteen 1's and one 0 delimiter of the info bit string had been hit.
# Stop pulling bits from the blue light once the fifteen 1's and one 0 delimiter of the message bit string has been hit.
# Convert the two bit pattern minus the delimiter back into ascii characters to create the original two character string.

# The structure of the LSB comes from a video tutorial done by DrapTV 
# "Steganography Tutorial - Hiding Text inside an Image" By DrapTV
# DrapTV. "Steganography Tutorial - Hiding Text inside an Image." YouTube, 22 Mar. 2014, https://www.youtube.com/watch?v=q3eOOMx5qoo&t=25s.



import binascii
import random
import sys
from PIL import Image


def rgb2bin(r, g, b):
    """ Convert the pixel tuple (red, green, blue) into a bit pattern of the form 0brr...rgg..ggbb..bb 
    
    Steps:
    1) Convert each color from in to binary.
    2) Standardize the size of each bit pattern. 
       Then return the each bit patter appended togeather.
    """

    # 1)
    # ---------------------------------------------------------------------------------------------
    red = bin(int(binascii.hexlify(str(r)), 16))
    green = bin(int(binascii.hexlify(str(g)), 16))
    blue = bin(int(binascii.hexlify(str(b)), 16))

    # 2)
    # ---------------------------------------------------------------------------------------------
    if len(red[2:]) < 24:
        buff = "0" * (24 - len(red[2:]))
        red = "0b" + buff + red[2:]

    if len(green[2:]) < 24:
        buff = "0" * (24 - len(green[2:]))
        green = "0b" + buff + green[2:]
    
    if len(blue[2:]) < 24:
        buff = "0" * (24 - len(blue[2:]))
        blue = "0b" + buff + blue[2:]

    return red + green[2:] + blue[2:]


def bin2rgb(binCode):
    """ Convert the bit pattern of the from 0brr...rgg..ggbb..bb back into the pixel tuple (red, green, blue).
    
    Steps:
    1) Grab the bit pattern for each color from the whole bit pattern.
    2) Convert each color's bit pattern back to an interger.
    """

    # 1)
    # ---------------------------------------------------------------------------------------------
    red = binCode[2:26]
    green = binCode[26:50]
    blue = binCode[50:74]

    # 2)
    # ---------------------------------------------------------------------------------------------
    r = binascii.unhexlify("%x" % (int(red, 2)))
    g = binascii.unhexlify("%x" % (int(green, 2)))
    b = binascii.unhexlify("%x" % (int(blue, 2)))

    return int(r) , int(g) , int(b)


def str2bin(message):
    """ Convert the ascii characters into there bit patterns."""
    binary = bin(int(binascii.hexlify(message), 16))
    return binary[2:]


def binary2str(binary):
    """ Convert the bit pattern into ascii characters"""
    message = binascii.unhexlify('%x' % (int('0b' + binary, 2)))
    return message


def encodeOneBit(bincode, messageBit):
    """ When the bit pattern for the blue channel end with 0 or 1 
        replace it with the current bit from the message"""
    if bincode[-1] in ('0', '1'):
        bincode = bincode[:-1] + messageBit
        return bincode
    else:
        return None

def decodeOneBit(bincode):
    """ When the blue channel's bit pattern end with a 0 or 1
        grab the bit as it's part of the message"""
    if bincode[-1] in ('0', '1'):
        return bincode[-1]
    else:
        return None

def encodeTwoBits(bincode, messageBit, infoBit):
    """ When the bit pattern for the blue and green channel end with 0 or 1:
        Replace the blue channel's bit with the current bit from the message.
        Replace the green channel's bit with the current bit from the AES infomation string."""

    if bincode[-1] in ('0', '1') and bincode[-23] in ('0', '1'):
        bincode = bincode[:-1] + messageBit
        bincode = bincode[:-25] + infoBit + bincode[-24:]

        return bincode
    else:
        return None

def decodeTwoBits(bincode):
    """ When the blue and green channeles bit pattern end with a 0 or 1:
        Grab the blue channel bit as it's part of the message.
        Grab the green channel bit as it's part of the AES infomation string."""
    if bincode[-1] in ('0', '1'):
        return bincode[-1], bincode[-25]
    else:
        return None, None


def encode(filename, cipherMessage, infoMessage):
    """ Encode the given message into the given image
    
    Steps:
    1) Convert the given message and information string into binary and add on the delemiter 15 1's with one zero to each
       Then check if the provided image is the correct image format 
    2) Reading in one pixel at a time from the image:
        - Determine with there is still message bits and infomation bits, 
          calling the correct encoding step or no coding step depending on.
        - If a bit was encoded, convert the pixel it back into is color numbers and append it to the image out list
          Otherwise just append the unmodified pixel to the image out list
    3) Create the cover image.
    """
    
    # 1)
    # ---------------------------------------------------------------------------------------------
    binaryMessage = str2bin(cipherMessage) + '1111111111111110'
    binaryInfo = str2bin(infoMessage) + '1111111111111110'
    img = Image.open(filename)
    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        data = img.getdata()

        newData = []
        digit = 0
        temp = ''

        # 2)
        # ---------------------------------------------------------------------------------------------
        for item in data:
            if (digit < len(binaryMessage)):
                
                if (digit < len(binaryInfo)):
                    newpix = encodeTwoBits(rgb2bin(item[0], item[1], item[2]), binaryMessage[digit], binaryInfo[digit])
                else:
                    # Convert out pixel into a binary code and give which ever bit of the message we are currently on, a 0 or a 1
                    newpix = encodeOneBit(rgb2bin(item[0], item[1], item[2]), binaryMessage[digit])
            
                if newpix == None:
                    newData.append(item)
                else:
                    
                    r, g, b = bin2rgb(newpix)
                    
                    newData.append((r,g,b,255))
                    digit += 1
            else:
                newData.append(item)
        
        # 3) 
        # ---------------------------------------------------------------------------------------------
        img.putdata(newData)
        img.save(filename[:-4] + "_encode" + filename[-4:], "PNG")
        
        return "Completed!"
    return "Incorrect image mode"

def decode(filename):
    """ Pull the message out of the given image
    
    Steps:
    1) Stetup the output strings and check if the provided image is the correct image format 
    2) Reading in one pixel at a time from the image:
        - Get the message and infomation bit from the pixel.
        - Check if the delimiter has been hit for both the message and information string.
    3) Convert both the message bit pattern and infomation string bit pattern into strings and return them back the the caller.
    """

    # 1)
    # ---------------------------------------------------------------------------------------------
    img = Image.open(filename)
    binaryMessage = ''
    binaryInfo = ''
    infoDone = 'f'

    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        data = img.getdata()

        # 2)
        # ---------------------------------------------------------------------------------------------
        for item in data:
    
            if infoDone != 't':
                messageBit, infoBit = decodeTwoBits(rgb2bin(item[0], item[1], item[2]))
            else:
                messageBit = decodeOneBit(rgb2bin(item[0], item[1], item[2]))
            
            if messageBit == None:
                pass
            else:
                binaryMessage = binaryMessage + messageBit
                if (binaryMessage[-16:] == '1111111111111110'):
                    return binary2str(binaryMessage[:-16]), binary2str(binaryInfo[:-16])
                
                if infoDone != 't':
                    binaryInfo = binaryInfo + infoBit

                    if (binaryInfo[-16:] == '1111111111111110'):
                        infoDone = 't'

        # 3)
        # ---------------------------------------------------------------------------------------------
        return binary2str(binaryMessage), binary2str(binaryInfo[:-16])
    return "Incorrect Image mode"
