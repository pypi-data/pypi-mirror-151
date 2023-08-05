plaintext = str(input("Enter the msg: "))
key = int(input("Enter a single digit: "))

def pad(text):
    while len(text)%key !=0:
        text += " "
    return text

plaintext = pad(plaintext)

ciphertext = ['']*key

for col in range(key):
    pointer = col
    while pointer < len(plaintext):
        ciphertext[col] += plaintext[pointer]

        pointer += key

secret = ''.join(ciphertext)
print("Encrypted:",secret)
leng = len(ciphertext[0])

plain = ['']*leng
for col in range(leng):
    pointer = col
    while pointer < len(secret):
        plain[col] += secret[pointer]

        pointer += leng
result = ''.join(plain)

print("Decrypted: ",result)

# Enter the msg: Hello there boys
# Enter the key in single digit: 5
# Encryption:  H eset  lhb leo ory 
# Decryption:  Hello there boys