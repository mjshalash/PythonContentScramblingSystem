import os


class ContentScramblingSystem:
    # Initialize "blank" array of 25 bits
    lsfr25 = [None]*25

    # Initialize "blank" array of 17 bits
    lsfr17 = [None]*17

    # Tap Values originate from ploynomials provided by project rubric
    # C2(x)
    taps25 = [15, 5, 4, 1, 0]

    # C1(x)
    taps17 = [15, 1, 0]
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
        self.lsfr25[0:21] = seedOneBitString[0:21]
        self.lsfr25[21] = "1"
        self.lsfr25[22:25] = seedOneBitString[21:24]

        # Append 1 into fourth bit to prevent null cycle
        self.lsfr17[0:13] = seedTwoBitString[0:13]
        self.lsfr17[13] = "1"
        self.lsfr17[14:17] = seedTwoBitString[13:16]

        # Convert each element in 17-bit LSFR array to a integer
        for i in range(17):
            self.lsfr17[i] = int(self.lsfr17[i])

        # Convert each element in 25-bit LSFR array to a integer
        for i in range(25):
            self.lsfr25[i] = int(self.lsfr25[i])

        return

    def rotate_set_25(self):

        xor = 0

        for i in self.taps25:
            current_bit = int(self.lsfr25[24 - i])
            if current_bit == 1:
                xor += 1

        xor = xor % 2

        for i in reversed(range(1, 25)):
            self.lsfr25[i] = self.lsfr25[i - 1]

        self.lsfr25[0] = xor

        return xor

    def rotate_set_17(self):
        xor = 0

        for i in self.taps17:
            current_bit = int(self.lsfr17[16 - i])

            if current_bit == 1:
                xor += 1

        xor = xor % 2

        for i in reversed(range(1, 17)):
            self.lsfr17[i] = self.lsfr17[i - 1]

        self.lsfr17[0] = xor

        return xor

    # Gets next byte from input to "insert" into the LSFRs
    def refillLSFR(self):

        lsfr25OutputByte = []
        lsfr17OutputByte = []

        # Generate 8-bit output byte from respective LSFR
        for i in range(8):
            lsfr25OutputByte.append(self.rotate_set_25())
            lsfr17OutputByte.append(self.rotate_set_17())

        # Return the two output bytes
        return lsfr17OutputByte, lsfr25OutputByte

    # Function to combine the outputs of both LSFRs
    def lsfrAdd(self, lsfr17OutputByte, lsfr25OutputByte):
        lsfr17_int = int((''.join((map(str, lsfr17OutputByte)))), 2)
        lsfr25_int = int((''.join((map(str, lsfr25OutputByte)))), 2)

        # Add two LSFR outputs to retrieve next output byte
        result = lsfr17_int + lsfr25_int + self.additionCarry

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
