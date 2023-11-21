import random
from math import pow
import time

def gcd(a, b):
    """
    Find the greatest common divisor (gcd) of two numbers.

    Parameters:
    - a (int): First number.
    - b (int): Second number.

    Returns:
    - int: GCD of the two numbers.
    """
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b
    else:
        return gcd(b, a % b)

def gen_key(q):
    """
    Generate a large random number for key generation.

    Parameters:
    - q (int): Upper limit for the random number.

    Returns:
    - int: Generated key.
    """
    key = random.randint(pow(10, 20), q)
    while gcd(q, key) != 1:
        key = random.randint(pow(10, 20), q)
    return key

def power(a, b, c):
    """
    Calculate (a^b) % c using the square and multiply method.

    Parameters:
    - a (int): Base.
    - b (int): Exponent.
    - c (int): Modulus.

    Returns:
    - int: Result of (a^b) % c.
    """
    x = 1
    y = a
    while b > 0:
        if b % 2 == 0:
            x = (x * y) % c
        y = (y * y) % c
        b = int(b / 2)
    return x % c

def elGamalEncryption(msg, q, h, g, printing: bool):
    """
    Perform ElGamal encryption on a message.

    Parameters:
    - msg (str): Message to be encrypted.
    - q (int): Prime number.
    - h (int): Public key.
    - g (int): Generator.
    - printing (bool): If True, print the encrypted result.

    Returns:
    - elGamalResult (list): List of encrypted values.
    - s (int): Session key.
    """
    elGamalResult = []
    k = gen_key(q)
    s = power(h, k, q)
    p = power(g, k, q)
    for i in range(0, len(msg)):
        elGamalResult.append(msg[i])
    for i in range(0, len(elGamalResult)):
        elGamalResult[i] = s * elGamalResult[i]

    return elGamalResult, s

def decryption(elGamalResult, s, printing: bool):
    """
    Perform ElGamal decryption on an encrypted result.

    Parameters:
    - elGamalResult (list): List of encrypted values.
    - s (int): Session key.
    - printing (bool): If True, print the decrypted result.

    Returns:
    - pt (list): List of decrypted characters.
    """
    pt = []
    for i in range(0, len(elGamalResult)):
        pt.append(chr(int(elGamalResult[i] / s)))
     
    return pt

def generateKeys():
    """
    Generate ElGamal keys (q, g, key, h).

    Returns:
    - q (int): Prime number.
    - g (int): Generator.
    - key (int): Generated key.
    - h (int): Public key.
    """
    q = random.randint(pow(10, 20), pow(10, 50))
    g = random.randint(2, q)
    key = gen_key(q)
    h = power(g, key, q)
    return q, g, key, h

def execute(result, printing: bool):
    """
    Execute ElGamal encryption and decryption on a given message.

    Parameters:
    - result (str): Message to be encrypted and decrypted.
    - printing (bool): If True, print the encrypted and decrypted values.

    Returns:
    - elGamalResult (list): List of encrypted values.
    - elGamalResultDec (list): List of decrypted characters.
    """
    # Encryption
    startEnc = time.time()
    q, g, key, h = generateKeys()
    elGamalResult, s = elGamalEncryption(result, q, h, g, printing)
    elapsed_timeEnc = time.time() - startEnc
    print("Encryption ElGamal time spent: ")
    print(elapsed_timeEnc)
    
    # Decryption
    startDec = time.time()
    elGamalResultDec = decryption(elGamalResult, s, printing)
    elapsed_timeDec = time.time() - startDec
    print("Decryption ElGamal time spent: ")
    print(elapsed_timeDec)

    if printing:
        print("============ PHE algorithm ================")
        print("========= encrypted ElGamal value =============")
        print(elGamalResult)
        print("========= decrypted ElGamal value=============")
        print(elGamalResultDec)

    return elapsed_timeEnc, elapsed_timeDec
