import os
import ContentScramblingSystem


def main():

    fileIn = open("encryptTest.txt", "rb")
    fileOut = open("decryptTest.txt", "wb")

    seedOne = input(
        "Please enter in length-three seed for 25-bit LSFR (i.e \"abc\", \"EUO\", etc.\):")
    seedTwo = input(
        "Please enter in length-two seed for 17-bit LSFR (i.e \"12\", \"25\", etc.\):")

    cryptoSystem = ContentScramblingSystem.ContentScramblingSystem(
        seedOne, seedTwo)

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
