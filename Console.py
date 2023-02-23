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

        self.__root = Tk()
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
        Label(self.__MainFrm, text="SRM-Attendance Console", font=self.__title).place(relx=0.5, rely=0.05, anchor=CENTER)
        self.GetData()
        fv1 = ['None']
        fv2 = ['None']
        fv3 = ['None']
        for i in self.__Date.items():
            fv1.append(i[0])
        for i in self.__Fac.items():
            fv2.append(i[0])
        for i in self.__Sub.items():
            fv3.append(i[0])
        
        Label(self.__MainFrm, text="Search Attendance Record", font=self.__font).place(relx=0.02, rely=0.1)
        self.cbdate = ttk.Combobox(self.__MainFrm, values=fv1, font=self.__font)
        self.cbdate.place(relx=0.02, rely=0.15)
        self.cbfac = ttk.Combobox(self.__MainFrm, values=fv2, font=self.__font)
        self.cbfac.place(relx=0.02, rely=0.2)
        self.cbsub = ttk.Combobox(self.__MainFrm, values=fv3, font=self.__font)
        self.cbsub.place(relx=0.02, rely=0.25)

    def enable(self):
        self.__root.mainloop()