import pyrebase as pb

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
    pass