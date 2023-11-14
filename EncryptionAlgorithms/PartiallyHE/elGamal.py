import random
from math import pow
a=random.randint(2,10)
import time

#To fing gcd of two numbers
def gcd(a,b):
    if a<b:
        return gcd(b,a)
    elif a%b==0:
        return b
    else:
        return gcd(b,a%b)

#For key generation i.e. large random number
def gen_key(q):
    key= random.randint(pow(10,20),q)
    while gcd(q,key)!=1:
        key=random.randint(pow(10,20),q)
    return key

def power(a,b,c):
    x=1
    y=a
    while b>0:
        if b%2==0:
            x=(x*y)%c;
        y=(y*y)%c
        b=int(b/2)
    return x%c

#For asymetric encryption
def elGamalEncryption(msg,q,h,g, printing:bool):
    elGamalResult=[]
    k=gen_key(q)
    s=power(h,k,q)
    p=power(g,k,q)
    for i in range(0,len(msg)):
        elGamalResult.append(msg[i])
    for i in range(0,len(elGamalResult)):
        elGamalResult[i]=s*elGamalResult[i]

    if printing:
        #Result
        print("---- elGamal encryption result: ----")
        print(elGamalResult)     
    return elGamalResult,s

#For decryption
def decryption(elGamalResult, s, printing:bool):
    pt=[]
    for i in range(0,len(elGamalResult)):
        pt.append(chr(int(elGamalResult[i]/s)))
    
    if printing:
        #Result
        print("---- elGamal decryption result: ----")
        print(pt)     
    return pt
def generateKeys():
    q=random.randint(pow(10,20),pow(10,50))
    g=random.randint(2,q)
    key=gen_key(q)
    h=power(g,key,q)
    return q,g,key,h

def execute(result, printing:bool):
    startEnc = time.time()
    q,g,key,h =generateKeys()
    elGamalResult,s = elGamalEncryption(result,q,h,g, printing)
    elapsed_timeEnc = startEnc - startEnc
    print("Encryption elGamal time spent: ")
    print(elapsed_timeEnc)
    
    startEnc = time.time()
    q,g,key,h =generateKeys()
    elGamalResultDec=decryption(elGamalResult,s,printing)
    elapsed_timeEnc = startEnc - startEnc
    print("Decryption elGamal time spent: ")
    print(elapsed_timeEnc)

    return elGamalResult, elGamalResultDec