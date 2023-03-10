import pyrebase as pb
import string
import face_recognition
import time
import cv2
import random
import datetime
import os
import pandas as pd
import serial as se
from tkinter import *
import pyautogui as pyg
from tkinter import ttk
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from PIL import Image, ImageTk
import json
import urllib

print(str(datetime.datetime.fromtimestamp(time.time()))[:10])

def InternetCheck(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

class State:
    Ardunio:bool = False
    Internet:bool = False
    Cam:bool = False
    def __init__(self) -> None:
        self.Ardunio = False
        self.Internet = False
    def ArduinoSet(self, state:bool):
        self.Ardunio = state
    def InternetSet(self, state:bool):
        self.Internet = state
    def CamSet(self, state:bool):
        self.Cam = state
    def GetArduino(self):
        return self.Ardunio
    def GetInternet(self):
        return self.Internet
    def GetCam(self):
        return self.Cam

UniversalObj = State()

class Ardunio:
    pass

class Mail:
    __send_from = None
    __username = None
    __password = None

    def __init__(self) -> None:
        f = open('data\mail.json')
        a = json.load(f)
        self.__send_from = a['Cred']['MailID']
        self.__username = a['Cred']['MailID']
        self.__password = a['Cred']['pass']

    def send_mail_message(self, toMail:list, message) -> None:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(self.__send_from, self.__password)
        s.sendmail(self.__username, toMail, message)
        s.quit()

    def send_mail_file(self, send_to,subject,text, files, file_name):
        msg = MIMEMultipart()
        msg['From'] = self.__send_from
        msg['To'] = send_to
        msg['Date'] = formatdate(localtime = True)
        msg['Subject'] = subject
        msg.attach(MIMEText(text))

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(files, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename='+file_name)
        msg.attach(part)

        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login(self.__username,self.__password)
        smtp.sendmail(self.__send_from, send_to, msg.as_string())
        smtp.quit()
    
    def send_df(self, send_to, subject, text, df:pd.DataFrame, file_name):
        df.to_csv("buffer.csv", index=None)
        self.send_mail_file(send_to, subject, text, 'buffer.csv', file_name)

class Hash:
    __aph = string.ascii_lowercase
    __num = list(map(str, range(0,10)))
    __sym = "!@#$%^&*()"
    __code = ''
    
    def GenerateCode(self, FBobj):
        dta = FBobj.GetHash()
        self.__code = ''
        self.__code += ( random.choice(self.__aph) + random.choice(self.__aph) + random.choice(self.__aph) )
        self.__code += ( random.choice(self.__num) + random.choice(self.__num) )
        self.__code += random.choice(self.__sym)
        if self.__code in dta:
            self.GenerateCode()
        return self.__code 

class FireBase:
    __Storage = None
    __dataBase = None
    __config = {
    "apiKey": "AIzaSyBk-trGoXiH-alr7TXC9p8v6OXGBgWHrfE",
    "authDomain": "attendance-management-8277c.firebaseapp.com",
    "databaseURL": "https://attendance-management-8277c-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "attendance-management-8277c",
    "storageBucket": "attendance-management-8277c.appspot.com",
    "messagingSenderId": "393696014722",
    "appId": "1:393696014722:web:ac2d77466297c64c671f9b",
    "measurementId": "G-Y019WT9CFF",
    "databaseURL" : "https://attendance-management-8277c-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "serviceAccount": "serviceAccountKey.json"
    }

    def initialize(self):
        fb = pb.initialize_app(self.__config)
        self.__dataBase = fb.database()
        self.__Storage = fb.storage()
    
    def AppendValue(self, path1:str, path2:str, path3:str, value:str):
        lst = []
        try:
            lst = list(self.__dataBase.child(path1).child(path2).child(path3).get().val())
        except:
            pass
        lst.append(value)
        self.__dataBase.child(path1).child(path2).child(path3).set(lst)

    def CreateAttendance(self, hash:str, students:tuple):    
        dct = {
        }
        for stu in students:
            dct[stu] = 'A'
        self.__dataBase.child("Attendance").child(hash).set(dct)
    
    def UpdateAttendance(self, hash:str, student:str, state:str):
        if not (state == 'A' or state == 'P'):
            print("Error : Invalid Key :"+state)
            return
        temp = self.__dataBase.child("Attendance").child(hash).child(student).get().val()
        self.__dataBase.child("Attendance").child(hash).update({student:state})
        return temp

    def Push(self, path1:str,path2:str, data:dict):
        self.__dataBase.child(path1).child(path2).set(data)

    def Get(self, path:str) -> dict:
        return self.__dataBase.child(path).get().val()

    def GetStudents(self, Class:str) -> tuple:
        temp = self.__dataBase.child("Class").child(Class).child("Students").get().val()
        return tuple(temp)
    
    def GetHash(self) -> tuple:
        temp = self.__dataBase.child("Hash").get().val()
        return tuple(temp)
    
    def AddHash(self, hash:str):
        lst = list(self.__dataBase.child("Hash").get().val())
        lst.append(hash)
        self.__dataBase.child("Hash").set(lst)
        
    def GetImages(self, imgList):
        for x in os.listdir('Images'):
            os.remove("Images\\"+x)
        for x in self.__Storage.list_files():
            if str(x.name) in imgList:
                x.download_to_filename("Images\\"+str(x.name))
    
    def GetClass(self):
        temp:dict = self.__dataBase.child("Class").get().val()
        return tuple(temp.keys())
    
    def GetRecords(self, hash:str):
        temp = self.__dataBase.child("Attendance").child(hash).get().val()
        lst = []
        for i in temp.items():
            lst.append(i)
        return pd.DataFrame(lst, columns=['ID', 'A/P'])
    
    def GetMailID(self, students:list[str]):
        tr = [[], []]
        for ids in students:
            temp = self.__dataBase.child('Students').child(ids).get().val()
            tr[0].append(temp['MailID'])
            tr[1].append(temp['Name'])
        return tr
    
    def Rfid_to_RA(self, rfid:str):
        return self.__dataBase.child("Rfid").child(rfid).get().val()
    
    def GetDatesData(self):
        temp = self.__dataBase.child("meta").child("Date").get().val()
        return temp
    def GetFacultyData(self):
        temp = self.__dataBase.child("meta").child("FacultyID").get().val()
        return temp
    def GetSubjectData(self):
        temp = self.__dataBase.child("meta").child("Subject").get().val()
        return temp
    def Mark(self, Class:str, hash:str):
        self.__dataBase.child("Class").child(Class).child("ActiveAttendance").set({"ActiveAttendance":hash})
    def GetActiveAttendances(self, Class:str):
        return self.__dataBase.child("Class").child(Class).child("ActiveAttendance").get().val()["ActiveAttendance"]

class Attendance:
    __FBobj:FireBase = None
    __Subject:str = None
    __Class:str = None
    __FacultyID:str = None
    __Hash:str = None
    __date:str = None
    def __init__(self, obj:FireBase, Subject:str, FacultyID:str, Class:str) -> None:
        self.__FBobj = obj
        self.__Class = Class
        self.__Subject = Subject
        self.__FacultyID = FacultyID
        date = str(datetime.datetime.fromtimestamp(time.time()))[:10]
        self.__date = date
        hc = Hash().GenerateCode(self.__FBobj)
        self.__Hash = hc
        self.__FBobj.AppendValue("meta", "Date", date, hc)
        self.__FBobj.AppendValue("meta", "FacultyID", self.__FacultyID, hc)
        self.__FBobj.AppendValue("meta", "Subject", self.__Subject, hc)
        self.__FBobj.AddHash(hc)
        stuList = self.__FBobj.GetStudents(self.__Class)
        self.__FBobj.CreateAttendance(hc, stuList)
        self.__FBobj.GetImages(stuList)
    def MarkPresent(self, student:str):
        temp = self.__FBobj.UpdateAttendance(self.__Hash, student, 'P')
        return temp == 'A'
    def Record(self, x):
        print(x)
    def GetTitle(self):
        return str(self.__Class) +" "+ str(self.__Subject) +" "+ str(self.__date)
    def GetRecords(self):
        return self.__FBobj.GetRecords(self.__Hash)
    def SetActive(self):
        self.__FBobj.Mark(self.__Class, self.__Hash)
    def Deactive(self):
        self.__FBobj.Mark(self.__Class, "None")

class FaceRecog:
    __TrainedList:list = None
    __Rfid:Ardunio = None
    __ID = os.listdir("Images")

    FunAdd = lambda self, a : "Images\\"+a

    def __init__(self) -> None:
        pass

    def start(self):
        self.__TrainedList = self.Train(tuple(map(self.FunAdd, self.__ID)))
    
    def PlotFace(self, img):
        try:
            loc = face_recognition.face_locations(img)[0]
            cv2.rectangle(img, (loc[0], loc[3]), (loc[2], loc[1]), (225,0,255), 2)
        except:
            pass

    def evaluate(self, results:list):
        for i in range(len(results)):
            if results[i]:
                return [True, self.__ID[i]]
        return [False, None]

    def Train(self, images:list[str]) -> list:                  
        encodedList = []  
        for x in images:
            img = face_recognition.load_image_file(x)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encd = face_recognition.face_encodings(img)[0]
            encodedList.append(encd)
        return encodedList    
    
    def Test(self, img, trainedList):                      
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            encoed = face_recognition.face_encodings(img)[0]
            results = face_recognition.compare_faces(trainedList, encoed)
            return results
        except:
            return []

    def initialize(self, cam):
        check, frame = cam.read()
        self.PlotFace(frame)
        result = self.Test(frame, self.__TrainedList)
        got = self.evaluate(result)
        if got[0]:
            time.sleep(1)
            return got[1]
        return None

class FaceRecog1:
    __TrainedList:list = None
    __Rfid:Ardunio = None
    __ID = os.listdir("Images")

    FunAdd = lambda self, a : "Images\\"+a

    def start(self):
        self.__TrainedList = self.Train(tuple(map(self.FunAdd, self.__ID)))

    def Train(self, images:list[str]):
        tr = []
        for loc in images:
            img = face_recognition.load_image_file(loc)
            enc = face_recognition.face_encodings(img)[0]
            tr.append(enc)
        return tr
    
    def Test(self, frame):
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(self.__TrainedList, face_encoding)
    
            name = "UN"
            if True in matches:
                match_index = matches.index(True)
                name = self.__ID[match_index]
            if name == 'UN':
                return None
            return name

class Ardunio:
    __Port:str = None
    __Conn:se.Serial = None 

    def __init__(self, Port:str) -> None:
        self.__Port = Port
    
    def Connect(self) -> bool:
        try:
            self.__Conn = se.Serial(self.__Port, baudrate=9600, timeout=0)
            return True
        except:
            return False
        
    def Disconnect(self):
        self.__Conn.close()
    def Refresh(self):
        self.__Conn.read_all()
    def read(self) -> str:
        time.sleep(0.5)
        temp = self.__Conn.readline()
        if temp != b'':
            return temp.decode('utf-8')
    def isOpen(self):
        if self.__Conn == None:
            return False
        return self.__Conn.isOpen()

class Window:
    __root:Tk  = None
    __mainFrm:LabelFrame = None
    __font = ("Consolas", 17)
    __title = ("Consolas", 20)
    __FbObj:FireBase = None
    __Attendance:Attendance = None
    __FbObj:FireBase = None
    __cam:cv2 = None
    __FaceObj:FaceRecog = None
    videoLabel:Label = None
    __Arduino:Ardunio = None
    lbl:Label = None
    def __init__(self, FaceRecog_:FaceRecog ) -> None:
        pyg
        self.__root = Tk()
        self.__root.title("SRM Attendance")
        width = self.__root.winfo_screenwidth() - 500   
        height = self.__root.winfo_screenheight() - 50
        self.__root.geometry('%dx%d'%(width, height))
        self.__mainFrm = LabelFrame(self.__root)
        self.__mainFrm.place(relx=0.5, rely=0.5, anchor=CENTER, relwidth=0.99, relheight=0.99)
        try:
            self.__FbObj = FireBase()
            self.__FbObj.initialize()
            UniversalObj.InternetSet(True)
        except:
            UniversalObj.InternetSet(False)
        self.__FaceObj = FaceRecog_
        self.__Arduino = Ardunio("COM5")
        self.ConnectArduino()

    def ConnectArduino(self):
        temp = self.__Arduino.Connect()
        UniversalObj.ArduinoSet(temp)
        return temp
    
    def CheckConnect(self):
        temp = self.__Arduino.isOpen()
        UniversalObj.ArduinoSet(temp)
        return temp

    def __CloseAttendance(self):
        self.__Attendance.Deactive()
        self.at_root.destroy()
        df = self.__Attendance.GetRecords()
        lst = list(df[df['A/P'] == 'A']['ID'])
        ml = Mail()
        print("Mail sending to faculty")
        ml.send_df(self.__MailId, "Attendance", "PFA", df, "Attendance.csv")
        print("Mail sent")
        mailIDS = self.__FbObj.GetMailID(lst)
        print("Mail sending to students")
        ml.send_mail_message(mailIDS[0], "You were marked Absent in "+self.__Attendance.GetTitle())
        print("Mail sent")
        self.__cam.release()
    def __CloseAttendance1(self):
        self.__Attendance.Deactive()
        self.rfid_root.destroy()
        df = self.__Attendance.GetRecords()
        lst = list(df[df['A/P'] == 'A']['ID'])
        ml = Mail()
        print("Mail sending to faculty")
        ml.send_df(self.__MailId, "Attendance", "PFA", df, "Attendance.csv")
        print("Mail sent")
        mailIDS = self.__FbObj.GetMailID(lst)
        print("Mail sending to students")
        ml.send_mail_message(mailIDS[0], "You were marked Absent in "+self.__Attendance.GetTitle())
        print("Mail sent")
        self.__cam.release()
        
    def __AttenadanceWindowRFID(self):
        self.__Attendance.SetActive()
        rfid_root = Tk()
        self.rfid_root = rfid_root
        rfid_root.title(self.__Attendance.GetTitle())
        width = self.__root.winfo_screenwidth() - 500
        height = self.__root.winfo_screenheight() - 50
        rfid_root.geometry('%dx%d'%(width, height))
        Button(rfid_root, text="Close Attendance", font=self.__font, command=self.__CloseAttendance1).pack(pady=10)

        disFrame = Frame(rfid_root)
        disFrame.pack(padx=10, pady=10)

        while True:
            rfid_root.update()
            id = self.__Arduino.read()
            if id != None:
                print(id[:-2])
                ra = self.__FbObj.Rfid_to_RA(id[:-2])
                print(ra)
                self.__Attendance.MarkPresent(ra)

    def __AttenadanceWindow(self):
        self.__Attendance.SetActive()
        try:
            self.__cam = cv2.VideoCapture(0)
            UniversalObj.CamSet(True)
        except:
            UniversalObj.CamSet(False)
        def Update(rt):
            try:
                rt.update()
            except:
                pass
        def Clr(frame):
            for i in frame.winfo_children():
                i.destroy()
        at_root = Tk()
        at_root.title()
        self.at_root = at_root
        tit = self.__Attendance.GetTitle()
        at_root.title(tit)
        width = self.__root.winfo_screenwidth() - 500
        height = self.__root.winfo_screenheight() - 50
        at_root.geometry('%dx%d'%(width, height))
        Button(at_root, text="Close Attendance", font=self.__font, command=self.__CloseAttendance).pack(pady=10)
        Dis = Frame(at_root)
        Dis.pack()
        while True:
            at_root.update()
            id = self.__FaceObj.Test(self.__cam.read()[1])
            if False:
                check, frame = self.__cam.read()
                b,g,r = cv2.split(frame)
                img = cv2.merge((r,g,b))
                im = Image.fromarray(img)
                imgtk = ImageTk.PhotoImage(image=im)
                Clr()
                Label(at_root, image=imgtk).pack()
                at_root.update()
                self.__cam.release()
            if id != None:
                Clr(Dis)
                print(id)

                if Update(at_root):
                    break
                if self.__Attendance.MarkPresent(id):
                    if Update(at_root):
                        break
                    Label(Dis, text="Marked Present", font=self.__font).pack(padx=10, pady=10)
                    if Update(at_root):
                        break
                else:
                    if Update(at_root):
                        break
                    Label(Dis, text="Already Marked Present", font=self.__font).pack(padx=10, pady=10)
                    if Update(at_root):
                        break

        at_root.mainloop()
    def Create(self, Subject, FacultyID, Class, MailID):
        try:
            a = cv2.VideoCapture(0)
            UniversalObj.CamSet(True)
        except:
            UniversalObj.CamSet(False)
        self.__MailId = MailID
        print(Subject, FacultyID, Class)
        self.__Attendance = Attendance(obj= self.__FbObj, Subject=Subject, FacultyID=FacultyID, Class=Class)
        self.__FaceObj.start()
        
        self.FcBtn = Button(self.__mainFrm, text="Take FaceRecognition Attendance", font=self.__font, command=self.__AttenadanceWindow)
        self.FcBtn.pack(pady=10)
        self.FcBtn['state'] = DISABLED
        self.RfBtn = Button(self.__mainFrm, text="Take Rfid Attendance", font=self.__font, command=self.__AttenadanceWindowRFID)
        self.RfBtn.pack(pady=10)
        self.RfBtn['state'] = DISABLED
        if UniversalObj.GetInternet():
            if UniversalObj.GetArduino():
                self.RfBtn['state'] = NORMAL
            if UniversalObj.GetCam():
                self.FcBtn['state'] = NORMAL
        
    def __CreateAttendanceWindow(self):
        for i in self.__mainFrm.winfo_children():
            i.destroy()
        ClassId = self.__FbObj.GetClass()
        n = StringVar()
        ttk.Combobox(self.__mainFrm, values=ClassId, textvariable=n, width=20, font=self.__font).pack(pady=10)
        Subject_Code = ttk.Entry(self.__mainFrm, width=20, font=self.__font)
        Subject_Code.pack(pady=10)
        Subject_Code.insert(0, 'Subject Code')
        FacultyId = ttk.Entry(self.__mainFrm, width=20, font=self.__font)
        FacultyId.pack(pady=10)
        FacultyId.insert(0, 'Faculty Id')
        MailId = ttk.Entry(self.__mainFrm, width=20, font=self.__font)
        MailId.insert(0, 'mm1632@srmist.edu.in')
        MailId.pack(pady=10)
        Button(self.__mainFrm, text="--OK--", font=self.__font, command=lambda: self.Create(Subject_Code.get(), FacultyId.get(), n.get(), MailId.get())).pack(pady=10)
    
    def MainWindow(self):
        Button(self.__mainFrm, text="Create Attendance", font=self.__font, command=self.__CreateAttendanceWindow).pack(pady=10)

    def __RefreshMain(self):
        for i in self.__mainFrm.winfo_children():
            i.destroy()
        self.MainWindow1()

    def MainWindow1(self):
        UniversalObj.InternetSet(InternetCheck())
        Label(self.__mainFrm, text="SRM-Automated Attendance", font=self.__title).place(relx=0.5, rely=0.05, anchor=CENTER)
        self.btn = Button(self.__mainFrm, text="Arduino Reconnect", command=self.ConnectArduino, font=self.__font)
        self.btn.place(relx=0.98, rely=0.14, anchor=E)
        self.btn['state'] = DISABLED
        Button(self.__mainFrm, text="Refresh", font=self.__font, command=self.__RefreshMain).place(relx=0.98, rely=0.21, anchor=E)
        tm = str(datetime.datetime.fromtimestamp(time.time()))[:10]
        Label(self.__mainFrm, text='Date:'+tm, font=self.__font).place(relx=0.02, rely=0.1, anchor=W)
        Label(self.__mainFrm, text='Arduino Connection Status', font=self.__font)
        self.btn2 = Button(self.__mainFrm, text="Create Attendance", font=self.__font, command=self.__CreateAttendanceWindow)
        self.btn2.place(relx=0.5, rely=0.25, anchor=CENTER)
        self.btn2['state'] = DISABLED

        stat = UniversalObj.GetArduino()
        if stat:
            self.btn['state'] = DISABLED
            self.btn2['state'] = NORMAL
            Label(self.__mainFrm, text="RFID Connected", font=self.__font, fg='green').place(relx=0.02, rely=0.175, anchor=W)
        else:
            self.btn['state'] = NORMAL
            self.btn2['state'] = DISABLED
            Label(self.__mainFrm, text="RFID Not Connected", font=self.__font, fg='red').place(relx=0.02, rely=0.175, anchor=W)

        stat = UniversalObj.GetInternet()
        if stat:
            self.btn['state'] = DISABLED
            self.btn2['state'] = NORMAL
            Label(self.__mainFrm, text="DataBase Connected", font=self.__font, fg='green').place(relx=0.02, rely=0.215, anchor=W)
        else:
            self.btn['state'] = NORMAL
            self.btn2['state'] = DISABLED
            Label(self.__mainFrm, text="DataBase Not Connected", font=self.__font, fg='red').place(relx=0.02, rely=0.215, anchor=W)

        
    def enable(self):
        self.__root.mainloop()
