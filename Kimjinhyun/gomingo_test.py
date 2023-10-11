# 암호화 복호화 메뉴로 구현한 코드!!!!!!!!!

from Crypto.Cipher import AES
from Crypto.Util import Counter
import os
import base64

def encrypt_file(input_file, output_file, key):
    # AES 블록 크기
    block_size = 16

    # 암호화할 파일 열기
    with open(input_file, 'rb') as f_in:
        plaintext = f_in.read()

    # 파일 확장자 추출
    ext_index = input_file.rfind('.')
    file_extension = input_file[ext_index:].encode('utf-8')
    plaintext += file_extension

    # 초기화 벡터(IV) 생성
    iv = os.urandom(block_size)

    # 카운터 생성
    counter = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))

    # AES 암호화 객체 생성
    cipher = AES.new(key, AES.MODE_CTR, counter=counter)

    # 암호문 생성
    ciphertext = cipher.encrypt(plaintext)

    # 초기화 벡터와 암호문을 출력 파일에 저장
    with open(output_file, 'wb') as f_out:
        f_out.write(iv + ciphertext)

def decrypt_file(input_file, output_dir, key):
    # AES 블록 크기
    block_size = 16

    # 암호문 파일 열기
    with open(input_file, 'rb') as f_in:
        data = f_in.read()

    # 초기화 벡터(IV) 추출
    iv = data[:block_size]
    ciphertext = data[block_size:]

    # 카운터 생성
    counter = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))

    # AES 복호화 객체 생성
    cipher = AES.new(key, AES.MODE_CTR, counter=counter)

    # 복호화
    plaintext = cipher.decrypt(ciphertext)

    # 파일 확장자 추출
    ext_index = plaintext.rfind(b'.')
    file_extension = plaintext[ext_index:]
    plaintext = plaintext[:ext_index]

    # 파일 저장
    output_file = os.path.join(output_dir, os.path.basename(input_file).replace('.gomingo', file_extension.decode('utf-8')))
    with open(output_file, 'wb') as f_out:
        f_out.write(plaintext)

def add_extension(file_path, new_extension):
    file_name, _ = os.path.splitext(file_path)
    return file_name + new_extension

def encrypt_files_in_directory(directory, key):
    for root, _, files in os.walk(directory):
        for filename in files:
            input_file = os.path.join(root, filename)
            output_file = add_extension(input_file, '.gomingo')
            encrypt_file(input_file, output_file, key)
            os.remove(input_file)

def decrypt_files_in_directory(directory, key):
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.gomingo'):
                input_file = os.path.join(root, filename)
                decrypt_file(input_file, root, key)
                os.remove(input_file)  # 삭제

def display_key(key):
    print("Symmetric Key:", base64.b64encode(key).decode('utf-8'))

def main_menu():
    key = b'Sixteen byte key'
    while True:
        print("\nMenu:")
        print("1. Encrypt files in a directory")
        print("2. Decrypt all files in a directory and its subdirectories")
        print("3. Display Symmetric Key")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            directory = input("Enter the directory to encrypt: ")
            key = input("Enter the encryption key: ").encode('utf-8')
            encrypt_files_in_directory(directory, key)
            print(f'Encryption complete for files in {directory}')

        elif choice == '2':
            input_directory = input("Enter the directory to decrypt: ")
            key = input("Enter the decryption key: ").encode('utf-8')

            decrypt_files_in_directory(input_directory, key)
            print(f'Decryption complete for files in {input_directory} and its subdirectories')

        elif choice == '3':
            display_key(key)

        elif choice == '4':
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == '__main__':
    main_menu()