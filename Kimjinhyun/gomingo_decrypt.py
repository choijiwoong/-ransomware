from Crypto.Cipher import AES
from Crypto.Util import Counter
import os

def decrypt_file(input_file, output_file, key):
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

    # 평문 생성
    plaintext = cipher.decrypt(ciphertext)

    # 복호문을 출력 파일에 저장
    with open(output_file, 'wb') as f_out:
        f_out.write(plaintext)

def decrypt_files_in_directory(directory, key):
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.gomingo'):
                input_file = os.path.join(root, filename)
                output_file = os.path.splitext(input_file)[0]
                decrypt_file(input_file, output_file, key)
                os.remove(input_file)

if __name__ == '__main__':
    directory = input('복호화할 파일이 있는 최상위 디렉토리 경로 입력: ') 
    key = b'Sixteen byte key' 

    decrypt_files_in_directory(directory, key)
    print(f'{directory} 디렉토리와 하위 디렉토리 내의 파일을 성공적으로 복호화하고 파일 확장자명을 .gomingo에서 제거했습니다.')
