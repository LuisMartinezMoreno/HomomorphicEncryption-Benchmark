#Rivest-Shamir-Adleman
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import time
import os

def generateKeys():
    """
    Generate RSA public and private keys and save them to files.

    Saves private key to "privateRSA.pem" and public key to "receiverRSA.pem".
    """
    key = RSA.generate(2048)
    private_key = key.export_key()
    file_out = open("privateRSA.pem", "wb")
    file_out.write(private_key)
    file_out.close()

    public_key = key.publickey().export_key()
    file_out = open("receiverRSA.pem", "wb")
    file_out.write(public_key)
    file_out.close()

def RSAEncryption(arrayData):
    """
    Encrypt an array of data using RSA encryption.

    Parameters:
    - arrayData (list): List of data to be encrypted.

    Returns:
    - encrypted_data (bytes): Encrypted data.
    """
    data = str(arrayData).encode("utf-8")
    file_out = open("encrypted_dataRSA.bin", "wb")

    recipient_key = RSA.import_key(open("receiverRSA.pem").read())
    session_key = get_random_bytes(16)

    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    encrypted_data, tag = cipher_aes.encrypt_and_digest(data)
    [file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, encrypted_data)]
    file_out.close()

    return encrypted_data

def RSADecryption(encrypted_data):
    """
    Decrypt data using RSA decryption.

    Parameters:
    - encrypted_data (bytes): Encrypted data.

    Returns:
    - decrypted_number_list (str): Decrypted data as a string.
    """
    # Read encrypted file and retrieve private key
    file_in = open("encrypted_dataRSA.bin", "rb")
    private_key = RSA.import_key(open("privateRSA.pem").read())
    BLOCK_SIZE = 16
    enc_session_key, nonce, tag, ciphertext = \
        [file_in.read(x) for x in (private_key.size_in_bytes(), BLOCK_SIZE, BLOCK_SIZE, -1)]
    file_in.close()

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    decrypted_number_list = data.decode("utf-8")
    return decrypted_number_list

def removeFiles():
    """
    Remove temporary files generated during RSA encryption and decryption.
    """
    os.remove("encrypted_dataRSA.bin")
    os.remove("privateRSA.pem")
    os.remove("receiverRSA.pem")

def execute(result, printing: bool):
    """
    Execute RSA encryption and decryption on a given array of data.

    Parameters:
    - result (list): List of data to be encrypted and decrypted.
    - printing (bool): If True, print the encrypted and decrypted values.

    Returns:
    - resultRSA (bytes): Encrypted data.
    - resultRSADec (str): Decrypted data.
    """
    # Encryption
    startEnc = time.time()
    generateKeys()
    resultRSA = RSAEncryption(result)
    elapsed_timeEnc = time.time() - startEnc
    print("Encryption RSA time spent: ")
    print(elapsed_timeEnc)

    # Decryption
    startDec = time.time()
    resultRSADec = RSADecryption(resultRSA)
    elapsed_timeDec = time.time() - startDec
    print("Decryption RSA time spent: ")
    print(elapsed_timeDec)
    removeFiles()

    if printing:
        print("============ PHE algorithm ================")
        print("========= encrypted RSA value =============")
        print(resultRSA)
        print("========= decrypted RSA value=============")
        print(resultRSADec)

    return elapsed_timeEnc, elapsed_timeDec
