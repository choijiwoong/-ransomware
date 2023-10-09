from Crypto.Cipher import AES
import os

enc_key = os.urandom(16)  
init_vec = os.urandom(16)  

data_to_encrypt = b'Hello World.'

block_size = 16
padding = block_size - (len(data_to_encrypt) % block_size)
data_to_encrypt += bytes([padding]) * padding

cipher = AES.new(enc_key, AES.MODE_CBC, init_vec)

encrypted_data = cipher.encrypt(data_to_encrypt)

with open('encrypted_data.bin', 'wb') as f:
    f.write(encrypted_data)

with open('encrypted_data.bin', 'rb') as f:
	encrypted_data = f.read()

decipher = AES.new(enc_key, AES.MODE_CBC, init_vec)

decrypted_data = decipher.decrypt(encrypted_data)

print("Decrypted Data: ", decrypted_data)
