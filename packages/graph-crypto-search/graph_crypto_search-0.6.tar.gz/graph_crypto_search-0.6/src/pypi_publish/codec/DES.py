from Crypto.Cipher import DES
from secrets import token_bytes

key = token_bytes(8)

def encrypt(msg):
    cipher = DES.new(key, DES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(msg.encode('ascii'))
    return ciphertext, tag, nonce

def decrypt(ciphertext, tag, nonce):
    cipher = DES.new(key, DES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    try:
        cipher.verify(tag)
        return plaintext.decode('ascii')
    except:
        return False

# Driver of the program
ciphertext, tag, nonce = encrypt(input("Enter a message: "))
plaintext = decrypt(ciphertext, tag, nonce)

print(f'Ciphertext DES: {ciphertext}')

if not plaintext:
    print("Message is corrupted")
else:
    print(f'Plaintext: {plaintext}')

