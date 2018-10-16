import sys
import json
import os 
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)

#Gathering encryption data from JSON
 # AES(MSG) -> Key, IV Ciphertext, tag -> RSA.E(Key, publicKey) -> RSA.D(Key, privateKey)

def Mydecrypt(ciphertext, tag, iv, key):
  #Decrypts the ciphertext using the tag, iv and key
  decryptor = Cipher(
      algorithms.AES(key),
      modes.GCM(iv, tag),
      backend=default_backend()
  ).decryptor()
  #Returns the decrypted value
  return decryptor.update(ciphertext) + decryptor.finalize()

def RSACipher_Decrypt (jsonFile, RSAPrvKeyPath):
    
    #Unpacking JSON
    cipherTxt = base64.b64decode(jsonFile['ciphertext_base64'])
    tag = base64.b64decode(jsonFile['tag'])
    IV = base64.b64decode(jsonFile['iv'])
    rsaCipher = base64.b64decode(jsonFile['RSACipher'])

    #Serializing Private Key
    with open(RSAPrvKeyPath, 'rb') as privKeyFile:
        privKey = serialization.load_pem_private_key(privKeyFile.read(), password=None, backend=default_backend())
    privKeyFile.close()

    #Determining AES from RSACipher
    AESKey = privKey.decrypt(
        rsaCipher,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None
        )
      )
<<<<<<< HEAD

    #Decrypting message using private key
    plaintext = privKey.decrypt(
        cipherTxt,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None
        )
    )
    #If decryption works print out message
    print(plaintext)

=======
    
    plaintext = Mydecrypt(cipherTxt, tag, IV, AESKey)
    output_filename = 'finalFile' + '.txt'
    f = open(output_filename, 'wb')
    f.write(plaintext)
    f.close()
>>>>>>> f1f9fde0a3b8ac85e61d8e43635cdae61ae4b7a4


if '--d' in sys.argv and '--rsaprivkey' in sys.argv:
    with open(sys.argv[sys.argv.index('--d')+1]) as enc:
        json_file = json.load(enc)
    RSAPrvKeyPath = sys.argv[sys.argv.index('--rsaprivkey') + 1]
    RSACipher_Decrypt(json_file, RSAPrvKeyPath)
    os.remove(sys.argv[sys.argv.index('--d')+1])

