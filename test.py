import os
import ContentScramblingSystem


def main():
    # TODO: Have use decide whether they want to encrypt message or decrypt message

    # Files to read and write to
    fileIn = open("decryptTest.txt", "rb")
    fileOut = open("encryptTest.txt", "wb")

    # User determines two seeds for each LSFR (one three characters, the other two characters)
    seedOne = input(
        "Please enter in length-three seed for 25-bit LSFR (i.e \"abc\", \"EUO\", etc.\):")
    seedTwo = input(
        "Please enter in length-two seed for 17-bit LSFR (i.e \"12\", \"25\", etc.\):")

    # Create instance of ContentScramblingSystem class
    cryptoSystem = ContentScramblingSystem.ContentScramblingSystem(
        seedOne, seedTwo)

    # Will loop until EOF reached
    while True:

        # Read in 1 byte from file aka one character
        inputChar = fileIn.read(1)

        # If at end
        if inputChar == b"":
            break

        # Retrieve ascii value for first byte
        inputCharAscii = ord(inputChar)

        # Use Content Scrambling System to generate random bit stream (byte)
        lsfrResult = cryptoSystem.getOutputByte()

        # Binary XOR the byte/character with output byte of Content Scrambling System
        # ^ is Binary XOR
        toWriteAscii = inputCharAscii ^ lsfrResult

        # Create array of bytes representing final output
        # MSB is at beginning of byte arrary
        toWriteBytes = toWriteAscii.to_bytes(1, byteorder="big")

        # Write encrypted byte to the specified output file
        fileOut.write(toWriteBytes)


# Main Program
if __name__ == "__main__":
    # Launch main menu
    main()
