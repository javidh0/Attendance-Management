from modules import *

class Console:
    __FbObj:FireBase = None
    __root:Tk = None
    __MainFrm:LabelFrame = None
    __font = ("Consolas", 17)
    __title = ("Consolas", 20)
    __Date:dict = None
    __Sub:dict = None
    __Fac:dict = None

    def __init__(self) -> None:
        pyg
        self.__FbObj = FireBase()
        self.__FbObj.initialize()
        self.__root.title("Console")
        
        width = self.__root.winfo_screenwidth() - 500   
        height = self.__root.winfo_screenheight() - 50

        self.__root.geometry('%dx%d'%(width, height))
        self.__mainFrm = LabelFrame(self.__root)
        self.__mainFrm.place(relx=0.5, rely=0.5, anchor=CENTER, relwidth=0.99, relheight=0.99)
    
    def GetData(self):
        self.__Date = self.__FbObj.GetDatesData()
        self.__Fac = self.__FbObj.GetFacultyData()
        self.__Sub = self.__FbObj.GetSubjectData()

    def MainWindow(self):
        Label(self.__MainFrm, text="SRM-Attendance Console", font=self.__title).place(relx=0.5, rely=0.05)
        self.GetData()
        
