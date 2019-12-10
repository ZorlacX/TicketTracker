import tkinter as tk
import tkinter.font as font 
import re
import mysql.connector
import csv

class TicketTracker(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('800x480')
        self.title("Ticket Tracker")
        Label = []
        UserInput = []
        self.Font1 = font.Font(family = 'Helvetica', size = 11, weight = "bold")
        self.Font2 = font.Font(family = 'Helvetica', size = 12, weight = "bold")
        self.container = tk.Frame()
        self.container.grid(row = 1, columnspan = 5, pady = 5) 
        self.mydb= mysql.connector.connect()
      
        self.MODES = [
            ("Add entry to ticket", 0),
            ("Remove entry from Ticket", 1),         
            ("Add new ticket", 2),
            ("Ticket Report", 3),
            ("Date Report", 4)
        ]        
        self.log_in() 
        self.v = tk.IntVar()
        self.v.set(0) # initialize
        
             
    def create_interface(self):
        b=[]
        for text, mode in self.MODES:
            b.append(tk.Radiobutton(self, text=text,font = self.Font1, variable=self.v, 
                    value=mode, command = self.cb, indicatoron = 1).grid(row = 0, column = mode, padx = 2))
        self.mycursor = self.mydb.cursor(buffered=True)         
        self.add_entry()
        tables=[]
              
        self.mycursor.execute("SHOW TABLES")
        for x in self.mycursor:
            y =  ''.join(x) 
            tables.append(y) 
        if "tickets" in tables:
            None
            #self.create_table()
        else:self.create_table()
        print(tables)
            
        
    def create_table(self):
        #self.mycursor.execute("DROP TABLE tickets")
        self.mycursor.execute("CREATE TABLE tickets (id INT AUTO_INCREMENT PRIMARY KEY, date DATE, ticket_number CHAR(5), ticket_task VARCHAR(255), hrs DOUBLE(4, 2), description VARCHAR(255), INDEX (ticket_number))") 
    def cb(self):
        for child in self.container.winfo_children():
            child.destroy()
        func = self.v.get()
        if func == 0:
            self.add_entry()
        elif func == 1:
            self.remove_entry()
        elif func == 2:
            self.add_ticket()
        elif func == 3:
            self.ticket_report()
        else:
            self.date_report()
            
    def log_in(self):
        Page = LogIn(parent = self, controller = self)
 
    def choose_db(self):
        Page = ChooseDB(parent = self, controller = self)
            
    def add_entry(self):
        Page = AddEntry(parent = self.container, controller = self)

    def remove_entry(self):
        Page = RemoveEntry(parent = self.container, controller = self)
        
    def add_ticket(self):
        Page = AddTicket(parent = self.container, controller = self)

    def ticket_report(self):
        Page = TicketReport(parent = self.container, controller = self)
        
    def date_report(self):
        Page = DateReport(parent = self.container, controller = self)  
            
class LogIn(tk.Label):
    def __init__(self, parent, controller):
        tk.Label.__init__(self, parent)
        self.grid(row = 0, column = 0, sticky = "s")
        Label = []
        UserInput = []
        '''Label.append(Descriptor(parent = self, r=0, c=1))
        Label.append(Descriptor(parent = self, r=1, c=0))
        Label.append(Descriptor(parent = self, r=2, c=0))
        UserInput.append(Input(parent = self, r=0, c=1, w = 50))
        UserInput.append(Input(parent = self, r=1, c=1, w = 50))
        Label[0].config(text = "Login Details")        
        Label[1].config(text = "User: ")
        Label[2].config(text = "Password")'''
        
        Loginbtn = tk.Button(self, text = "Login", borderwidth=0, height = 1, width = 5, 
                        font = ('DejaVu Serif', 26, "bold"), command = lambda: SQLLogin())
        Loginbtn.grid(row = 1, column = 2, sticky = 'n', pady = 4, padx = 4, rowspan = 2)

        
        def SQLLogin():
            try:
                parent.mydb = mysql.connector.connect(
                host="localhost",
                user="Zorlac",#UserInput[0].get()
                passwd="#Zorlac69",#UserInput[1].get()
                auth_plugin="mysql_native_password"
                )
                self.destroy()
                controller.choose_db()  
                print(parent.mydb)
            except:
                Error = Descriptor(parent = self, r=3, c=1)
                Error.config(text = "Invalid Login Details.\nPlease try again.")
                
class ChooseDB(tk.Label):
    def __init__(self, parent, controller):
        tk.Label.__init__(self, parent)
        self.grid(row = 0, column = 0, sticky = "s")
        Label = []
        UserInput = []        
        choices = []
        Label.append(Descriptor(parent = self, r=0, c=0))
        Label[0].config(text = "Choose Database")        
        Contbtn = tk.Button(self, text = "Continue", borderwidth=0, height = 1, width = 8, 
                        font = ('DejaVu Serif', 26, "bold"), command = lambda: pick_db(tkvar.get()))
        Contbtn.grid(row = 2, column = 0, sticky = 'n', pady = 4, padx = 4)        
             
                
        mycursor = parent.mydb.cursor()                
        mycursor.execute("SHOW DATABASES")
        for x in mycursor:
            y =  ''.join(x) 
            print(y)
            choices.append(y)   
             
        tkvar = tk.StringVar()
        tkvar.set('Choose DB')
        popupMenu = tk.OptionMenu(self, tkvar, *choices)
        popupMenu.grid(row = 1, column =0)
                    
        def pick_db(x):
            if x != 'Choose DB':
                self.destroy()
                parent.mydb.database = x
                parent.create_interface()
               
class AddEntry(tk.Label):
    def __init__(self, parent, controller):
        tk.Label.__init__(self, parent)
        self.config(text = "0", anchor ="s")
        self.grid(row = 1, column = 0, sticky = "s")
        self.Label = []
        UserInput = []
        self.ticketnumber = 0
        self.tickettask = 'Ticket Task'
        self.controller = controller
        Ticket = TicketSelect(self, controller)
        self.Label.append(Descriptor(parent = self, r=0, c=1))
        self.Label.append(Descriptor(parent = self, r=0, c=2))
        self.Label.append(Descriptor(parent = self, r=0, c=3))        
        self.Label.append(Descriptor(parent = self, r=2, c=0))  
        self.Label.append(Descriptor(parent = self, r=1, c=1))
        UserInput.append(DateBox(parent = self, r=0, c=2, w = 10))
        UserInput.append(Input(parent = self, r=0, c=3, w = 5)) 
        UserInput.append(Input(parent = self, r=2, c=0, w = 90))  
        self.Label[0].config(text = "Ticket Task")
        self.Label[1].config(text = "Date(YYYY-MM-DD)")
        self.Label[2].config(text = "Hrs")  
        self.Label[3].config(text = "Description of work done")
        self.Label[4].config(text = self.tickettask)
        UserInput[2].grid(columnspan = 5)
        Contbtn = tk.Button(self, text = "Add Entry", borderwidth=0, height = 1, width = 8, 
                        font = ('DejaVu Serif', 26, "bold"), command = lambda: save())
        Contbtn.grid(row = 4, column = 0, sticky = 'n', pady = 4, padx = 4)        

        def save():
            sql = "INSERT INTO tickets (date, hrs, description, ticket_number, ticket_task) VALUES (%s, %s, %s, %s, %s)"
            val = (UserInput[0].get(), UserInput[1].get(), UserInput[2].get(), self.ticketnumber, self.tickettask)
            print(sql, val)
            print(controller.mycursor.lastrowid)
            controller.mycursor.execute(sql, val)
            controller.mydb.commit()
        
    def func(self,value):
        self.ticketnumber = ''.join(value)        
        self.controller.mycursor.execute("SELECT ticket_task FROM tickets WHERE ticket_number = '" + self.ticketnumber +"'")
        self.tickettask = ''.join(self.controller.mycursor.fetchone())
        self.Label[4].config(text = self.tickettask)
                
class RemoveEntry(tk.Label):
    def __init__(self, parent, controller):
        tk.Label.__init__(self, parent)
        self.config(text = "1", anchor ="s")
        self.grid(row = 1, column = 0, sticky = "s")
        
        Label = []
        UserInput = []

        Ticket = TicketSelect(self, controller)
        Label.append(Descriptor(parent = self, r=0, c=1))
        Label.append(Descriptor(parent = self, r=0, c=2))
        Label.append(Descriptor(parent = self, r=0, c=3))        
        Label.append(Descriptor(parent = self, r=2, c=0))
        UserInput.append(Input(parent = self, r=0, c=1, w = 50))
        UserInput.append(DateBox(parent = self, r=0, c=2, w = 10))
        UserInput.append(Input(parent = self, r=0, c=3, w = 5)) 
        UserInput.append(Input(parent = self, r=2, c=0, w = 90)) 
        Label[0].config(text = "Ticket Task")
        Label[1].config(text = "Date")
        Label[2].config(text = "Hrs")  
        Label[3].config(text = "Description of work done")
        UserInput[3].grid(columnspan = 5)

    def func(self,value):
        print (value)  
                
class AddTicket(tk.Label):
    def __init__(self, parent, controller):
        tk.Label.__init__(self, parent)
        self.config(text = "2", anchor ="s")
        self.grid(row = 1, column = 0, sticky = "s")
        Label = []
        UserInput = []
        
        Label.append(Descriptor(parent = self, r=0, c=0))
        Label.append(Descriptor(parent = self, r=0, c=1))
        Label.append(Descriptor(parent = self, r=2, c=0))  
              
        UserInput.append(DateBox(parent = self, r=0, c=0, w = 10))
        UserInput.append(Input(parent = self, r=0, c=1, w = 5))
        UserInput.append(Input(parent = self, r=2, c=0, w = 90))  
                   
        Label[0].config(text = "Date(YYYY-MM-DD)")
        Label[1].config(text = "Ticket Number")
        Label[2].config(text = "Ticket Task")
        
        UserInput[2].grid(columnspan = 5)
        Contbtn = tk.Button(self, text = "Add Ticket", borderwidth=0, height = 1, width = 8, 
                        font = ('DejaVu Serif', 26, "bold"), command = lambda: save())
        Contbtn.grid(row = 4, column = 0, sticky = 'n', pady = 4, padx = 4)        

        def save():
            sql = "INSERT INTO tickets (date, ticket_number, ticket_task, hrs, description) VALUES (%s, %s, %s, %s, %s)"
            val = (UserInput[0].get(), UserInput[1].get(), UserInput[2].get(), "0", "Add New Ticket")
            print(sql, val)
            print(controller.mycursor.lastrowid)
            controller.mycursor.execute(sql, val)
            controller.mydb.commit()


        
class TicketReport(tk.Label):
    def __init__(self, parent, controller):
        tk.Label.__init__(self, parent)
        self.controller = controller
        self.config(text = "3", anchor ="s")
        self.grid(row = 1, column = 0, sticky = "s")
        Ticket = TicketSelect(self, controller)
 
    def func(self,val):      
        self.controller.mycursor.execute("SELECT * FROM tickets WHERE ticket_number = '" + val +"'")
        myresult = self.controller.mycursor.fetchall()
        for x in myresult:
          print(x)
        
        column_names = [i[0] for i in self.controller.mycursor.description]
        fp = open('Report_Ticket_'+val+'.csv', 'w')
        myFile = csv.writer(fp, lineterminator='\n')
        myFile.writerow(column_names)
        myFile.writerows(myresult)
        fp.close()  
      
                 
class DateReport(tk.Label):
    def __init__(self, parent, controller):
        tk.Label.__init__(self, parent)
        self.config(text = "4", anchor ="s")
        self.grid(row = 1, column = 0, sticky = "s") 
        
        StartDate = DateBox(parent = self, r=0, c=1, w = 10)
        EndDate = DateBox(parent = self, r=0, c=2, w = 10)    
        
        controller.mycursor.execute("SELECT * FROM tickets")
        #sql = "SELECT * FROM customers WHERE address ='Park Lane 38'"
        myresult = controller.mycursor.fetchall()

        for x in myresult:
          print(x)       
        
class Descriptor(tk.Label):
    def __init__(self, parent, r, c):
        tk.Label.__init__(self, parent)
        self.config(text = "Hallo", anchor ="s")
        self.grid(row = r, column = c, sticky = "s")        
        
class Input(tk.Entry):
    def __init__(self, parent, r, c, w):
        tk.Entry.__init__(self, parent)
        self.grid(row = r+1, column = c)
        self.config(width = w)
        
class DateBox(tk.Entry):
    def __init__(self, parent, r, c, w):
        tk.Entry.__init__(self, parent)
        self.grid(row = r+1, column = c)
        self.config(width = w)
        
        def ValidateDate():
            inputString = self.get()
            print (inputString)
            if re.match(r"^[2][0][0-2][0-9][-][0-1][0-2][-][0-3][0-9]", inputString):
                print("Input accepted")
                self.config(fg= "black"  ) 
                return True
            else:
                print("Bad input, please try again") 
                self.config(fg= "red")    
                return False         
        
        self.config(validate ='focusout', vcmd = lambda:ValidateDate()) 

class TicketSelect(tk.Label):
    def __init__(self, parent, controller):
        tk.Label.__init__(self, parent)
        tkvar = tk.StringVar()
        choices = []    
        controller.mycursor.execute("SELECT ticket_number FROM tickets")
        myresult = controller.mycursor.fetchall()
        myresult = list(dict.fromkeys(myresult))
        for x in myresult:
            choices.append(''.join(x))
        tkvar.set('Ticket#')
        popupMenu = tk.OptionMenu(self, tkvar, *choices, command = parent.func)
        popupMenu.grid()
        self.grid(row = 0, column =0, rowspan = 2) 
    
if __name__ == "__main__":
    app = TicketTracker()      
    tk.mainloop()
    
