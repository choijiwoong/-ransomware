from Crypto.Cipher import AES
from Crypto.Util import Counter
import os

# AES decryption function
def decrypt_aes_ctr(encrypted_data, aes_key, iv):
    # Create a counter object for AES-CTR mode with a 128-bit block size.
    ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))
    cipher = AES.new(aes_key, AES.MODE_CTR, counter=ctr)
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data

# Decrypt a file using AES-256 CTR mode.
def decrypt_file(file_path, key, IV):
    try:
        with open(file_path, 'rb+') as file:
            # Define the byte_size to read from the beginning of each file.
            byte_size = 256  # Fixed byte size

            binary_data = file.read(byte_size)
            decrypted_data = decrypt_aes_ctr(binary_data, key, IV)
            file.seek(0)
            file.write(decrypted_data)
            return True
    except Exception as e:
        # Do not print the error message and file path.
        return False

# Decrypt all files in a folder and its subfolders.
def decrypt_files_in_folder(decrypt_folder_path, key, IV):
    file_list = []
    extensions = ('zip', 'hwp', 'hwpx', 'xlsx', 'docx', 'pptx', 'pdf')

    decryption_successful = True

    for root, dirs, files in os.walk(decrypt_folder_path):
        for file in files:
            ext = file.lower().split('.')[-1]
            if ext in extensions:
                file_path = os.path.join(root, file)
                success = decrypt_file(file_path, key, IV)
                if not success:
                    decryption_successful = False

    print_decryption_result(decryption_successful)

# Print success or failure of decryption.
def print_decryption_result(successful):
    if successful:
        print("Decryption Successful!")
    else:
        print("Decryption Failed for some files!")

if __name__ == "__main__":
    # Input AES key as a 48-byte hexadecimal string.
    combine_key_hex = input("AES Key (48 bytes in hex): ").strip()

    # Convert hexadecimal string to bytes.
    combine_key_bytes = bytes.fromhex(combine_key_hex)

    # Extract the first 32 bytes as the encryption key and the next 16 bytes as the IV.
    key = combine_key_bytes[:32]
    IV = combine_key_bytes[32:]

    # Specify the input folder path for decryption.
    decrypt_folder_path = 'C:/'  # Enter the desired folder path here.

    decrypt_files_in_folder(decrypt_folder_path, key, IV)
