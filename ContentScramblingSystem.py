import os

class ContentScramblingSystem:
    #Initialize "blank" array of 25 bits
    lsfr25 = [None]*25

    #Initialize "blank" array of 17 bits
    lsfr17 = [None]*17


    poly_25 = [15, 5, 4, 1]
    poly_17 = [15, 1]
    additionCarry = 0

    # "Constructor" for Content Scrambling System Class
    def __init__(self, seedOne, seedTwo):

        # Returns immutable sequence of integers corresponding to each LSFR
        seedOneBytes = bytes(seedOne, 'utf-8')
        seedTwoBytes = bytes(seedTwo, 'utf-8')

        print("byte_array_17 is: ", seedTwoBytes)
        
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
            print("bit_str_17 is: ", seedTwoBitString)

        # Append 1 into fourth bit to prevent null cycle
        self.lsfr25[0:21] = seedOneBitString[0:21]
        self.lsfr25[21] = "1"
        self.lsfr25[22:25] = seedOneBitString[21:24]
        
        # Append 1 into fourth bit to prevent null cycle
        self.lsfr17[0:13] = seedTwoBitString[0:13]
        self.lsfr17[13] = "1"
        self.lsfr17[14:17] = seedTwoBitString[13:16]

        print("lsfr17 after appending: ", self.lsfr17)

        # Convert each element in 17-bit LSFR array to a string
        for i in range(17):
            self.lsfr17[i] = int(self.lsfr17[i])

        # Convert each element in 25-bit LSFR array to a string
        for i in range(25):
            self.lsfr25[i] = int(self.lsfr25[i])

        return

    def rotate_set_25(self):
        
        # print(self.lsfr25)
        xor_count = 0

        for i in self.poly_25:
            # if (i + 1) in self.poly_25:
            current_bit = int(self.lsfr25[25 - i])
            if current_bit == 1:
                xor_count += 1

        xor_count = xor_count % 2

        for i in reversed(range(1,25)):
            self.lsfr25[i] = self.lsfr25[i - 1]

        self.lsfr25[0] = xor_count

        # print(self.lsfr25)

        return xor_count

    def rotate_set_17(self):
        # print(self.lsfr17)
        xor_count = 0

        for i in self.poly_17:
            # if (i + 1) in self.poly_25:
            current_bit = int(self.lsfr17[17 - i])
            if current_bit == 1:
                xor_count += 1

        xor_count = xor_count % 2

        for i in reversed(range(1, 17)):
            self.lsfr17[i] = self.lsfr17[i - 1]

        self.lsfr17[0] = xor_count

        return xor_count

    # Gets next byte from input to "insert" into the LSFRs
    def refillLSFR(self):
        lsfr25_bytes = []
        lsfr17_bytes = []

        for i in range(8):
            lsfr25_bytes.append(self.rotate_set_25())
            lsfr17_bytes.append(self.rotate_set_17())

        return lsfr17_bytes, lsfr25_bytes

    # Function to combine the outputs of both LSFRs
    def lsfrAdd(self, lsfr17_bytes, lsfr25_bytes):        
        lsfr17_int = int((''.join((map(str, lsfr17_bytes)))), 2)
        lsfr25_int = int((''.join((map(str, lsfr25_bytes)))), 2)
        
        # Add two LSFR outputs to retrieve next output byte
        result = lsfr17_int + lsfr25_int + self.additionCarry
        
        # Establish additionCarry to be used in addition for next output byte
        self.additionCarry = result // 256
        result = result % 256

        # Return the newly found output byte
        return result

    def getOutputByte(self):
        next_bytes = self.refillLSFR()
        return self.lsfrAdd(next_bytes[0], next_bytes[1])

