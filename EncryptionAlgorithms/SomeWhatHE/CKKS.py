# Cheon-Kim-Kim-Song Fully Homomorphic Encryption (CKKS)
import os
import time
from ckks.ckks_encoder import CKKSEncoder
from ckks.ckks_decryptor import CKKSDecryptor
from ckks.ckks_encryptor import CKKSEncryptor
from ckks.ckks_key_generator import CKKSKeyGenerator
from ckks.ckks_parameters import CKKSParameters
from tests.helper import check_complex_vector_approx_eq
from util.random_sample import sample_random_complex_vector

degree = 16
ciph_modulus = 1 << 1200
big_modulus = 1 << 1200
scaling_factor = 1 << 30
params = CKKSParameters(
    poly_degree=degree,
    ciph_modulus=ciph_modulus,
    big_modulus=big_modulus,
    scaling_factor=scaling_factor,
)
key_generator = CKKSKeyGenerator(params)
public_key, secret_key = key_generator.public_key, key_generator.secret_key
encoder, encryptor, decryptor = (
    CKKSEncoder(params),
    CKKSEncryptor(params, public_key, secret_key),
    CKKSDecryptor(params, secret_key),
)

def CKKSEncryption(message, printing: bool):
    plain = encoder.encode(message, scaling_factor)
    ciphertext = encryptor.encrypt_with_secret_key(plain)

    return ciphertext


def CKKSDecryption(message, ciphertext, printing: bool):
    decrypted = decryptor.decrypt(ciphertext)
    decoded = encoder.decode(decrypted)

    check_complex_vector_approx_eq(message, decoded, 0.001)
    return decoded


def execute(result, printing: bool):
    # Encryption
    startEnc = time.time()
    resultCKKS = CKKSEncryption(result, printing)
    elapsed_timeEnc = startEnc - startEnc
    print("Encryption CKKS time spent: ")
    print(elapsed_timeEnc)

    # Decryption
    startDec = time.time()
    resultCKKSDec = CKKSDecryption(result, resultCKKS, printing)
    elapsed_timeDec = startDec - startEnc

    print("Decryption CKKS time spent: ")
    print(elapsed_timeDec)

    if printing:
        print("========= encrypted CKKS value =============")
        print(resultCKKS)
        print("========= decrypted CKKS value=============")
        print(resultCKKSDec)

    return resultCKKS, resultCKKSDec
