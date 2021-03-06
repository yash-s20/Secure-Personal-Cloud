import os
import binascii
import pickle
import pathlib

AES = "AES"
TripleDES = "TripleDES"


def encrypt_files(algorithm, base, encrypted_base, files, key_file=None):
    """
    Takes all file paths (relative to base) and encrypts with the same name onto encrypted_base
    :param base: home_dir for decrypted files
    :param files: list of files in base
    :param key_file: string - path to key file, not provided if user will give input
    :param encrypted_base: to store encrypted files
    :param algorithm: AES / TripleDES
    :return: boolean for success
    """
    if os.path.normpath(base) == os.path.normpath(encrypted_base):
        print("There was a problem. Try again.")
        exit(1)
    if key_file is None:
        print("Please enter the key and IV given on generation. Encryption schema-", algorithm)
        while True:
            key = input("Key: ").upper()
            if algorithm == AES or algorithm == TripleDES:
                iv = input("IV: ").upper()

            try:
                x = int(key, 16)
                if algorithm == AES or algorithm == TripleDES:
                    x = int(iv, 16)
            except ValueError:
                print("Please enter a valid hexadecimal key/iv")
                continue
            break
    else:
        with open(key_file, 'rb') as f:
            keys = pickle.load(f)
            key = keys["key"].decode('utf-8').upper()
            if algorithm == AES or algorithm == TripleDES:
                iv = keys["iv"].decode('utf-8').upper()
    if algorithm == AES:
        command = "openssl enc -aes-256-ctr -in '{0}' -out '{1}' -base64 -nosalt -K {2} -iv {3}"
    elif algorithm == TripleDES:
        command = "openssl enc -des-ede3-cfb -in '{0}' -out '{1}' -base64 -nosalt -K {2} -iv {3}"
    else:
        command = "openssl enc -rc4 -in '{0}' -out {1} -base64 -nosalt -K {2}"
    for file in files:
        inp = os.path.join(base, file)
        output = os.path.join(encrypted_base, file)
        if not os.path.isdir(os.path.dirname(output)):
            pathlib.Path(os.path.dirname(output)).mkdir(parents=True, exist_ok=True)
        if algorithm == AES or algorithm == TripleDES:
            x = os.system(command.format(inp, output, key, iv))
        else:
            x = os.system(command.format(inp, output, key))
        if x:
            print(file, base, os.path.isdir(base), os.path.isfile(os.path.join(base,file)))
            print("Something went wrong while encrypting, exiting")
            return False
    print("Files encrypted successfully.")
    return True


def decrypt_files(algorithm, encrypted_base, decrypted_base, files, key_file=None):
    """
    Takes all file paths (relative to base) and encrypts with the same name onto encrypted_base
    :param decrypted_base: path to store files
    :param files: list of files in base
    :param key_file: string - path to key file, not provided if user will give input
    :param encrypted_base: where encrypted files are stored
    :param algorithm: AES / TripleDES
    :return: boolean for success
    """
    if os.path.normpath(encrypted_base) == os.path.normpath(decrypted_base):
        print("The path to files given are the same. Please try again")
        exit(1)
    if key_file is None:
        print("Please enter the key and IV given on generation")
        while True:
            key = input("Key: ").upper()
            if algorithm == AES or algorithm == TripleDES:
                iv = input("IV: ").upper()
            try:
                x = int(key, 16)
                if algorithm == AES or algorithm == TripleDES:
                    x = int(iv, 16)
            except ValueError:
                print("Please enter a valid hexadecimal key/iv")
                continue
            break
    else:
        with open(key_file, 'rb') as f:
            keys = pickle.load(f)
            key = keys["key"].decode('utf-8').upper()
            if algorithm == AES or algorithm == TripleDES:
                iv = keys["iv"].decode('utf-8').upper()
    if algorithm == AES:
        command = "openssl enc -aes-256-ctr -d -in '{0}' -out '{1}' -base64 -nosalt -K {2} -iv {3}"
    elif algorithm == TripleDES:
        command = "openssl enc -des-ede3-cfb -d -in '{0}' -out '{1}' -base64 -nosalt -K {2} -iv {3}"
    else:
        command = "openssl enc -rc4 -d -in '{0}' -out {1} -base64 -nosalt -K {2}"
    for file in files:
        inp = os.path.join(encrypted_base, file)
        output = os.path.join(decrypted_base, file)
        if not os.path.isdir(os.path.dirname(output)):
            pathlib.Path(os.path.dirname(output)).mkdir(parents=True, exist_ok=True)
        if algorithm == AES or algorithm == TripleDES:
            x = os.system(command.format(inp, output, key, iv))
        else:
            x = os.system(command.format(inp, output, key))
        if x:
            print("Something went wrong while decrypting, exiting")
            return False

    print("Files decrypted successfully.")
    return True


# def decrypt_key(encryptedKeyFile, password, decryptedFilePath):
#     """
#     :param encryptedKeyFile: str - complete path of encrypted key
#     :param password: str
#     :param decryptedFilePath: str - complete path to store decrypted key
#     :return: void
#     """
#     command = "java KeyEncrypt {0} decrypt {1} {2}"
#     os.system(command.format(password, encryptedKeyFile, decryptedFilePath))
#
#
# def encrypt_key(decryptedKeyFile, password, encryptedFilePath):
#     """
#     :param decryptedKeyFile: str - complete path of encrypted key
#     :param password: str
#     :param encryptedFilePath: str - complete path to store decrypted key
#     :return: void
#     """
#     command = "java KeyEncrypt {0} encrypt {1} {2}"
#     os.system(command.format(password, decryptedKeyFile, encryptedFilePath))


# def change_pass(keyFile, oldpass, newpass):
#     """
#     :param keyFile: str - path to current (encrypted) key file
#     :param oldpass: str
#     :param newpass: str
#     :return: void
#     """
#     with tempfile.TemporaryDirectory as d:
#         tempKey = os.path.join(d, "temp.key")
#         decrypt_key(keyFile, oldpass, tempKey)
#         encrypt_key(tempKey, newpass, keyFile)


def generate_key(encryption_schema, key_file=None):
    """
    We're using the openssl ctr mode aes 256 bit key with random key and iv
    :param encryption_schema: string- AES / TripleDES / RSA
    :param key_file: file path chosen by user, not provided if he/she would like to manually type it on sync
    :return: boolean for success
    """
    if encryption_schema == AES:
        keylength = 32
        ivlength = 16
    elif encryption_schema == TripleDES:
        keylength = 24
        ivlength = 8
    else:
        keylength = 16

    randomKeyHex = binascii.b2a_hex(os.urandom(keylength))
    if encryption_schema == AES or encryption_schema == TripleDES:
        randomIVHex = binascii.b2a_hex(os.urandom(ivlength))
    if key_file is None:
        print("Please keep the following following information confidential, for the privacy of your files "
              "uploaded on the server.\nWe will not be responsible for any breach of privacy")
        print("AES schema chosen. Produce this key and the initialization vector when you wish to download, "
              "upload or sync.")
        print("KEY (length -", keylength, "hex characters):", randomKeyHex.decode('utf-8').upper())
        if encryption_schema == AES or encryption_schema == TripleDES:
            print("IV (length -", ivlength, "hex characters): ", randomIVHex.decode('utf-8').upper())
        return True
    else:
        print("Please keep the file extremely secure and in the same path as chosen. DO NOT delete or move the "
              "file, until a new encryption schema is chose.")
        with open(key_file, 'wb') as f:
            aeskey = {"key": randomKeyHex}
            if encryption_schema == AES or encryption_schema == TripleDES:
                aeskey["iv"] = randomIVHex
            pickle.dump(aeskey, f)
        print("Key stored successfully")
        return True
