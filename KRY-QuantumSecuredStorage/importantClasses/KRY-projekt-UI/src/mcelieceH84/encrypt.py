# Encryption and generating key
from mc_core import *
import sys

def print_usage():
	print("\n\tHow to type: python encrypt.py input_file\n")
	print("\tOutput will be three files:")
	print( "\t\tinput_file.priv - private key")
	print("\t\tinput_file.pub - public key")
	print("\t\tinput_file.ctxt - encrypted file\n")

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print_usage()
		exit()
	else:
		print("Generate private key")
		tPriv = privateKeyH84()
		print("Generate public key")
		tPub = publicKeyH84(tPriv.makeGPrime())
		print("Processing encryption")
		tPub.encryptFile(sys.argv[1])
		tPriv.writeKeyToFile(str(sys.argv[1])+".priv")
		tPub.writeKeyToFile(str(sys.argv[1])+".pub")
		print("Generate key and encryption finished")
