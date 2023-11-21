import sympy
from Crypto.Util.number import GCD
import random, time

# Parameters
p = 10007
q = 191
n = p * q
phi = (p - 1) * (q - 1)
m = 17

# Function to generate a block size 'r' for the encryption scheme
def generate_block_size():
    """
    Generates a block size 'r' for the encryption scheme.

    Returns:
    - r: The generated block size.
    """
    while True:
        r = random.randint(2, n)

        if (
            # r should divide (p - 1) without remainder
            (p - 1) % r == 0
            # r and (p - 1) / r must be coprimes
            and GCD(r, int((p - 1) / r)) == 1
            # r and (q - 1) must be coprimes
            and GCD(r, q - 1)
        ) == 1:
            break
    return r

# Function to generate public and private keys for the encryption scheme
def generate_keys():
    """
    Generates public and private keys for the encryption scheme.

    Returns:
    - r: Private key component.
    - x: Private key component.
    - y: Public key component.
    """
    while True:
        r = generate_block_size()

        y = random.randint(2, n)
        if GCD(y, n) != 1:
            continue

        # To guarantee correct decryption, check prime factors of 'r'
        prime_factors = sympy.factorint(r).keys()

        decryption_guaranteed = True
        for prime_factor in prime_factors:
            # None of 'r's prime factors should satisfy the condition
            if pow(y, int(phi / prime_factor), n) == 1:
                decryption_guaranteed = False
        if decryption_guaranteed is False:
            # Regenerate keys if decryption is not guaranteed
            continue

        x = pow(y, int(phi / r), n)
        if x != 1:
            break

    return r, x, y

# Function to decrypt a ciphertext 'c' using private key components 'x' and 'r'
def decrypt(c, x, r):
    """
    Decrypts a ciphertext 'c' using private key components 'x' and 'r'.

    Parameters:
    - c: Ciphertext to be decrypted.
    - x: Private key component.
    - r: Private key component.

    Returns:
    - md: Decrypted message.
    """
    a = pow(c, int(phi / r), n)

    md = 0
    while True:
        if pow(x, md, n) == a:
            break
        md = md + 1

    return md

# Function to encrypt a message 'm' using public key components 'u', 'y', and 'r'
def encrypt(m, u, y, r):
    """
    Encrypts a message 'm' using public key components 'u', 'y', and 'r'.

    Parameters:
    - m: Message to be encrypted.
    - u: Public key component.
    - y: Public key component.
    - r: Private key component.

    Returns:
    - ciphertext: Encrypted message.
    """
    return (pow(y, m, n) * pow(u, r, n)) % n

# Main function to execute Benaloh's scheme on a given result list
def execute(result, printing: bool):
    """
    Executes Benaloh's scheme on a given result list.

    Parameters:
    - result: List of values to be encrypted and decrypted.
    - printing: A boolean indicating whether to print additional information.
    """
    # Generate public and private keys
    r, x, y = generate_keys()

    # Constants
    maxValue = (n // 1000)
    sumValues = 0
    multValues = 1
    multRandoms = 1

    # Encrypt each element in the result list and compute aggregate values
    for i in result:
        sumValues += i
        u = random.randint(0, maxValue)
        multRandoms *= u
        multValues *= encrypt(i, u, y, r)

    startEnc = time.time()
    # Encrypt the sum of values
    encryptResultBenaloh = encrypt(sumValues, random.randint(0, n), y, r)
    elapsed_timeEnc = time.time() - startEnc
    print("Encryption Benaloh time spent: ")
    print(elapsed_timeEnc)

    startDec = time.time()
    # Decrypt the product of encrypted values
    decryptedResultBenaloh = decrypt((multValues) % n, x, r)
    elapsed_timeDec = time.time() - startDec
    print("Decryption Benaloh time spent: ")
    print(elapsed_timeDec)

    if printing:
        print("============ SwHE algorithm ================")
        print("========= plaintext benaloh value =============")
        print(sumValues)
        print("========= encrypted benaloh value =============")
        print(encryptResultBenaloh)
        print("========= decrypted benaloh value=============")
        print(decryptedResultBenaloh)
    return elapsed_timeEnc, elapsed_timeDec