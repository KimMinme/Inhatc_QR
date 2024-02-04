from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode

def get_key(file_name):
    f = open(file_name, 'r')
    key = f.read()
    f.close()

    return key.encode('utf-8')

def encrypt(text, key):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()

    # Ensure the text length is a multiple of 16 by padding
    text = text.ljust((len(text) // 16 + 1) * 16)

    ciphertext = encryptor.update(text.encode()) + encryptor.finalize()
    return b64encode(ciphertext).decode()

def decrypt(ciphertext, key):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()

    ciphertext = b64decode(ciphertext)
    decrypted_text = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_text.decode().rstrip()


if __name__ == "__main__":
    text = "Hello AES!"
    key = get_key("AES.key")

    tmp1 = encrypt(text, key)
    tmp2 = decrypt(tmp1, key)

    print(tmp1)
    print(tmp2)