from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import time
import os


"""Generate keys for encryption and decryption, those keys are stored

    Returns: Nothing
    """
def generateKeys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    file_out = open("privateRSA.pem", "wb")
    file_out.write(private_key)
    file_out.close()

    public_key = key.publickey().export_key()
    file_out = open("receiverRSA.pem", "wb")
    file_out.write(public_key)
    file_out.close()

   
"""Encrypts the given data and stores it in a file

    Parameters:
    - arrayData: provided data
    - printing: if true the result is printed

    Returns:
    arrayData encrypted
    """
def RSAEncryption(arrayData, printing:bool):
    #read provided data
    data = str(arrayData).encode("utf-8")
    file_out = open("encrypted_dataRSA.bin", "wb")

    #Create keys and store them
    recipient_key = RSA.import_key(open("receiverRSA.pem").read())
    session_key = get_random_bytes(16)

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    encrypted_data, tag = cipher_aes.encrypt_and_digest(data)
    [ file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, encrypted_data) ]
    file_out.close()

    #Result
    if printing: 
        print("---- RSA encryption result: ----")
        print(encrypted_data)
    return encrypted_data



def RSADecryption(encrypted_data, printing:bool):
    #Read encrypted file and retrieve privKey
    file_in = open("encrypted_dataRSA.bin", "rb")
    private_key = RSA.import_key(open("privateRSA.pem").read())
    BLOCK_SIZE = 16
    enc_session_key, nonce, tag, ciphertext = \
    [file_in.read(x) for x in (private_key.size_in_bytes(), BLOCK_SIZE, BLOCK_SIZE, -1) ]
    file_in.close()

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    decrypted_number_list = data.decode("utf-8")

    if printing:
        #Result
        print("---- RSA decryption result: ----")
        print(decrypted_number_list)                            
    return decrypted_number_list

def removeFiles():
    os.remove("encrypted_dataRSA.bin")
    os.remove("privateRSA.pem")
    os.remove("receiverRSA.pem")

def execute(result, printing:bool):
    #Encryption
    startEnc = time.time()
    generateKeys()
    resultRSA = RSAEncryption(result, printing)
    elapsed_timeEnc = startEnc - startEnc
    print("Encryption RSA time spent: ")
    print(elapsed_timeEnc)

    #Decryption
    startDec = time.time()
    resultRSADec = RSADecryption(resultRSA, printing)
    elapsed_timeDec = startDec - startEnc
    print("Decryption RSA time spent: ")
    print(elapsed_timeDec)
    removeFiles()
    
    return resultRSA,resultRSADec
