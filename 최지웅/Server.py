import telegram, asyncio                    #텔레그램 송수신용
from nacl.public import PrivateKey, Box     #공개키암호
from datetime import datetime               #시간정보
from time import sleep                      #딜레이
import os, sys                              #파일 내부 디렉토리
import nacl

#0. 기본 환경설정
PRIVATE_KEY_RSA_FILENAME=f"PRIVATE_KEY_RSA_SERVER_{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}"
DECRYPTED_KEY_AES_FILENAME=f"DECRYPTED_KEY_AES_FOR_CLIENT_{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}"
DECRYPTED_KEY_AES=0
BOX=0

#1. RSA개인키 생성_스크립트 인자로 key path를 입력받으면 해당 내용을 읽어 로드(.py "privatePath")
PRIVATE_KEY_RSA=0
PUBLIC_KEY_RSA=0
if len(sys.argv)==2:
    print("[DEBUG] Loading ServerPrivateKey by using script argument...")
    with open(sys.argv[1], 'rb') as File:
        byteCode=File.read()
    PRIVATE_KEY_RSA=PrivateKey(byteCode)
    PUBLIC_KEY_RSA=PRIVATE_KEY_RSA.public_key
    print("[DEBUG] Loaded ServerPrivateKey")
    print(PRIVATE_KEY_RSA._private_key)
    print("[DEBUG] Derived ServerPublicKey")
    print(PUBLIC_KEY_RSA)
    print("[DEBUG] Key is completely Loaded!")
else:
    print("[DEBUG] WARINING_Previous ServerRSAKey will be removed and we will create new key after 30 seconds. After covering key, we cannot decrypt client key before we linked.")
    sleep(30)
    print("[DEBUG] Making ServerPrivateKey by using script argument...")
    PRIVATE_KEY_RSA=PrivateKey.generate()
    PUBLIC_KEY_RSA=PRIVATE_KEY_RSA.public_key
    with open(PRIVATE_KEY_RSA_FILENAME, 'wb') as File:
        File.write(PRIVATE_KEY_RSA._private_key)
    print("[DEBUG] Created ServerPrivateKey")
    print(PRIVATE_KEY_RSA._private_key)
    print("[DEBUG] Derived ServerPublicKey")
    print(PUBLIC_KEY_RSA)
    print("[DEBUG] Key is completely Saved!")

#2. 텔레그램으로 전달받은 키값으로 복호화하여 저장.
def parse_key_from_client(clientRSAPublicKey, encryptedClientAESKey):
    print("[DEBUG] Stsrt Parsing keys from client...")
    clientRSAPublicKey=nacl.public.PublicKey(clientRSAPublicKey)
    encryptedClientAESKey=nacl.utils.EncryptedMessage(encryptedClientAESKey)
    print(type(encryptedClientAESKey))
    BOX=Box(PRIVATE_KEY_RSA, clientRSAPublicKey)
    decryptedClientAESKey=BOX.decrypt(encryptedClientAESKey)
    print("[DEBUG] Finished Parsing key. decrypted Client AES key: ", decryptedClientAESKey)
    with open(DECRYPTED_KEY_AES_FILENAME, 'wb') as File:
        File.write(decryptedClientAESKey)
    print("[DEBUG] Saved Parsed AES Key for Client")
    

if __name__=='__main__':
    print('hello')
    parse_key_from_client(b'\xe1\x1d\xb6\xee\x1e\xd7\xd95\x02\x96\x19\xde\x9b\x80\xc5\\9PF>\xda\xef\xf1t\xb6\xb9/$o\x15\xf4;'
                          , b"Ni\xa9\xfcnPCf.q{{\xc8\x01\xeb\xbd\xaef\xa9G\x1eQ\xf0\x90\xa9(\xd7R\xb4\x98\xaf\x96\x9f%.V\xc0\x1a\xe2\x19K=\x9a\xce\x15\x82O\x047\x8a\x9d\x19\xcb\x9d'\x1a\x89\xfa\x16\xc8\x8aB\xa7vT\xbd\x11K`\xeb\xf2\x94")
    print('h')
