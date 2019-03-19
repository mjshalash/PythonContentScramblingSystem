import os, ContentScramblingSystem

class test:
    
    # Constructor for test.py
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
        
        # Number of bytes to read in from file at a time
        fileChar = 1
        
        # Read input file as a raw bytestream
        # Write to output file with a raw bytestream
        with open(self.file_name, "rb") as fileInput, open(self.output_name, "wb") as fileOutput:
            
            while True:

                # Read in 1 byte from file aka one character
                inputChar = fileInput.read(fileChar)

                # If at end
                if inputChar == b"":
                    break

                # Retrieve ascii value for first byte
                inputCharAscii = ord(inputChar)
                
                # Use Content Scrambling System to generate random bit stream (byte)
                lsfrResult = self.css.getOutputByte()
                
                # Binary XOR the byte/character with output byte of Content Scrambling System
                # ^ is Binary XOR
                toWriteAscii = inputCharAscii ^ lsfrResult

                # Create array of bytes representing final output
                # MSB is at beginning of byte arrary
                toWriteBytes = toWriteAscii.to_bytes(1, byteorder="big")

                # Write encrypted byte to the specified output file
                fileOutput.write(toWriteBytes)



# Test Encryption (to test decryption, switch files)

# Ask user to input two seeds
# One will be three characters for the 25-bit LSFR
# One will be two characters for the 17-bit LSFR
seedOne = input("Please enter in length-three seed for 25-bit LSFR (i.e \"abc\", \"EUO\", etc.\):");
seedTwo = input("Please enter in length-two seed for 17-bit LSFR (i.e \"12\", \"25\", etc.\):");

# Create instance of test class
# Initialized with a "three" byte seed for 25-bit LSFR
# Initialized with a "two" byte seed for 17-bit LSFR
testClass = test(seedOne, seedTwo, "encryptTest.txt", "decryptTest.txt");
# testClass = test(seedOne, seedTwo, "decryptTest.txt", "encryptTest.txt");

# Run Content Scrambling System
testClass.compute()

print()





