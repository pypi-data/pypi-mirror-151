from Crypto.Cipher import AES
from secrets import token_bytes

key = token_bytes(16)

def encrypt(msg):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce

    ciphertext, tag = cipher.encrypt_and_digest(msg.encode('ascii'))
    return nonce, tag, ciphertext

def decrypt(tag, ciphertext, nonce):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    try:
        cipher.verify(tag)
        return plaintext.decode('ascii')
    except:
        return False

nonce, tag, ciphertext = encrypt(input('Enter the message: '))
plaintext = decrypt(tag, ciphertext, nonce)
print(f'Ciphertext is {ciphertext}')
if not plaintext:
    print('Message corrupted')
else:
    print(f'Plaintext is {plaintext}')



