import os, ContentScramblingSystemImplementation

class ContentScramblingSystem:
    set_25 = [None]*25
    set_17 = [None]*17
    poly_25 = [15, 5, 4, 1]
    poly_17 = [15, 1]
    carry = 0

    def __init__(self, chars_25, chars_17):
        byte_array_25 = bytes(chars_25, 'utf-8')
        byte_array_17 = bytes(chars_17, 'utf-8')
        bit_str_25 = ''
        bit_str_17 = ''

        for b in byte_array_25:
            bit_str_25 += (str(bin(b)[2:].zfill(8)))

        for b in byte_array_17:
            bit_str_17 += (str(bin(b)[2:].zfill(8)))

        self.set_25[0:21] = bit_str_25[0:21]
        self.set_25[21] = "1"
        self.set_25[22:25] = bit_str_25[21:24]
        # self.set_25 = list(reversed(self.set_25))


        self.set_17[0:13] = bit_str_17[0:13]
        self.set_17[13] = "1"
        self.set_17[14:17] = bit_str_17[13:16]
        # self.set_17 = list(reversed(self.set_17))

        for i in range(17):
            self.set_17[i] = int(self.set_17[i])

        for i in range(25):
            self.set_25[i] = int(self.set_25[i])

        # Note: MSB -> LSB
        return



    def rotate_set_25(self):
        # print(self.set_25)
        xor_count = 0

        for i in self.poly_25:
            # if (i + 1) in self.poly_25:
            current_bit = int(self.set_25[25 - i])
            if current_bit == 1:
                xor_count += 1

        xor_count = xor_count % 2

        for i in reversed(range(1,25)):
            self.set_25[i] = self.set_25[i - 1]

        self.set_25[0] = xor_count

        # print(self.set_25)

        return xor_count


    def rotate_set_17(self):
        # print(self.set_17)
        xor_count = 0

        for i in self.poly_17:
            # if (i + 1) in self.poly_25:
            current_bit = int(self.set_17[17 - i])
            if current_bit == 1:
                xor_count += 1

        xor_count = xor_count % 2

        for i in reversed(range(1, 17)):
            self.set_17[i] = self.set_17[i - 1]

        self.set_17[0] = xor_count
        #  print(self.set_17)

        return xor_count



    def get_next_bytes(self):
        set_25_bytes = []
        set_17_bytes = []

        for i in range(8):
            set_25_bytes.append(self.rotate_set_25())
            set_17_bytes.append(self.rotate_set_17())

        return set_17_bytes, set_25_bytes

    def full_adder(self, set_17_bytes, set_25_bytes):
        set_17_int = int((''.join((map(str, set_17_bytes)))), 2)
        set_25_int = int((''.join((map(str, set_25_bytes)))), 2)
        addition = set_17_int + set_25_int + self.carry
        self.carry = addition // 256
        addition = addition % 256
        return addition



    def get_next_sum(self):
        next_bytes = self.get_next_bytes()
        return self.full_adder(next_bytes[0], next_bytes[1])