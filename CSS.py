import os

class ContentScramblingSystem:
    set_25 = [None]*25
    set_17 = [None]*17
    poly_25 = [15, 5, 4, 1]
    poly_17 = [15, 1]
    carry = 0

    # "Constructor" for Content Scrambling System Class
    def __init__(self, chars_25, chars_17):

        # Returns immutable sequence of integers corresponding to each LSFR
        byte_array_25 = bytes(chars_25, 'utf-8')
        byte_array_17 = bytes(chars_17, 'utf-8')
        
        # Strings to represent bit strings for each LSFR
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





class ContentScramblingSystemImplementation:
    
    # Define the initial class
    def __init__(self, init_1, init_2, file_name, output_name):
        
        # Establish Class Variables for Content Scrambling System Implementation
        self.css = ContentScramblingSystem(init_1, init_2)  # CSS
        self.file_name = file_name                          # File to read in
        self.output_name = output_name                      # File to write out to
        self.byte_size = (int(os.stat(file_name).st_size))  


    # Carry out the computation
    def do_css(self):
        progress_print_counter = 0
        progress_counter = 0
        piece_size = 1
        
        # Read input file as a raw bytestream, Write to output file with a raw bytestream
        with open(self.file_name, "rb") as in_file, open(self.output_name, "wb") as out_file:
            while True:
                piece = in_file.read(piece_size)
                if piece == b"":
                    break

                piece_int = ord(piece)
                next_xor_byte = self.css.get_next_sum()
                write_int = piece_int ^ next_xor_byte
                write_byte = write_int.to_bytes(1, byteorder="big")


                out_file.write(write_byte)
                progress_counter += 1
                progress = (progress_counter / self.byte_size) * 100

                if progress // 10 > progress_print_counter:
                    print(str(progress) + " % Done")
                    progress_print_counter += 1





# cssi = ContentScramblingSystemImplementation("abc", "12", "CECS 564/ArtOfWar.txt", "CECS 564/ENCRYPT_OUTPUT.txt")
cssi = ContentScramblingSystemImplementation("abc", "12", "CECS 564/ENCRYPT_OUTPUT.txt", "CECS 564/DECRYPT_OUTPUT.txt")
cssi.do_css()

print()





