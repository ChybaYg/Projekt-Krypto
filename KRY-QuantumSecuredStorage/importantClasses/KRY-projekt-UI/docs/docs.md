## General commands

For each of our algorithms we use different commands in format *algoritm*_*action* as can be seen bellow.  

```text
usage: kry.py [-h] [--log] [--onedir]
              {ntru_g,ntru_e,ntru_d,sphinx_sign,sphinx_verify,sign_multivariate,verify_multivariate,encrypt_mceliece,decrypt_mceliece}
              ...

positional arguments:
  {ntru_g,ntru_e,ntru_d,sphinx_sign,sphinx_verify,sign_multivariate,verify_multivariate,encrypt_mceliece,decrypt_mceliece}
                        cipher/decipher
    ntru_g              Generating key
    ntru_e              Encrypting message
    ntru_d              Decrypting message
    sphinx_sign         Signing a file
    sphinx_verify       Verifying file signature
    sign_multivariate   Signing a file
    verify_multivariate
                        Verifying file signature
    encrypt_mceliece    Encrypt file using McEliece.
    decrypt_mceliece    Decrypt file using McEliece.

optional arguments:
  -h, --help            show this help message and exit
  --log                 Log to separate file in the generated directory.
  --onedir              Save signature and public key in directory. This option will overwrite existing files.

KRY 2022 project - cipher/decipher or sign a file.


```

## SPHINX+ usage

### Sign
```text
usage: kry.py sphinx_sign [-h] file

positional arguments:
  file        Filename

optional arguments:
  -h, --help  show this help message and exit
```

### Verify

```text
usage: kry.py sphinx_verify [-h] public_key signature file

positional arguments:
  public_key  File containing public key.
  signature   File containing signature.
  file        Filename

optional arguments:
  -h, --help  show this help message and exit
```


## Examples

You can run this test by running ```make test_sphinx```. It will sign the file and then verify it. To show the functionality we change the original file and try to run verification again with (ecpected) unsuccessful result.

Signing a file.
```text
python3 kry.py --onedir sphinx_sign loremipsum.txt
```

And verifying signature.
```text
python3 kry.py --onedir sphinx_verify -s out/loremipsum.txt.signature -k out/loremipsum.txt.pbkey loremipsum.txt 
```


## Multivariate usage

### Sign
```text
usage: kry.py sign_multivariate [-h] file

positional arguments:
  file        Filename

optional arguments:
  -h, --help  show this help message and exit
```

### Verify

```text
usage: kry.py verify_multivariate [-h] public_key signature file

positional arguments:
  public_key  File containing public key.
  signature   File containing signature.
  file        Filename

optional arguments:
  -h, --help  show this help message and exit
```


## NTRU usage

### Generate
```text
usage: kry.py ntru_g [-h] parameters parameters parameters private_file public_file

positional arguments:
  parameters    N p q
  private_file  Private key Filename
  public_file   Public key Filename

optional arguments:
  -h, --help    show this help message and exit
```

### Encrypt
```text
usage: kry.py ntru_e [-h] public_key encrypted_file message

positional arguments:
  public_key
  encrypted_file
  message

optional arguments:
  -h, --help      show this help message and exit
```

### Decrypt
```text
usage: kry.py ntru_d [-h] private_key encrypted_message decrypted_file

positional arguments:
  private_key        File containing private key
  encrypted_message  File containing encrypted message
  decrypted_file     Output file

optional arguments:
  -h, --help         show this help message and exit
```


## McEliece cryptosystem

### Encrypt

```text
usage: kry.py encrypt_mceliece [-h] file

positional arguments:
  file        Filename

optional arguments:
  -h, --help  show this help message and exit
```

### Decrypt

```text
usage: kry.py decrypt_mceliece [-h] file

positional arguments:
  file        Filename

optional arguments:
  -h, --help  show this help message and exit
```