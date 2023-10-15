import telegram, asyncio                    #텔레그램 송수신용
from nacl.public import PrivateKey, Box     #공개키암호
from datetime import datetime               #시간정보
from time import sleep                      #딜레이
import os, sys                              #파일 내부 디렉토리

#0. 기본 환경설정
PRIVATE_KEY_RSA_FILENAME=f"KEY_FILE"

#1. RSA개인키 생성_스크립트 인자로 key path를 입력받으면 해당 내용을 읽어 로드(.py "privatePath")
PRIVATE_KEY_RSA=0
PUBLIC_KEY_RSA=0
if os.path.isfile(PRIVATE_KEY_RSA_FILENAME):
    print("[DEBUG] Loading ClientPrivateKey by using script argument...")
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
    PRIVATE_KEY_RSA=PrivateKey.generate()
    PUBLIC_KEY_RSA=PRIVATE_KEY_RSA.public_key
    with open(PRIVATE_KEY_RSA_FILENAME, 'wb') as File:
        File.write(PRIVATE_KEY_RSA._private_key)
    print("[DEBUG] Created ServerPrivateKey")
    print(PRIVATE_KEY_RSA._private_key)
    print("[DEBUG] Derived ServerPublicKey")
    print(PUBLIC_KEY_RSA)
    print("[DEBUG] Key is completely Saved!")

if __name__=='__main__':
    print('hello')
