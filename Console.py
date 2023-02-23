from modules import *

class Table:

    def TableDis(self, dt:pd.DataFrame, column_name, max_ht, rt, app:bool, wid):
        w = ttk.Scrollbar(rt)
        w.pack(side=RIGHT, fill = 'y')
        tr = ttk.Treeview(rt, yscrollcommand=w.set)
        tr['columns'] = column_name
        tr.column('#0', minwidth=0, width=0)
        for x in range(len(column_name)):
            id = '#'+str(x+1)
            tr.column(id, anchor=W, width=wid)
        for x in column_name:
            tr.heading(x, text = x, anchor=W)
        tr['height'] = max_ht
        if app:
            for x in range(dt.shape[0]):
                while(True):
                    try:
                        res = ''.join(random.choices(string.ascii_uppercase +string.digits, k = 10))
                        tr.insert(parent='',index='end', iid=str(res), values=tuple(dt.iloc[x]), text='')
                        break
                    except:
                        pass
        tr.pack()
        w.config(command=tr.yview)
        return tr
    
    def TableAppend(self, dt, tr, uniq):   #data, tree, unique append (True/ False)
        lst = []
        lst1 = []
        dtc = dt
        if uniq:
            for x in tr.get_children():
                lst.append(list(tr.item(x)['values']))

            for x in range(dt.shape[0]):
                if list(dt.iloc[x]) not in lst:
                    lst1.append(list(dt.iloc[x]))
            dtc = pd.DataFrame(lst1)
            

        for x in range(dtc.shape[0]):
            print("hell")
            res = ''.join(random.choices(string.ascii_uppercase +string.digits, k = 10))
            tr.insert(parent='',index='end', iid=str(res), values=tuple(dtc.iloc[x]), text='')
            break
    def TableDel(self, tr):
        for x in tr.get_children():
            tr.delete(x)

    def TableFetch(self, tr, clm):
        lst = []
        for x in tr.get_children():
            lst.append(tr.item(x)['values'])
        return pd.DataFrame(lst, columns=clm)

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

        self.TreeFrame = LabelFrame(self.__MainFrm)
        self.TreeFrame.place(relx=0.5, rely=0.35, relheight=0.6, relwidth=0.98, anchor=N)

        self.TrObj = Table()
    
    def GetData(self):
        self.__Date = self.__FbObj.GetDatesData()
        self.__Fac = self.__FbObj.GetFacultyData()
        self.__Sub = self.__FbObj.GetSubjectData()
        self.__Class = self.__FbObj.GetClass()

    def SearchAtttendance(self):
        pass

    def MainWindowRecords(self):
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

        self.Tr = self.TrObj.TableDis(pd.DataFrame(), ['ID', "P/A"], 40, self.TreeFrame, False, 300)

    def GetAttendRec(self, hash):
        return self.__FbObj.GetRecords(hash)

    def SearchAttend1(self, hash:str):
        self.TrObj.TableDel(self.Tr)
        self.TrObj.TableAppend(self.GetAttendRec(hash), self.Tr, False)
        Button(self, text="Refresh", command=lambda : self.SearchAttend1(hash))

    def SearchAttend0(self):
        Class = str(self.cbclass.get())
        active = [self.__FbObj.GetActiveAttendances(Class)]
        activecb = ttk.Combobox(self.__MainFrm, values=active, font=self.__font)
        activecb.place(relx=0.5, rely=0.2, anchor=CENTER)
        Button(self.__MainFrm, text="Search" ,font=self.__font, command=lambda : self.init_Fetch(str(activecb.get()))).place(relx=0.75,rely=0.22, anchor=E)
    
    def MainWindowStudent(self):
        self.Tr = self.TrObj.TableDis(pd.DataFrame(), ['ID', "P/A"], 40, self.TreeFrame, False, 300)
        Label(self.__MainFrm, text="SRM-Attendance Student's Console", font=self.__title).place(relx=0.5, rely=0.05, anchor=CENTER)
        self.GetData()
        fv1 = self.__Class
        Label(self.__MainFrm, text="Active Attendances", font=self.__font).place(relx=0.5, rely=0.1, anchor=CENTER)
        self.cbclass = ttk.Combobox(self.__MainFrm, values=fv1, font=self.__font)
        self.cbclass.place(relx=0.5, rely=0.15, anchor=CENTER)
        Button(self.__MainFrm, text="Search" ,font=self.__font, command=self.SearchAttend0).place(relx=0.75,rely=0.15, anchor=E)
        
    def init_Fetch(self, hash):
        while True:
            time.sleep(0.5)
            print(self.GetAttendRec(hash))

    def enable(self):
        self.__root.mainloop()