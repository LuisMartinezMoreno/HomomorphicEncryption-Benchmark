# Cheon-Kim-Kim-Song Fully Homomorphic Encryptio with bootstrapping (CKKS-bootstrapping)
import time
from ckks.ckks_decryptor import CKKSDecryptor
from ckks.ckks_encoder import CKKSEncoder
from ckks.ckks_encryptor import CKKSEncryptor
from ckks.ckks_evaluator import CKKSEvaluator
from ckks.ckks_key_generator import CKKSKeyGenerator
from ckks.ckks_parameters import CKKSParameters
from tests.helper import check_complex_vector_approx_eq
import util.matrix_operations as mat
from util.random_sample import sample_random_complex_vector

def execute(message, printing: bool):
    """
    Execute CKKS encryption and decryption on a given message.

    Parameters:
    - message (list): List of complex numbers representing the message.
    - printing (bool): If True, print the decrypted values and similarity checks.

    Returns:
    - None
    """
    num_slots = len(message)
    poly_degree = closestPow(num_slots)
    max_size = poly_degree // 2
    ciph_modulus = 1 << 600
    big_modulus = 1 << 1200
    scaling_factor = 1 << 30
    ciph_modulus = 1 << 600
    big_modulus = 1 << 1200
    scaling_factor = 1 << 30

    # CKKS Parameters
    params = CKKSParameters(poly_degree=poly_degree,
                            ciph_modulus=ciph_modulus,
                            big_modulus=big_modulus,
                            scaling_factor=scaling_factor)

    # Key Generation
    key_generator = CKKSKeyGenerator(params)
    public_key = key_generator.public_key
    secret_key = key_generator.secret_key
    relin_key = key_generator.relin_key

    # Encoder, Encryptor, Decryptor, Evaluator
    encoder = CKKSEncoder(params)
    encryptor = CKKSEncryptor(params, public_key, secret_key)
    decryptor = CKKSDecryptor(params, secret_key)
    evaluator = CKKSEvaluator(params)

    while len(message) < max_size:
        message.append(0)

    # Encryption
    startEnc = time.time()
    num_slots = len(message)
    plain = encoder.encode(message, scaling_factor)
    plain_ans1 = mat.scalar_multiply(plain.poly.coeffs[:num_slots], 1 / scaling_factor)
    plain_ans2 = mat.scalar_multiply(plain.poly.coeffs[num_slots:], 1 / scaling_factor)
    ciph = encryptor.encrypt(plain)
    elapsed_timeEnc = time.time() - startEnc
    print("Encryption CKKS with bootstrapping time spent: ")
    print(elapsed_timeEnc)

    # Decryption
    startDec = time.time()
    rot_keys = {}
    for i in range(num_slots):
        rot_keys[i] = key_generator.generate_rot_key(i)

    conj_key = key_generator.generate_conj_key()

    ciph1, ciph2 = evaluator.coeff_to_slot(ciph, rot_keys, conj_key, encoder)
    decrypted_1 = decryptor.decrypt(ciph1)
    decrypted_1 = encoder.decode(decrypted_1)
    decrypted_2 = decryptor.decrypt(ciph2)
    decrypted_2 = encoder.decode(decrypted_2)
    elapsed_timeDec = time.time() - startDec
    
    print("Decryption CKKS with bootstrapping time spent: ")
    print(elapsed_timeDec)

    # Check similarity between decrypted values and original message
    result1 = check_complex_vector_approx_eq(plain_ans1, decrypted_1, error=0.0001)
    result2 = check_complex_vector_approx_eq(plain_ans2, decrypted_2, error=0.01)
    if printing:
        print("============= FHE algorithm =============")
        print("========= CKKS Bootstrapping first half decryption similarity =============")
        print(result1)
        print("========= CKKS Bootstrapping second half decryption similarity=============")
        print(result2)
    return elapsed_timeEnc, elapsed_timeDec

def closestPow(number):
    """
    Find the closest power of 2 greater than or equal to a given number.

    Parameters:
    - number (int): The input number.

    Returns:
    - int: The closest power of 2.
    """
    pows = []
    pow = 1

    while pow <= number:
        pows.append(pow)
        pow *= 2
    result = pows[-1] * 2 * 2
    return result
