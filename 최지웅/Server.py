import telegram, asyncio                    #텔레그램 송수신용
from nacl.public import PrivateKey, Box     #공개키암호
from datetime import datetime               #시간정보
from time import sleep                      #딜레이
import os, sys                              #파일 내부 디렉토리
import nacl
import base64

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
    ClientAESKeyString=base64.b64encode(decryptedClientAESKey).decode('utf-8')
    print("[DEBUG] Finished Parsing key. decrypted Client AES key: ", ClientAESKeyString)
    with open(DECRYPTED_KEY_AES_FILENAME, 'wb') as File:
        File.write(decryptedClientAESKey)
    print("[DEBUG] Saved Parsed AES Key for Client")
    

if __name__=='__main__':
   # sleep(1000)
    print('hello')
    #sleep(100)
    parse_key_from_client(b'\xac\xc4\x9ajZ\x1e9Jw\xc5\xa4\xd3\x9b\xa0\xf2k\xffc\x80\x8db\xa6z\xfc\xbf!x"\x96}\xa2C',
                          b'\xa2Bq\xff\xac\xe4-\xefR\x84\xcdT\x96\x80\xd6\x08\xf1Z\x90C3+peB1Au|\xdc\xd00yj\xfe75\xe6\xcdI+\xfb\xd6\xf0\xe6R1\x81\xd5\x88\x9f\xc29(\x8aYW\xbdG\x06h5\xdf\xf7\x1ax\xaf\x19bw\xe4\xc5')
    print('h')
