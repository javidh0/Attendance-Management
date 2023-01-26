import pyrebase as pb
import face_recognition
import time
import cv2

class FireBase:
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
    "databaseURL" : "https://attendance-management-8277c-default-rtdb.asia-southeast1.firebasedatabase.app/"
    }

    def initialize(self):
        fb = pb.initialize_app(self.__config)
        self.__dataBase = fb.database()

    def Push(self, path:str, data:dict):
        self.__dataBase.child(path).set(data)

    def Get(self, path:str) -> dict:
        return self.__dataBase.child(path).get().val()
    def GetStudents(self, Class:str) -> tuple:
        temp = self.__dataBase.child("Class").child(Class).child("Students").get().val()
        return tuple(temp)

class Attendance:
    def Record(self, id:str):
        print("Attendance Recorded in DataBase -> "+id)

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