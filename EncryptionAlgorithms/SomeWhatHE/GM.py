import random
import math
import time

import sympy


def generate_big_prime(size):
    k = 40
    p = random.randrange(2 ** (size - 1), 2 ** size - 1)
    if p % 2 == 0:
        p += 1
    while not is_prime(p, k):
        p += 2
    return p

def is_prime(n, k):
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)

def generate_keys(n, phi, p, q):    
    while True:
        r = generate_block_size(n, p, q) 
        y = random.randint(2, n)
        if gcd(y, n) != 1:
            continue
         
        # to guarantee correct decryption
        prime_factors = sympy.factorint(r).keys()

        decryption_guaranteed = True
        for prime_factor in prime_factors:
            # none of r's prime factor should satisfy the condition
            if pow(y, int(phi/prime_factor), n) == 1:
                decryption_guaranteed = False
        if decryption_guaranteed is False:
            # regenerate keys
            continue
         
        x = pow(y, int(phi/r), n)        
        if x != 1:
            break
             
    return r, x, y

def generate_block_size(n, p, q):
    while True:
        r = random.randint(2, n)
        if (
            # r should divide p-1 without remainder
            (p-1) % r == 0
            # r and (p - 1) / r must be coprimes
            and gcd(r, int((p - 1) / r)) == 1
            # r and q-1 must be coprimes
            and gcd(r, q - 1)
        ) == 1:
            break
    return r

def gen(security_param):
    # 1. Choose two large prime numbers
    length = security_param
    p = 10007
    q = 191
    while p == q:
        q = generate_big_prime(length)

    # 2. Calculate N = pq
    n = p * q
    phi = (p-1)*(q-1)
    
    return p, q, n, phi


def GMEncrypt(m, u, n, r, y):
    return (pow(y, m, n) * pow(u, r, n)) % n
 


def GMDecrypt(c, n, phi, r, x):
    a = pow(c, int(phi/r), n)
 
    md = 0
    while True:
        if pow(x, md, n) == a:
            break
        md = md + 1
     
    return md


def execute(result, printing:bool):
    p, q, n, phi = gen(30)
    r, x, y = generate_keys(n, phi, p, q)
    
    sum = 0
    randoms = 0
    for i in result:
        sum += i
        randoms*=(random.randint(0, n))
    print(sum)

    '''firstHalf = result[:len(result)//2]
    u1 = random.randint(0, n)
    c1 = GMEncrypt(firstHalf[0], u1,  n, r, y)   
    print("-----firstHalf ")
    print(firstHalf)

    secondHalf = result[len(result)//2:]
    u2 = random.randint(0, n)
    c2 = GMEncrypt(secondHalf[0], u2,  n, r, y)
    print("-----secondHalf ")
    print(secondHalf)    '''

    startEnc = time.time()
    #resultGM = GMEncrypt(firstHalf[0]+secondHalf[0], u1*u2, n, r, y)
    resultGM = GMEncrypt(sum, randoms, n, r, y)
    elapsed_timeEnc = startEnc - startEnc
    print("Encryption GM time spent: ")
    print(elapsed_timeEnc)

    startDec = time.time()
    resultGMDec = GMDecrypt(resultGM, n, phi, r, x)
    elapsed_timeDec = startDec - startEnc
    print("Decryption GM time spent: ")
    print(elapsed_timeDec)

    if printing:
        print("========= encrypted GM value =============")
        print(resultGM)
        print("========= decrypted GM value=============")
        print(resultGMDec)

    return resultGM,resultGMDec