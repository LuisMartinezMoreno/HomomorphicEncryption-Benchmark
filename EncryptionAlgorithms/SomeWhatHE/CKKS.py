# Cheon-Kim-Kim-Song Fully Homomorphic Encryption (CKKS)
import time
from ckks.ckks_encoder import CKKSEncoder
from ckks.ckks_decryptor import CKKSDecryptor
from ckks.ckks_encryptor import CKKSEncryptor
from ckks.ckks_key_generator import CKKSKeyGenerator
from ckks.ckks_parameters import CKKSParameters
from tests.helper import check_complex_vector_approx_eq

# Function to set encryption parameters and generate encoder, encryptor, and decryptor
def setValues(length):
    """
    Sets encryption parameters and generates encoder, encryptor, and decryptor.

    Parameters:
    - length: The length of the input data.

    Returns:
    - encoder: The CKKSEncoder object.
    - encryptor: The CKKSEncryptor object.
    - scaling_factor: The scaling factor used in encoding.
    - decryptor: The CKKSDecryptor object.
    """
    degree = length
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
    return encoder, encryptor, scaling_factor, decryptor

# Function to perform CKKS encryption
def CKKSEncryption(message, printing: bool, encoder, encryptor, scaling_factor):
    """
    Performs CKKS encryption.

    Parameters:
    - message: The input data to be encrypted.
    - printing: A boolean indicating whether to print additional information.
    - encoder: The CKKSEncoder object.
    - encryptor: The CKKSEncryptor object.
    - scaling_factor: The scaling factor used in encoding.

    Returns:
    - ciphertext: The encrypted data.
    """
    plain = encoder.encode(message, scaling_factor)
    ciphertext = encryptor.encrypt_with_secret_key(plain)
    return ciphertext

# Function to perform CKKS decryption
def CKKSDecryption(message, ciphertext, printing: bool, decryptor, encoder):
    """
    Performs CKKS decryption.

    Parameters:
    - message: The original input data.
    - ciphertext: The encrypted data to be decrypted.
    - printing: A boolean indicating whether to print additional information.
    - decryptor: The CKKSDecryptor object.
    - encoder: The CKKSEncoder object.

    Returns:
    - decoded: The decrypted data.
    """
    decrypted = decryptor.decrypt(ciphertext)
    decoded = encoder.decode(decrypted)

    check_complex_vector_approx_eq(message, decoded, 0.001)
    return decoded

# Function to find the closest power of 2 greater than or equal to the given number
def closestPow(number):
    """
    Finds the closest power of 2 greater than or equal to the given number.

    Parameters:
    - number: The input number.

    Returns:
    - result: The closest power of 2.
    """
    pows = []
    pow = 1

    while pow <= number:
        pows.append(pow)
        pow *= 2
    result = pows[-1] * 4
    return result

# Main function to execute CKKS encryption and decryption
def execute(result, printing: bool):
    """
    Executes CKKS encryption and decryption.

    Parameters:
    - result: The input data to be encrypted and decrypted.
    - printing: A boolean indicating whether to print additional information.

    Returns:
    - resultCKKS: The encrypted data.
    - resultCKKSDec: The decrypted data.
    """
    # Find the degree for CKKS encryption
    degree = closestPow(len(result))
    while(len(result) < degree//2):
        result.append(0)
    
    # Set encryption parameters and generate encoder, encryptor, and decryptor
    encoder, encryptor, scaling_factor, decryptor = setValues(degree)

    # Perform CKKS encryption
    startEnc = time.time()
    resultCKKS = CKKSEncryption(result, printing, encoder, encryptor, scaling_factor)
    elapsed_timeEnc = time.time() - startEnc
    print("Encryption CKKS time spent: ")
    print(elapsed_timeEnc)

    # Perform CKKS decryption
    startDec = time.time()
    resultCKKSDec = CKKSDecryption(result, resultCKKS, printing, decryptor, encoder)
    elapsed_timeDec = time.time() - startDec

    print("Decryption CKKS time spent: ")
    print(elapsed_timeDec)

    # Check if the decrypted result is approximately equal to the original result
    simResult = check_complex_vector_approx_eq(result, resultCKKSDec, 0.001)
    
    if printing:
        print("============ SwHE algorithm ================")
        print("========= encrypted CKKS value =============")
        print(resultCKKS)
        print("========= decrypted CKKS value=============")
        print(resultCKKSDec)

    return elapsed_timeEnc, elapsed_timeDec
