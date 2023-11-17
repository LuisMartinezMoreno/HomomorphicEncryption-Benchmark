#BFV (Brakerski-Vaikuntanathan-Fan)
import os
import unittest
from bfv.bfv_decryptor import BFVDecryptor
from bfv.bfv_encryptor import BFVEncryptor
from bfv.bfv_key_generator import BFVKeyGenerator
from bfv.bfv_parameters import BFVParameters
from util.plaintext import Plaintext
from util.polynomial import Polynomial
from util.random_sample import sample_uniform
import similarityRate

def execute(message, printing:True):
    poly_degree = closestPow(len(message))
    large_plain_modulus = 256
    large_ciph_modulus = 0x3fffffff000001

    params = BFVParameters(poly_degree=poly_degree,
                               plain_modulus=large_plain_modulus,
                               ciph_modulus=large_ciph_modulus)
    key_generator = BFVKeyGenerator(params)
    public_key = key_generator.public_key
    secret_key = key_generator.secret_key
    encryptor = BFVEncryptor(params, public_key)
    decryptor = BFVDecryptor(params, secret_key)
    while(len(message)<poly_degree):
        message.append(0)
    messagePre = message
    message = Plaintext(Polynomial(poly_degree, message))
    ciphertext = encryptor.encrypt(message)
    decrypted_message = decryptor.decrypt(ciphertext)
    if(printing):
        print("========= encrypted BFV value =============")
        print(ciphertext)
        print("========= decrypted BFV value =============")
        print(decrypted_message)
        print("========= Similarity BFV value =============")
        print(str(message) == str(decrypted_message))

def closestPow(number):
    pows = []
    pow = 1

    while pow <= number:
        pows.append(pow)
        pow *= 2
    result = pows[-1]*2
    return result