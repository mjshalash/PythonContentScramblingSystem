# Python Content Scrambling System
A Content Scrambling Cryptography System written in Python


# General Steps for Encryption:
        # 1.) Generate a 40-bit stream to seed the two LSFRs
        # 2.) Seed the first 17-LSFR with bytes 0 and 1 (8 bits each with 1 injected in fourth bit)
        # 3.) Seed the second 25-LSFR with bytes 2, 3 and 4 (8 bits each with 1 inj. fourth bit)
        # 4.) Compute output for the 17 LSFR
        # 5.) Compute output for the 25 LSFR
        # 6.) Add the outputs of the two LSFRs together using 8-bit addition

#General Steps for Decryption:
    