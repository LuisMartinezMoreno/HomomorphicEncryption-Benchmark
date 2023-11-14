import math
import cmath
import os
import unittest

from ckks.ckks_decryptor import CKKSDecryptor
from ckks.ckks_encoder import CKKSEncoder
from ckks.ckks_encryptor import CKKSEncryptor
from ckks.ckks_evaluator import CKKSEvaluator
from ckks.ckks_key_generator import CKKSKeyGenerator
from ckks.ckks_parameters import CKKSParameters
from tests.helper import check_complex_vector_approx_eq
from util.plaintext import Plaintext
import util.matrix_operations as mat
from util.random_sample import sample_random_complex_vector
from . import similarityRate

def execute(message, printing:bool):
    poly_degree = closestPow(len(message))[-2]
    max_size = poly_degree//2
    ciph_modulus = 1 << 600
    big_modulus = 1 << 1200
    scaling_factor = 1 << 30
    degree = 16
    ciph_modulus = 1 << 600
    big_modulus = 1 << 1200
    scaling_factor = 1 << 30

    params = CKKSParameters(poly_degree=degree,
                                ciph_modulus=ciph_modulus,
                                big_modulus=big_modulus,
                                scaling_factor=scaling_factor)
    key_generator = CKKSKeyGenerator(params)
    public_key = key_generator.public_key
    secret_key = key_generator.secret_key
    relin_key = key_generator.relin_key
    encoder = CKKSEncoder(params)
    encryptor = CKKSEncryptor(params, public_key, secret_key)
    decryptor = CKKSDecryptor(params, secret_key)
    evaluator = CKKSEvaluator(params)

    dividedMessage = [message[i:i+max_size] for i in range(0, len(message), max_size)]

    num_slots = len(message)
    plain = encoder.encode(message, scaling_factor)
    plain_ans1 = mat.scalar_multiply(plain.poly.coeffs[:num_slots], 1 / scaling_factor)
    plain_ans2 = mat.scalar_multiply(plain.poly.coeffs[num_slots:], 1 / scaling_factor)
    ciph = encryptor.encrypt(plain)

    rot_keys = {}
    for i in range(num_slots):
        rot_keys[i] = key_generator.generate_rot_key(i)

    conj_key = key_generator.generate_conj_key()

    ciph1, ciph2 = evaluator.coeff_to_slot(ciph, rot_keys, conj_key, encoder)
    decrypted_1 = decryptor.decrypt(ciph1)
    decrypted_1 = encoder.decode(decrypted_1)
    decrypted_2 = decryptor.decrypt(ciph2)
    decrypted_2 = encoder.decode(decrypted_2)

    check_complex_vector_approx_eq(plain_ans1, decrypted_1, error=0.01)
    check_complex_vector_approx_eq(plain_ans2, decrypted_2, error=0.01)

def closestPow(number):
    pows = []
    pow = 1

    while pow <= number:
        pows.append(pow)
        pow *= 2

    return pows[:-1]