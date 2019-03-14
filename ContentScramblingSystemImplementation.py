class ContentScramblingSystemImplementation:
    def __init__(self, init_1, init_2, file_name, output_name):
        self.css = ContentScramblingSystem(init_1, init_2)
        self.file_name = file_name
        self.output_name = output_name
        self.byte_size = (int(os.stat(file_name).st_size))



    def do_css(self):
        progress_print_counter = 0
        progress_counter = 0
        piece_size = 1
        
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