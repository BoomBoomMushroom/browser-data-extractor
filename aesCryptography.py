from Crypto.Cipher import AES

def encrypt(key, text):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(text.encode("utf8"))
    print(ciphertext)
    return ciphertext