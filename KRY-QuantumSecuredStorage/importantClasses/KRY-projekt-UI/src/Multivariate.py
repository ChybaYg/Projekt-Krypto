""" Create and verify signatures using postquantum cryptography algorithm Oil and vinegar 
    from Rainbow scheme.

    Author: Pavel Podlužanský
    email: xpodlu01@vutbr.cz
"""

from cryptovinaigrette import cryptovinaigrette

# import pyspx.shake256_128f as pysphinx
import numpy as np
from src.utilities import log_print

class Multivariate():
    """docstring for Multivariate"""
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        with open(filename, "rb") as fp:
            self.message = fp.read()

    def sign(self):
        """ signing """

        # Initialise keygen object and generate keys and save them to "out folder"
        myKeyObject = cryptovinaigrette.rainbowKeygen(save="./out/")

        # signing
        signature = cryptovinaigrette.rainbowKeygen.sign("./out/cvPriv.pem", self.filename)

        return signature

    def verify(self, signature):
        signatureList=[]
        with open(signature, "r") as fp:  # read signature file
            log_print("Making list from signature file...")
            # make list again because the external library use signature as list 
            signatureList = [int(line.strip()) for line in fp] 
        if cryptovinaigrette.rainbowKeygen.verify('./out/cvPub.pub', signatureList, self.filename):
            return 1
        return 0

