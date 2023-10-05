from Crypto.Cipher import AES
from Crypto.Util import Counter
import os
import binascii

# AES decryption function
def decrypt_aes_ctr(encrypted_data, key, iv):
    # Create a counter object for AES-CTR mode with a 128-bit block size.
    ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    
    # Decrypt the encrypted_data using AES-CTR mode.
    decrypted_data = cipher.decrypt(encrypted_data)
    
    return decrypted_data

if __name__ == "__main__":
    # Input the AES key as a 48-byte hexadecimal string.
    key_hex = input("AES Key (48 bytes in hex): ").strip()

    # Convert the hexadecimal string to bytes.
    key_bytes = bytes.fromhex(key_hex)

    # Extract the first 32 bytes as the encryption key and the next 16 bytes as the IV.
    aes_key = key_bytes[:32]
    iv = key_bytes[32:]

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
    
    decryption_successful = True  # Flag to track decryption success

    for file_path in file_list:
        try:
            with open(file_path, 'rb+') as file:
                # Read the first byte_size bytes of the file as binary data.
                binary_data = file.read(byte_size)

                # Decrypt the binary_data using AES-256 CTR mode with the provided key and IV.
                decrypted_data = decrypt_aes_ctr(binary_data, aes_key, iv)

                # Seek back to the beginning of the file and write the decrypted_data.
                file.seek(0)
                file.write(decrypted_data)

                # Print the results.
                print(f"File partially decrypted: {file_path}")
                # print("AES-CTR Decrypted Hex value:", binascii.hexlify(decrypted_data).decode('utf-8').upper())

        except Exception as e:
            print(f"An error occurred for file {file_path}: {e}")
            decryption_successful = False

    if decryption_successful:
        print("Decryption Successful!")  # Print a success message if all files are successfully decrypted
    else:
        print("Decryption Failed for some files!")  # Print a failure message if decryption failed for some files
