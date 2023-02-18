import pyrebase as pb
import string
import face_recognition
import time
import cv2
import random
import datetime
import serial as se

print(str(datetime.datetime.fromtimestamp(time.time()))[:10])

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
        print(lst)
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
        self.__dataBase.child("Attendance").child(hash).update({student:state})

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
    
    def SPush(self, file, name):
        self.__Storage.child("TestFolder").child(name).put(file)
    
    def GetImages(self, Class:tuple):
        for img in Class:
            self.__Storage.child("TestFolder").child(img).download("data\\"+img)

class Attendance:
    __FBobj:FireBase = None
    __Subject:str = None
    __Class:str = None
    __FacultyID:str = None
    __Hash:str = None
    def __init__(self, obj:FireBase, Subject:str, FacultyID:str, Class:str) -> None:
        self.__FBobj = obj
        self.__Class = Class
        self.__Subject = Subject
        self.__FacultyID = FacultyID
        date = str(datetime.datetime.fromtimestamp(time.time()))[:10]
        hc = Hash().GenerateCode(self.__FBobj)
        self.__Hash = hc
        self.__FBobj.AppendValue("meta", "Date", date, hc)
        self.__FBobj.AppendValue("meta", "FacultyID", self.__FacultyID, hc)
        self.__FBobj.AppendValue("meta", "Subject", self.__Subject, hc)
        self.__FBobj.AddHash(hc)
        self.__FBobj.CreateAttendance(hc, self.__FBobj.GetStudents(self.__Class))
    def MarkPresent(self, student:str):
        self.__FBobj.UpdateAttendance(self.__Hash, student, 'P')

class FaceRecog:
    
    __TrainedList:list = None
    __ID = ["Javidh", "Elon Musk"]

    def __init__(self) -> None:
        self.__TrainedList = self.Train(["data\RA148.jpeg", "data\RA002.jpg"])
    
    def PlotFace(self, img):
        try:
            loc = face_recognition.face_locations(img)[0]
            cv2.rectangle(img, (loc[0], loc[3]), (loc[2], loc[1]), (225,0,255), 2)
        except:
            pass

    def evaluate(self, results:list):
        for i in range(len(results)):
            if results[i]:
                at = Attendance()
                at.Record(self.__ID[i])
                return True

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
    
    def initialize(self):

        cam = cv2.VideoCapture(0)
        print("Camera On..")
        while True:
            check, frame = cam.read()
            self.PlotFace(frame)
            result = self.Test(frame, self.__TrainedList)
            if self.evaluate(result):
                time.sleep(3)

class Ardunio:
    __Port:str = None
    __Conn:se.Serial = None 

    def __init__(self, Port:str) -> None:
        self.__Port = Port
    
    def Connect(self) -> bool:
        try:
            com = se.Serial(self.__Port, baudrate=9600)
            return True
        except:
            return False
        
    def Disconnect(self):
        self.__Conn.close()
    
    def read(self) -> str:
        self.__Conn.write(b'r')
        for x in range(5):
            temp =  self.__Conn.readline().decode('utf-8')
            if(temp!=''):
                return temp
        return None