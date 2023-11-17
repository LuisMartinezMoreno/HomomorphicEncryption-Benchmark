from phe import paillier
import time

def paillierEncryption(arrayData):

    public_key, private_key = paillier.generate_paillier_keypair()
    encrypted_data = [public_key.encrypt(x) for x in arrayData]
    '''print("Paillier encryption result: ")
    print(encrypted_data)'''
    return public_key, private_key, encrypted_data

def paillierDecryption(private_key, encrypted_data):
    decrypted_number_list = [private_key.decrypt(x) for x in encrypted_data]
    print(decrypted_number_list)
    return decrypted_number_list

def execute(result, printing:bool):
    startEnc = time.time()
    public_key, private_key, resultPaillier = paillierEncryption(result)
    elapsed_timeEnc = startEnc - startEnc
    print("Encryption paillier time spent: ")
    print(elapsed_timeEnc)

    startDec = time.time()
    resultPaillierDec = paillierDecryption(private_key, resultPaillier)
    elapsed_timeDec = startDec - startEnc
    print("Decryption paillier time spent: ")
    print(elapsed_timeDec)

    if printing:
        print("========= encrypted paillier value =============")
        print(resultPaillier)
        print("========= decrypted paillier value=============")
        print(resultPaillierDec)

    return resultPaillier,resultPaillierDec
