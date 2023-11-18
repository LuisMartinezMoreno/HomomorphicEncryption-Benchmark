from phe import paillier
import time

def paillierEncryption(arrayData):
    """
    Perform Paillier encryption on an array of numbers.

    Parameters:
    - arrayData (list): List of numbers to be encrypted.

    Returns:
    - public_key (PaillierPublicKey): Public key for encryption.
    - private_key (PaillierPrivateKey): Private key for decryption.
    - encrypted_data (list): List of encrypted numbers.
    """
    # Generate Paillier public and private keys
    public_key, private_key = paillier.generate_paillier_keypair()
    
    # Encrypt each element in the array using the public key
    encrypted_data = [public_key.encrypt(x) for x in arrayData]
    
    # Return the public key, private key, and the encrypted data
    return public_key, private_key, encrypted_data

def paillierDecryption(private_key, encrypted_data):
    """
    Perform Paillier decryption on an array of encrypted numbers.

    Parameters:
    - private_key (PaillierPrivateKey): Private key for decryption.
    - encrypted_data (list): List of encrypted numbers.

    Returns:
    - decrypted_number_list (list): List of decrypted numbers.
    """
    # Decrypt each element in the array using the private key
    decrypted_number_list = [private_key.decrypt(x) for x in encrypted_data]
    
    # Print the decrypted numbers
    print(decrypted_number_list)
    
    # Return the list of decrypted numbers
    return decrypted_number_list

def execute(result, printing: bool):
    """
    Execute Paillier encryption and decryption on a given array of numbers.

    Parameters:
    - result (list): List of numbers to be encrypted and decrypted.
    - printing (bool): If True, print the encrypted and decrypted values.

    Returns:
    - resultPaillier (list): List of encrypted numbers.
    - resultPaillierDec (list): List of decrypted numbers.
    """
    # Record the start time for encryption
    startEnc = time.time()
    
    # Perform Paillier encryption
    public_key, private_key, resultPaillier = paillierEncryption(result)
    
    # Calculate the time spent on encryption
    elapsed_timeEnc = time.time() - startEnc
    
    # Print the encryption time
    print("Encryption paillier time spent: ")
    print(elapsed_timeEnc)

    # Record the start time for decryption
    startDec = time.time()
    
    # Perform Paillier decryption
    resultPaillierDec = paillierDecryption(private_key, resultPaillier)
    
    # Calculate the time spent on decryption
    elapsed_timeDec = time.time() - startDec
    
    # Print the decryption time
    print("Decryption paillier time spent: ")
    print(elapsed_timeDec)

    # If 'printing' is True, print the encrypted and decrypted values
    if printing:
        print("========= encrypted paillier value =============")
        print(resultPaillier)
        print("========= decrypted paillier value=============")
        print(resultPaillierDec)

    # Return the encrypted result and the decrypted result
    return resultPaillier, resultPaillierDec
