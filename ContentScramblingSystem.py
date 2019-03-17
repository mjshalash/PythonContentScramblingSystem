import os

class ContentScramblingSystem:
    #Initialize "blank" array of 25 bits
    LSFR_25 = [None]*25

    #Initialize "blank" array of 17 bits
    LSFR_17 = [None]*17

    poly_25 = [15, 5, 4, 1]
    poly_17 = [15, 1]
    carry = 0

    # "Constructor" for Content Scrambling System Class
    def __init__(self, seedOne, seedTwo):

        # Returns immutable sequence of integers corresponding to each LSFR
        byte_array_25 = bytes(seedOne, 'utf-8')
        byte_array_17 = bytes(seedTwo, 'utf-8')

        print("byte_array_17 is: ", byte_array_17)
        
        # Strings to represent bit strings for each LSFR
        bit_str_25 = ''
        bit_str_17 = ''

        # 25-bit LSFR
        # Convert initial three-byte seed into bits
        for b in byte_array_25:
            bit_str_25 += (str(bin(b)[2:].zfill(8)))

        # 17-bit LSFR
        # Convert initial two-byte seed into bits
        for b in byte_array_17:
            bit_str_17 += (str(bin(b)[2:].zfill(8)))
            print("bit_str_17 is: ", bit_str_17)

        # Append 1 into fourth bit
        self.LSFR_25[0:21] = bit_str_25[0:21]
        self.LSFR_25[21] = "1"
        self.LSFR_25[22:25] = bit_str_25[21:24]
        
        # Append 1 into fourth bit
        self.LSFR_17[0:13] = bit_str_17[0:13]
        self.LSFR_17[13] = "1"
        self.LSFR_17[14:17] = bit_str_17[13:16]

        print("LSFR_17 after appending: ", self.LSFR_17)

        # Convert each element in 17-bit LSFR array to a string
        for i in range(17):
            self.LSFR_17[i] = int(self.LSFR_17[i])

        # Convert each element in 25-bit LSFR array to a string
        for i in range(25):
            self.LSFR_25[i] = int(self.LSFR_25[i])

        # Note: MSB -> LSB
        return

    def rotate_set_25(self):
        
        # print(self.LSFR_25)
        xor_count = 0

        for i in self.poly_25:
            # if (i + 1) in self.poly_25:
            current_bit = int(self.LSFR_25[25 - i])
            if current_bit == 1:
                xor_count += 1

        xor_count = xor_count % 2

        for i in reversed(range(1,25)):
            self.LSFR_25[i] = self.LSFR_25[i - 1]

        self.LSFR_25[0] = xor_count

        # print(self.LSFR_25)

        return xor_count

    def rotate_set_17(self):
        # print(self.LSFR_17)
        xor_count = 0

        for i in self.poly_17:
            # if (i + 1) in self.poly_25:
            current_bit = int(self.LSFR_17[17 - i])
            if current_bit == 1:
                xor_count += 1

        xor_count = xor_count % 2

        for i in reversed(range(1, 17)):
            self.LSFR_17[i] = self.LSFR_17[i - 1]

        self.LSFR_17[0] = xor_count

        return xor_count

    def get_next_bytes(self):
        LSFR_25_bytes = []
        LSFR_17_bytes = []

        for i in range(8):
            LSFR_25_bytes.append(self.rotate_set_25())
            LSFR_17_bytes.append(self.rotate_set_17())

        return LSFR_17_bytes, LSFR_25_bytes

    # Function to add the two LSFR bit streams to each other
    def LSFR_add(self, LSFR_17_bytes, LSFR_25_bytes):
        LSFR_17_int = int((''.join((map(str, LSFR_17_bytes)))), 2)
        print(LSFR_17_int)
        
        LSFR_25_int = int((''.join((map(str, LSFR_25_bytes)))), 2)
        
        addition = LSFR_17_int + LSFR_25_int + self.carry
        self.carry = addition // 256
        addition = addition % 256
        return addition

    def get_next_sum(self):
        next_bytes = self.get_next_bytes()
        return self.LSFR_add(next_bytes[0], next_bytes[1])

