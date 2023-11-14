from ckks.ckks_decryptor import CKKSDecryptor
from ckks.ckks_encoder import CKKSEncoder
from ckks.ckks_encryptor import CKKSEncryptor
from ckks.ckks_evaluator import CKKSEvaluator
from ckks.ckks_key_generator import CKKSKeyGenerator
from ckks.ckks_parameters import CKKSParameters
from tests.helper import check_complex_vector_approx_eq
from . import similarityRate

def execute(message, printing:bool):
    poly_degree = closestPow(len(message))[-2]
    max_size = poly_degree//2
    ciph_modulus = 1 << 600
    big_modulus = 1 << 1200
    scaling_factor = 1 << 30

    params = CKKSParameters(poly_degree=poly_degree,
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

    multipliedResult = [1] * max_size
    encodedMessage = []
    for i in dividedMessage:
        while(len(i)<max_size):
            i.append(0)
        encodedMessage.append(encoder.encode(i, scaling_factor))
        for j in range(0,len(i)):
            multipliedResult[j] = multipliedResult[j]*i[j]

    encryptedMessage = []
    for i in encodedMessage:
        encryptedMessage.append(encryptor.encrypt(i))

    ciph_prod = encryptedMessage[0]
    for i in range(1,len(encryptedMessage)):
         ciph_prod = evaluator.multiply(encryptedMessage[i],ciph_prod, relin_key)

    decrypted_prod = decryptor.decrypt(ciph_prod)
    decoded_prod = encoder.decode(decrypted_prod)
    if(printing):
        print("========= encrypted CKKS value =============")
        print(ciph_prod)
        print("========= decrypted CKKS value =============")
        print(decoded_prod)
        print(similarityRate.checkSimilarity(multipliedResult, decoded_prod, 1e10))
    return ciph_prod, decoded_prod, similarityRate.checkSimilarity(multipliedResult, decoded_prod, 1e10)

def closestPow(number):
    pows = []
    pow = 1

    while pow <= number:
        pows.append(pow)
        pow *= 2

    return pows[:-1]