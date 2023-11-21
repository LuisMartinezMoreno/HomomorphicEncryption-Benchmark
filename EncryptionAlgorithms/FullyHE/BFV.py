import time
from bfv.bfv_decryptor import BFVDecryptor
from bfv.bfv_encryptor import BFVEncryptor
from bfv.bfv_key_generator import BFVKeyGenerator
from bfv.bfv_parameters import BFVParameters
from util.plaintext import Plaintext
from util.polynomial import Polynomial
from util.random_sample import sample_uniform

def execute(message, printing=True):
    """
    Executes the BFV (Brakerski-Vaikuntanathan-Fan) encryption and decryption process on a given message.

    Parameters:
    - message (list): The message to be encrypted and decrypted.
    - printing (bool): If True, print details of the encryption and decryption process. Default is True.

    Returns:
    - tuple: A tuple containing the time spent on encryption and decryption, respectively.

    Example:
    >>> execute([1, 2, 3], printing=True)
    """
    # Determine the polynomial degree and set modulus values
    poly_degree = closestPow(len(message))
    large_plain_modulus = 1024
    large_ciph_modulus = 0x3fffffff000001

    # Set BFV parameters
    params = BFVParameters(poly_degree=poly_degree,
                           plain_modulus=large_plain_modulus,
                           ciph_modulus=large_ciph_modulus)

    # Generate keys
    key_generator = BFVKeyGenerator(params)
    public_key = key_generator.public_key
    secret_key = key_generator.secret_key

    # Ensure the message length is at least poly_degree
    while len(message) < poly_degree:
        message.append(0)

    # Encryption
    start_enc = time.time()
    encryptor = BFVEncryptor(params, public_key)
    message = Plaintext(Polynomial(poly_degree, message))
    ciphertext = encryptor.encrypt(message)
    elapsed_time_enc = time.time() - start_enc
    print("Encryption BFV time spent: ")
    print(elapsed_time_enc)

    # Decryption
    start_dec = time.time()
    decryptor = BFVDecryptor(params, secret_key)
    decrypted_message = decryptor.decrypt(ciphertext)
    elapsed_time_dec = time.time() - start_dec
    print("Decryption BFV time spent: ")
    print(elapsed_time_dec)

    # Printing details if specified
    if printing:
        print("============= FHE algorithm =============")
        print("========= encrypted BFV value =============")
        print(ciphertext)
        print("========= decrypted BFV value =============")
        print(decrypted_message)
        print("========= Similarity BFV value =============")
        print(str(message) == str(decrypted_message))

    return elapsed_time_enc, elapsed_time_dec

def closestPow(number):
    """
    Finds the closest power of 2 greater than or equal to the given number.

    Parameters:
    - number (int): The input number.

    Returns:
    - int: The closest power of 2 greater than or equal to the input number.

    Example:
    >>> closestPow(10)
    """
    pows = []
    pow_val = 1

    while pow_val <= number:
        pows.append(pow_val)
        pow_val *= 2

    result = pows[-1] * 2
    return result
