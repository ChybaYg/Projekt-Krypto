""" Create and verify signatures using postquantum cryptography algorithm SPHINX+

    Author: Jakub Sencak
    email: xsenca00@vutbr.cz
"""

import pyspx.shake256_128f as pysphinx
import numpy as np
from src.utilities import log_print

class PySPHINXplus():
    """docstring for PySPHINXPLUS"""
    def __init__(self, filename):
        super().__init__()
        with open(filename, "rb") as fp:
            self.message = fp.read()

    def sign(self):
        """ signing 
            return: public_key, secret_key, signature
        """
        # generate random seed
        seed = np.random.bytes(pysphinx.crypto_sign_SEEDBYTES)
        # generating key pair
        public_key, secret_key = pysphinx.generate_keypair(seed)
        # signing
        signature = pysphinx.sign(self.message, secret_key)
        return public_key, secret_key, signature    

    def verify(self, signature, public_key):
        """ Verifing signature 
            signature: filename contatining signature 
            public_key: filename containing public key 

            return: boolean value
        """
        with open(signature, "rb") as fp:  # read signature file
            signature = fp.read()
        with open(public_key, "rb") as fp:  # read public key file
            public_key = fp.read()

        # Verify the signature
        if pysphinx.verify(self.message, signature, public_key):
            return 1
        return 0
