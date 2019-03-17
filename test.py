import os, ContentScramblingSystem

class test:
    
    # Constructor for ContentScramblingImplementation
    def __init__(self, seedOne, seedTwo, file_name, output_name):
       
        # Create class for Content Scrambling System
        self.css = ContentScramblingSystem.ContentScramblingSystem(seedOne, seedTwo)  # CSS
        
        # File to read data from
        self.file_name = file_name 

        # File path to write encryption/decryption to                       
        self.output_name = output_name         
        
        # Size of th input file in bytes
        self.byte_size = (int(os.stat(file_name).st_size))  

    # Carry out the computation
    def compute(self):
        
        # Number of bytes to read in from file
        piece_size = 1
        
        # Read input file as a raw bytestream
        # Write to output file with a raw bytestream
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



# Test Encryption (to test decryption, switch files)
# Create instance of test class
# Initialized with a "three" byte seed for 25-bit LSFR
# Initialized with a "two" byte seed for 17-bit LSFR
cssi = test("abc", "12", "encryptTest.txt", "decryptTest.txt")

# Run Content Scrambling System
cssi.compute()

print()





