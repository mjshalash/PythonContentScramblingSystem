import sys
import os
import random
import string
import collections
import statistics
import numpy
from scipy.stats import entropy
plainCodes = []
cipherCodes = []


def main():
    # Import ascii values from plaintext and analyze
    analyzeText()


def analyzeText():
    # Define file to be read in
    file = open("decryptTest.txt", "rb")

    # Initialize variable to hold letters in file
    plainCodes = []
    plainSymbols = []

    # Will loop until EOF reached
    while True:

        # Read in 1 byte from file aka one character
        inputChar = file.read(1)

        # If at end
        if inputChar == b"":
            break

        # Retrieve ascii value for first byte
        inputCharAscii = ord(inputChar)

        # Add ascii value to the overall array
        plainCodes.append(inputCharAscii)
        plainSymbols.append(chr(inputCharAscii))

    print("-----------Stats-----------")
    # Mode
    #plainMode = statistics.mode(plainCodes)
    #print("Mode: %d, Char: %s" % (plainMode, chr(plainMode)))

    # Mean
    plainMean = statistics.mean(plainCodes)
    print("Mean: %d, Char: %s" % (plainMean, chr(int(plainMean))))

    # Standard Deviation
    plainSTD = statistics.stdev(plainCodes)
    print("Stdev: %d," % plainSTD)

    # Median
    plainMedian = statistics.median(plainCodes)
    print("Median: %d, Char: %s" % (plainMedian, chr(int(plainMedian))))

    # Entropy
    messageStats = collections.Counter(plainSymbols)
    sortStats = sorted(messageStats)
    ent = findEntropy(sortStats, 256)
    print("Entropy: %f" % ent)

    # Variance
    plainVariance = numpy.var(plainCodes)
    print("Variance: %d" % (plainVariance))


def findEntropy(labels, base=None):
    value, counts = numpy.unique(labels, return_counts=True)
    return entropy(counts, base=base)


if __name__ == "__main__":
    main()
