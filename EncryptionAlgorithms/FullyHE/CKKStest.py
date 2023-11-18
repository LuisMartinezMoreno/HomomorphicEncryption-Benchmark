import os
import unittest
from ckks.ckks_encoder import CKKSEncoder
from ckks.ckks_decryptor import CKKSDecryptor
from ckks.ckks_encryptor import CKKSEncryptor
from ckks.ckks_key_generator import CKKSKeyGenerator
from ckks.ckks_parameters import CKKSParameters
from tests.helper import check_complex_vector_approx_eq
from util.plaintext import Plaintext
from util.polynomial import Polynomial
from util.random_sample import sample_random_complex_vector

def execute(message):
        degree = 16
        ciph_modulus = 1 << 1200
        big_modulus = 1 << 1200
        scaling_factor = 1 << 30
        params = CKKSParameters(poly_degree=degree,
                                     ciph_modulus=ciph_modulus,
                                     big_modulus=big_modulus,
                                     scaling_factor=scaling_factor)
        key_generator = CKKSKeyGenerator(params)
        public_key = key_generator.public_key
        secret_key = key_generator.secret_key
        encoder = CKKSEncoder(params)
        encryptor = CKKSEncryptor(params, public_key, secret_key)
        decryptor = CKKSDecryptor(params, secret_key)


        plain = encoder.encode(message, scaling_factor)

        ciphertext = encryptor.encrypt(plain)
        decrypted = decryptor.decrypt(ciphertext)
        decoded = encoder.decode(decrypted)
        print(decoded)
        check_complex_vector_approx_eq(message, decoded, 0.1)