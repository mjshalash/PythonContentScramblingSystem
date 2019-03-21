import os


class ContentScramblingSystem:
    # Initialize "blank" array of 25 bits
    # None initialization is needed so the fourth bit can be injected properly
    lfsr25 = [None]*25

    # Initialize "blank" array of 17 bits
    # None initialization is needed so the fourth bit can be injected properly
    lfsr17 = [None]*17

    # Tap Values originate from ploynomials provided by project rubric
    additionCarry = 0

    # "Constructor" for Content Scrambling System Class
    def __init__(self, seedOne, seedTwo):

        # Returns immutable sequence of integers corresponding to each LSFR
        seedOneBytes = bytes(seedOne, 'utf-8')
        seedTwoBytes = bytes(seedTwo, 'utf-8')

        # Strings to represent bit strings for each LSFR seed
        seedOneBitString = ''
        seedTwoBitString = ''

        # 25-bit LSFR
        # Convert initial three-byte seed into bits
        for b in seedOneBytes:
            seedOneBitString += (str(bin(b)[2:].zfill(8)))

        # 17-bit LSFR
        # Convert initial two-byte seed into bits
        for b in seedTwoBytes:
            seedTwoBitString += (str(bin(b)[2:].zfill(8)))

        # Append 1 into fourth bit to prevent null cycle
        self.lfsr25[0:21] = seedOneBitString[0:21]
        self.lfsr25[21] = "1"
        self.lfsr25[22:25] = seedOneBitString[21:24]

        # Append 1 into fourth bit to prevent null cycle
        self.lfsr17[0:13] = seedTwoBitString[0:13]
        self.lfsr17[13] = "1"
        self.lfsr17[14:17] = seedTwoBitString[13:16]

        # Convert each element in 17-bit LSFR array to a integer
        for i in range(17):
            self.lfsr17[i] = int(self.lfsr17[i])

        # Convert each element in 25-bit LSFR array to a integer
        for i in range(25):
            self.lfsr25[i] = int(self.lfsr25[i])

        return

    # "Rotate" 25-bit lsfr, establish new MSB and return this same value as part of our output byte
    # C2(X) => taps => [15, 5, 4, 1, 0]
    def rotate_set_25(self):

        # Bits to be XOR'd
        xBitOne = 0
        xBitTwo = 0
        xBitThree = 0
        xBitFour = 0
        xBitFive = 0

        # Final XOR result
        tappedXorOutput = 0

        # Find bits
        xBitOne = int(self.lfsr25[24 - 15])
        xBitTwo = int(self.lfsr25[24 - 5])
        xBitThree = int(self.lfsr25[24 - 4])
        xBitFour = int(self.lfsr25[24 - 1])
        xBitFive = int(self.lfsr25[24])

        # Use binary xor to calculate result
        tappedXorOutput = xBitOne ^ xBitTwo ^ xBitThree ^ xBitFour ^ xBitFive

        # Shift bits to the right to make room for new MSB
        for i in reversed(range(1, 25)):
            self.lfsr25[i] = self.lfsr25[i - 1]

        # Set new MSB
        self.lfsr25[0] = tappedXorOutput

        # Return next bit to append to output byte
        return tappedXorOutput

    # "Rotate" 17-bit lsfr, establish new MSB and return this same value as part of our output byte
    # C(x) => taps => [15, 1, 0]
    def rotate_set_17(self):

        # Bits to be XOR'd
        xBitOne = 0
        xBitTwo = 0
        xBitThree = 0

        # Final XOR result
        tappedXorOutput = 0

        # Find bits
        xBitOne = int(self.lfsr17[16 - 15])
        xBitTwo = int(self.lfsr17[16 - 1])
        xBitThree = int(self.lfsr17[16])

        # Use binary xor to calculate result
        tappedXorOutput = xBitOne ^ xBitTwo ^ xBitThree

        # Shift bits to the right to make room for new MSB
        for i in reversed(range(1, 17)):
            self.lfsr17[i] = self.lfsr17[i - 1]

        # Set new MSB
        self.lfsr17[0] = tappedXorOutput

        # Return next bit to append to output byte
        return tappedXorOutput

    # Gets next byte from input to "insert" into the LSFRs
    def refillLSFR(self):

        # Initialize output byte arrays
        lfsr25OutputByte = []
        lfsr17OutputByte = []

        # Generate 8-bit output byte from respective LFSR
        for i in range(8):
            lfsr25OutputByte.append(self.rotate_set_25())
            lfsr17OutputByte.append(self.rotate_set_17())

        # Return the two output bytes
        return lfsr17OutputByte, lfsr25OutputByte

    # Function to combine the outputs of both LSFRs
    def lsfrAdd(self, lfsr17OutputByte, lfsr25OutputByte):
        lfsr17Int = int((''.join((map(str, lfsr17OutputByte)))), 2)
        lfsr25Int = int((''.join((map(str, lfsr25OutputByte)))), 2)

        # Add two LSFR outputs to retrieve next output byte
        result = lfsr17Int + lfsr25Int + self.additionCarry

        # Establish additionCarry to be used in addition for next output byte
        self.additionCarry = result // 256
        result = result % 256

        # Return the newly found output byte
        return result

    def getOutputByte(self):

        # Compute the next two output bytes from the 17-bit LSFR and the 25-bit LSFR
        # Stored in next bytes tuple
        nextBytes = self.refillLSFR()

        # Combine the two output bytes utilizing 8-bit addition
        # Value returned to test.py for further processing
        return self.lsfrAdd(nextBytes[0], nextBytes[1])
