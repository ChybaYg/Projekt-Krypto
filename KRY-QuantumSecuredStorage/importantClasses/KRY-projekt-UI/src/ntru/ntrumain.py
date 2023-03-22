""" Encryption and decryption using postquantum cryptography algorithm NTRU
    Main functions for key generation, encryption and decryption for NTRU
    Author: Thao Le
    email: 243759@vutbr.cz
"""

from src.ntru.ntrucipher import NtruCipher
import numpy as np
from src.ntru.mathutils import random_poly
from sympy import ZZ, Poly, isprime
import math
from src.ntru.padding import *
from sympy.abc import x
from src.utilities import log_print
from src.exceptions import OptionException

# Key generation and saving to numpy's .npz format
def generate(N, p, q, priv_key_file, pub_key_file):
    if not isprime(N):
        raise OptionException("N must be a prime")
    if math.gcd(p,q) != 1:
        raise OptionException("p and q must be co-prime")
    ntru = NtruCipher(N, p, q)
    ntru.generate_random_keys()
    h = np.array(ntru.h_poly.all_coeffs()[::-1])
    f, f_p = ntru.f_poly.all_coeffs()[::-1], ntru.f_p_poly.all_coeffs()[::-1]
    np.savez_compressed(f"out/ntru_key/{priv_key_file}", N=N, p=p, q=q, f=f, f_p=f_p)
    log_print("Private key saved to {} file".format(priv_key_file))
    np.savez_compressed(f"out/ntru_key/{pub_key_file}", N=N, p=p, q=q, h=h)
    log_print("Public key saved to {} file".format(pub_key_file))

# Encrytion of message using public key
def encrypt(pub_key_file, input_arr, bin_output=True, block=True):
    input_arr = np.unpackbits(np.frombuffer(input_arr, dtype=np.uint8))
    input_arr = np.trim_zeros(input_arr, 'b')
    log_print("POLYNOMIAL DEGREE: {}".format(max(0, len(input_arr) - 1)))
    log_print("BINARY: {}".format(input_arr))

    pub_key = np.load(pub_key_file, allow_pickle=True)
    ntru = NtruCipher(int(pub_key['N']), int(pub_key['p']), int(pub_key['q']))
    ntru.h_poly = Poly(pub_key['h'].astype(np.int)[::-1], x).set_domain(ZZ)
    if not block:
        if ntru.N < len(input_arr):
            raise Exception("Input is too large for current N")
        output = (ntru.encrypt(Poly(input_arr[::-1], x).set_domain(ZZ),
                               random_poly(ntru.N, int(math.sqrt(ntru.q)))).all_coeffs()[::-1])
    else:
        input_arr = padding_encode(input_arr, ntru.N)
        input_arr = input_arr.reshape((-1, ntru.N))
        output = np.array([])
        block_count = input_arr.shape[0]
        for i, b in enumerate(input_arr, start=1):
            log_print("Processing block {} out of {}".format(i, block_count))
            next_output = (ntru.encrypt(Poly(b[::-1], x).set_domain(ZZ),
                                        random_poly(ntru.N, int(math.sqrt(ntru.q)))).all_coeffs()[::-1])
            if len(next_output) < ntru.N:
                next_output = np.pad(next_output, (0, ntru.N - len(next_output)), 'constant')
            output = np.concatenate((output, next_output))

    if bin_output:
        k = int(math.log2(ntru.q))
        output = [[0 if c == '0' else 1 for c in np.binary_repr(n, width=k)] for n in output]
    return np.array(output).flatten()

# Decryption of message using private key
def decrypt(priv_key_file, input_arr, bin_input=True, block=True):
    input_arr = np.unpackbits(np.frombuffer(input_arr, dtype=np.uint8))
    input_arr = np.trim_zeros(input_arr, 'b')

    priv_key = np.load(priv_key_file, allow_pickle=True)
    ntru = NtruCipher(int(priv_key['N']), int(priv_key['p']), int(priv_key['q']))
    ntru.f_poly = Poly(priv_key['f'].astype(np.int)[::-1], x).set_domain(ZZ)
    ntru.f_p_poly = Poly(priv_key['f_p'].astype(np.int)[::-1], x).set_domain(ZZ)

    if bin_input:
        k = int(math.log2(ntru.q))
        pad = k - len(input_arr) % k
        if pad == k:
            pad = 0
        input_arr = np.array([int("".join(n.astype(str)), 2) for n in
                              np.pad(np.array(input_arr), (0, pad), 'constant').reshape((-1, k))])
    if not block:
        if ntru.N < len(input_arr):
            raise Exception("Input is too large for current N")
        log_print("POLYNOMIAL DEGREE: {}".format(max(0, len(input_arr) - 1)))
        return ntru.decrypt(Poly(input_arr[::-1], x).set_domain(ZZ)).all_coeffs()[::-1]
    # import pdb
    # pdb.set_trace()
    input_arr = input_arr.reshape((-1, ntru.N))
    output = np.array([])
    block_count = input_arr.shape[0]
    for i, b in enumerate(input_arr, start=1):
        log_print("Processing block {} out of {}".format(i, block_count))
        next_output = ntru.decrypt(Poly(b[::-1], x).set_domain(ZZ)).all_coeffs()[::-1]
        if len(next_output) < ntru.N:
            next_output = np.pad(next_output, (0, ntru.N - len(next_output)), 'constant')
        output = np.concatenate((output, next_output))
    return padding_decode(output, ntru.N)