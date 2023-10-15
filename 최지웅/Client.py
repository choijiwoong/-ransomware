import telegram, asyncio                    #텔레그램 송수신용
from nacl.public import PrivateKey, Box     #공개키암호
import nacl, nacl.secret
from datetime import datetime               #시간정보
from time import sleep                      #딜레이
import os, sys                              #파일 내부 디렉토리

#0. 기본 환경설정
PRIVATE_KEY_RSA_FILENAME=f"KEY_FILE"
PRIVATE_KEY_RSA=0
PUBLIC_KEY_RSA=0

PRIVATE_KEY_AES_FILENAME=f"KEY_FILE2"
PRIVATE_KEY_AES=0

PUBLIC_SERVER_RSA_KEY=PrivateKey(b'=\xe5!\xfb\xf0\x82\xa2\x1f\x070\x0c\xad\xdcR\x16=\x03\\\xa8\x11\xc6\xa4\xa3\xd7,Kn;\n\xb8\xcd.').public_key

AES_BOX=0

#1. RSA개인키 생성_스크립트 인자로 key path를 입력받으면 해당 내용을 읽어 로드(.py "privatePath")
if os.path.isfile(PRIVATE_KEY_RSA_FILENAME):
    print("[DEBUG] Loading ClientPrivateKey...")
    with open(PRIVATE_KEY_RSA_FILENAME, 'rb') as File:
        byteCode=File.read()
    PRIVATE_KEY_RSA=PrivateKey(byteCode)
    PUBLIC_KEY_RSA=PRIVATE_KEY_RSA.public_key
    print("[DEBUG] Loaded ClientPrivateKey")
    print(PRIVATE_KEY_RSA._private_key)
    print("[DEBUG] Derived ClientPublicKey")
    print(PUBLIC_KEY_RSA)
    print("[DEBUG] Key is completely Loaded!")
else:
    print("[DEBUG] WARINING_Previous ClientRSAKey will be removed and we will create new key after 30 seconds. After covering key, we cannot decrypt your file. RESTORE KEY FILE")
    sleep(30)
    print("[DEBUG] Making ClientPrivateKey by using script argument...")
    PRIVATE_KEY_RSA=PrivateKey.generate()
    PUBLIC_KEY_RSA=PRIVATE_KEY_RSA.public_key
    with open(PRIVATE_KEY_RSA_FILENAME, 'wb') as File:
        File.write(PRIVATE_KEY_RSA._private_key)
    print("[DEBUG] Created ServerPrivateKey")
    print(PRIVATE_KEY_RSA._private_key)
    print("[DEBUG] Derived ServerPublicKey")
    print(PUBLIC_KEY_RSA)
    print("[DEBUG] Key is completely Saved!")

#2. AES 대칭키 생성
print()
if os.path.isfile(PRIVATE_KEY_AES_FILENAME):
    print("[DEBUG] Loading AESKey...")
    with open(PRIVATE_KEY_AES_FILENAME, 'rb') as File:
        PRIVATE_KEY_AES=File.read()
    print("[DEBUG] Loaded AESKey")
    print(PRIVATE_KEY_AES)
else:
    print("[DEBUG] WARINING_Previous AESKey will be removed and we will create new key after 30 seconds. After covering key, we cannot decrypt your file. RESTORE KEY FILE")
    sleep(30)
    print("[DEBUG] Making AESKey by using script argument...")
    PRIVATE_KEY_AES=nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
    with open(PRIVATE_KEY_AES_FILENAME, 'wb') as File:
        File.write(PRIVATE_KEY_AES)
    print("[DEBUG] Created AESKey")
    print(PRIVATE_KEY_AES)

print()
#3. AES 대칭키 암호화
print("[DEBUG] Encrypting AESKey...")
AES_BOX=Box(PRIVATE_KEY_RSA, PUBLIC_SERVER_RSA_KEY)
encrypted_aes_key=AES_BOX.encrypt(PRIVATE_KEY_AES)
print("[DEBUG] Complete Encryption")
print(encrypted_aes_key)


    

if __name__=='__main__':
    print('hello')
