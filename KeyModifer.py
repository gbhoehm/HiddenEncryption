# Author: Gage Boehm
# Date: 12/03/2019

# Description
# Purpose of this program is to mask and unmask a 4X4 matrix that is given is list form.
#
# Masking:
# 1) Convert the provided pin, key seed, and an internal prime number list into NumPy matrices.
# 2) Scramble/mix-up the rows and columns of the key seed matrix and prime number matrix.
# 3) Multiply the matrices together to from the storage key matrix.
# 4) Convert the storage key matrix into a list of numbers.
#
# Unmask:
# 1) Convert the provided pin, storage key, and an internal prime number list into NumPy matrices.
# 2) Scramble the prime matrix, then multiply the prime matrix and pin matrix.
# 3) Take the inverse of the prime/pin matrix and multiply it with the storage key matrix.
# 4) Unscrambling the key matrix and convert it back into a list of numbers. 


import os
import numpy


def invertable(pin):
    """ Test if the provided pin is invertable """

    pinOffset = ((sum(pin))/len(pin))%16
    pinMatrix = convertIntoMatrix(pin, pinOffset)
    return numpy.linalg.det(pinMatrix) == 0


def convertIntoMatrix(listIn, offset):
    """ Convert the provided list of numbers into a 4X4 matrix
    
    Steps:
    1) Take four numbers from the inputted list and build a numpy array with those four numbers.
        This array will be the first row in the outputted matrix.        
    2) Grab four numbers at a time from the inputted list, build a numpy array with those four numbers, 
       and then add the array to the matrix.
       Repate twice.
    """

    # 1)
    # ---------------------------------------------------------------------------------------------
    listSegment = []
    for i in range(4):
        index = (offset) % 16
        listSegment.append(listIn[index])
        offset += 1

    matrix = numpy.array([listSegment])
    listSegment = []
    
    # 2)
    # ---------------------------------------------------------------------------------------------
    for i in range(12):
        index = (offset) % 16
        listSegment.append(listIn[index])
        
        if (len(listSegment) % 4) == 0:
            b = numpy.array([listSegment])
            matrix = numpy.concatenate((matrix, b))
            listSegment = []

        offset += 1
    
    return matrix


def convertIntoList(A, offset):
    """ Convert the matrix A back into a list of numbers """

    tempList = []
    for i in range(4):
        row = A[[i]]
        
        for j in range(4):
            tempList.append(int(round(row[0][j])))

    outList = []
    for i in range(16):
        index = (offset) % 16
        outList.append(tempList[-index])
        offset -= 1

    return outList


def scrambleMatrix(A, mixNumber, primeMix):
    """ Swap two rows and two columns based on the provided mixing number
    
    This is done in the manner: swap row, swap column, adjust mixing number, swap row, swap column.

    The prime matrix and the key matrix second mixing number slightly different to mask any pattern between the two.
    """
    
    for i in range(2):
        
        # swap row 1 with the mixNumber row
        # default row 1 swap with row 4
        if mixNumber != 0:
            A[[0,mixNumber]] = A[[mixNumber,0]]
        else:
            A[[mixNumber, 3]] = A[[3, mixNumber]]

        # swap column 1 with the mixNumber column
        # default column 1 swap with column 4
        if mixNumber != 0:
            A[:,[0,mixNumber]] = A[:,[mixNumber,0]]
        else:
            A[:,[mixNumber, 3]] = A[:,[3, mixNumber]]

        if primeMix == 't':
            mixNumber = (mixNumber + 3) % 4
        else:    
            mixNumber = (mixNumber + 2) % 3
    return A


def unscrambleMatrix(A, mixNumber, primeMix):
    """ Reverse the swaping done by the scrambleMatrix step to restore the prime and key matrices
    
    This is done in the manner: adjust mixing number, reverse column swap, reverse row swap, back to provided mixing number,
                                reverse column swap, reverse row swap.

    The prime matrix and the key matrix second mixing number is slightly different, adjust accordingly.
    """
    
    # swap rows and columns based on the mixNumber provided
    storeOGMixNum = mixNumber
    if primeMix == 't':
        mixNumber = (mixNumber + 3) % 4
    else:    
        mixNumber = (mixNumber + 2) % 3
    
    for i in range(2):

        # swap column 1 with the mixNumber column
        # default column 1 swap with column 4
        if mixNumber != 0:
            A[:,[0,mixNumber]] = A[:,[mixNumber,0]]
        else:
            A[:,[mixNumber, 3]] = A[:,[3, mixNumber]]

        # swap row 1 with the mixNumber row
        # default row 1 swap with row 4
        if mixNumber != 0:
            A[[0,mixNumber]] = A[[mixNumber,0]]
        else:
            A[[mixNumber, 3]] = A[[3, mixNumber]]

        mixNumber = storeOGMixNum

    return A


def maskKey(keySeedMatrix, pin):
    """ Prefrom three simple steps to mask the Key used in the AES encryption phase.
    
    The three steps are:
    1) Calcute an offset for the three list, that way when converted into a matrix the list and matrix do not line up.
    2) Scramble the key matrix, and scramble the prime matrix.  The scrambaling the prime matrix is to add verity between runs.
    3) prefrom this calculation: Pmatrix X PINmatrix X KEYmatrix = StorageMatrix.  Return the StorageMatrix in list from to the caller.
    
    """

    primesList = [999425970427, 927425969867, 327425970031, 762475413737, 441349, 325861, 785597, 165541, 7640287, 2168377, 9396271, 94113661, 37814797, 378135293, 624938047, 2624756177]

    # 1)
    # ---------------------------------------------------------------------------------------------
    pinSum = sum(pin)
    pinLength = len(pin)
    keySeedOffset = ((pinSum+(primesList[3]*primesList[1]))/pinLength)%16
    primeMatrixOffset = ((pinSum+(primesList[5]*primesList[15]))/pinLength)%16
    pinOffset = ((pinSum)/pinLength)%16

    
    pinMatrix = convertIntoMatrix(pin, pinOffset)
    
    # Check if the pin isn't invertable
    if numpy.linalg.det(pinMatrix) == 0:
        print
        print "This pin will not work"
        print "Please try another"
        return 'f', keySeedMatrix
                    

    keySeedMatrix = convertIntoMatrix(keySeedMatrix, keySeedOffset)
    primeMatrix = convertIntoMatrix(primesList, primeMatrixOffset)


    # 2)
    # ---------------------------------------------------------------------------------------------
    keySeedMatrix = scrambleMatrix(keySeedMatrix, ((pinOffset + primeMatrixOffset)%4), 'f')
    primeMatrix = scrambleMatrix(primeMatrix, ((pinOffset + primeMatrixOffset)%3), 't')

    # 3)
    # ---------------------------------------------------------------------------------------------
    pinMatrix = primeMatrix.dot(pinMatrix)
    storageKeyMatrix = pinMatrix.dot(keySeedMatrix)

    return 't', convertIntoList(storageKeyMatrix, 0)
    

def unMaskKey(storageKey, pin):
    """ Convert the StorageKey back into its original form.  

        Perfrom these three steps to rebuild the original key's seed:
        1) Calcute an offset for the three list, that way when converted into a matrix the list and matrix do not line up.
        2) Scramble the prime matrix. 
        3) prefrom this calculation: inverse(Pmatrix X PINmatrix) X KEYmatrix = StorageMatrix.  Return the StorageMatrix to the caller.
        4) Unscramble the key matrix, and return it in list from.
    """
    
    primesList = [999425970427, 927425969867, 327425970031, 762475413737, 441349, 325861, 785597, 165541, 7640287, 2168377, 9396271, 94113661, 37814797, 378135293, 624938047, 2624756177]


    pinSum = sum(pin)
    pinLength = len(pin)
    keySeedOffset = ((pinSum+(primesList[3]*primesList[1]))/pinLength)%16
    primeMatrixOffset = ((pinSum+(primesList[5]*primesList[15]))/pinLength)%16
    pinOffset = ((pinSum)/pinLength)%16

    # Convert the pin, primes, and storage key into matrices
    pinMatrix = convertIntoMatrix(pin, pinOffset)
    primeMatrix = convertIntoMatrix(primesList, primeMatrixOffset)
    storageKeyMatrix = convertIntoMatrix(storageKey, 0)


    primeMatrix = scrambleMatrix(primeMatrix, ((pinOffset + primeMatrixOffset)%3), 't')
    pinMatrix = primeMatrix.dot(pinMatrix)

    inversePinMatrix = numpy.linalg.inv(pinMatrix)

    keySeedMatrix = inversePinMatrix.dot(storageKeyMatrix)
    keySeedMatrix = unscrambleMatrix(keySeedMatrix, ((pinOffset + primeMatrixOffset)%4), 'f')

    keySeed = convertIntoList(keySeedMatrix, keySeedOffset)

    return keySeed
