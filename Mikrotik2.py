import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import ros_api

class Loginpage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller = controller
        
        #background
        load = Image.open("image/hqzen.png")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image=photo
        label.place(x=0, y=0)
        
        load = Image.open("image/logo.png")
        logo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=logo, bg='white')
        label.image=logo
        label.place(x=315, y=50)
        
        self.border = tk.LabelFrame(self, background="white", highlightbackground="#f2f2f2")
        self.border.pack(fill="both", expand="no", padx=250, pady=150)
        
        self.login_label = tk.Label(self.border, text="Login to ISP Switch", background="white", font=("Arial", 13))
        self.login_label.pack()

        # BUTTON HOVER STYLING
        
        def on_enter(e):
            self.port_entry.delete(0,'end')
        
        def on_leave(e):
            port=self.port_entry.get()
            if port=='':
                self.port_entry.insert(0,'Port #')
        
        def on_enter1(e):
            self.ipaddress_entry.delete(0,'end')
        
        def on_leave1(e):
            ip=self.ipaddress_entry.get()
            if ip=='':
                self.ipaddress_entry.insert(0,'IP Address')

        def on_enter2(e):
            self.user_entry.delete(0,'end')

        def on_leave2(e):
            users=self.user_entry.get()
            if users=='':
                self.user_entry.insert(0,'Username')
                
        def on_enter3(e):
            self.password_entry.delete(0,'end')

        def on_leave3(e):
            password=self.password_entry.get()
            if password=='':
                self.password_entry.insert(0,'Password')

                
        style = ttk.Style(self)
        style.theme_use("clam")
        
        #Port
        self.portvar = StringVar()
        self.port_entry = ttk.Entry(self.border, width=20, foreground="gray", font=('Calibre', 10))
        self.port_entry.pack(pady=12, padx=10)
        self.port_entry.insert(0, "Port #")
        self.port_entry.bind('<FocusIn>', on_enter)
        self.port_entry.bind('<FocusOut>', on_leave)
        
        #ipaddress
        self.ipaddressvar = StringVar()
        self.ipaddress_entry = ttk.Entry(self.border, width=20, foreground="gray", font=('Calibre', 10))
        self.ipaddress_entry.pack(pady=12, padx=10)
        self.ipaddress_entry.insert(0, "IP Address")
        self.ipaddress_entry.bind('<FocusIn>', on_enter1)
        self.ipaddress_entry.bind('<FocusOut>', on_leave1)
        
        #username
        self.user_entry = ttk.Entry(self.border, width=20, foreground="gray", font=('Calibre', 10))
        self.user_entry.pack(pady=12, padx=10)
        self.user_entry.insert(0, "Username")
        self.user_entry.bind('<FocusIn>', on_enter2)
        self.user_entry.bind('<FocusOut>', on_leave2)
        
        #password
        self.password_entry = ttk.Entry(self.border, width=20, foreground="gray", font=('Calibre', 10))
        self.password_entry.pack(pady=12, padx=10)
        self.password_entry.insert(0, "Password")
        self.password_entry.bind('<FocusIn>', on_enter3)
        self.password_entry.bind('<FocusOut>', on_leave3)
        
        Button = tk.Button(self.border, text="Login", width=20,
                            background="#0099ff",
                            foreground="white",
                            activebackground="#008ae6",
                            activeforeground="white",
                            highlightthickness=2,
                            highlightbackground="#0099ff",
                            highlightcolor="white",
                            border=0,
                            command=self.verify)
        Button.pack(pady=12, padx=10)
        
        
    def verify(self):
                
        port = self.port_entry.get()
        ipaddress = self.ipaddress_entry.get()
        username = self.user_entry.get()
        password = self.password_entry.get()
        global router
        global PrimaryStatus
        # global SecondaryStatus
        global RISEBtnState
        # global PLDTBtnState
                
        if (ipaddress == '' or username == '' or password == ''):
            messagebox.showerror('Login error', 'Please input credentials')
        else:
            try:
                router = ros_api.Api(ipaddress, user=username, password=password, verbose=False, use_ssl=False, port=port)
                messagebox.showinfo("Login", "Login Successful")
                self.controller.set_username(username)
                self.controller.set_ipaddress(ipaddress)
                self.controller.set_port(port)
                
                #~~~ Router Identity ~~~#
                routerResponse = router.talk('/system/identity/print')
                print(routerResponse)
                identity = routerResponse[0]

                identityKeys = list(identity.keys())
                identityName = identityKeys[1]
                identityValue = identity[identityName]
                
                self.controller.set_identity(identityValue)
                
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ISP STATUS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
                
                # routerResponse = router.talk('/interface/print')
                # PrimaryISP = routerResponse[0]

                # Primarykeys = list(PrimaryISP.keys())  # Get the list of keys
                # PrimaryName = Primarykeys[26]
                # PrimaryStatus = PrimaryISP[PrimaryName]  # Access the value associated with the key
                
                # self.controller.Primary_Status(PrimaryStatus)
                #print("login",RISEStatus)
                
                # SecondaryISP = routerResponse[1]

                # Secondarykeys = list(SecondaryISP.keys())  # Get the list of keys
                # SecondaryName = Secondarykeys[26]
                # SecondaryStatus = SecondaryISP[SecondaryName]  # Access the value associated with the key
                
                # self.controller.Secondary_Status(SecondaryStatus)
                
                # if PrimaryStatus == "true":
                #         # RISEBtnState = 1
                #         self.controller.Primary_Status(PrimaryStatus)
                # else:
                #     # RISEBtnState = 0
                #     self.controller.Primary_Status(PrimaryStatus)
                    
                # if SecondaryStatus == "true":
                #         PLDTBtnState = 1
                #         self.controller.Secondary_Status(SecondaryStatus)
                # else:
                #     PLDTBtnState = 0
                #     self.controller.Secondary_Status(SecondaryStatus)
                
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
                self.controller.show_frame(Mainpage)
                
            except:
                messagebox.showinfo("Login Error", "Incorrect credentials")
            

class Mainpage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller = controller
        
        self.configure(bg="white")
        
        self.NavFrame = tk.LabelFrame(self)
        self.NavFrame.pack(anchor="n", fill="both", ipadx="20", ipady="15",expand=False)
        
        self.Welcome = tk.Label(self.NavFrame, text="", bg="#f2f2f2", font=("Helvitica", 10))
        self.Welcome.place(in_=self.NavFrame, x="10", y="3")
        
        self.RouterIdentity =tk.Label(self.NavFrame, text="", bg="#f2f2f2", font=("Helvitica", 10))
        self.RouterIdentity.place(in_=self.NavFrame, x="150", y="3")
        
        Button = tk.Button(self.NavFrame, text="Logout",
                            background="#0099ff",
                            foreground="white",
                            activebackground="#008ae6",
                            activeforeground="white",
                            highlightthickness=2,
                            highlightbackground="#0099ff",
                            highlightcolor="white",
                            border=0,
                            command="")
        Button.place(in_=self.NavFrame, x="747", y="1" )
        
        risebtn_inactive = Image.open("image/rise_btn_inact.png")
        risebtn_active = Image.open("image/rise_btn_act.png")
        pldtbtn_inactive = Image.open("image/pldt_btn_inact.png")
        pldtbtn_active = Image.open("image/pldt_btn_act.png")
        apnbtn_inactive = Image.open("image/apn_btn_inact.png")
        apnbtn_active = Image.open("image/apn_btn_act.png")
        settingsbtn = Image.open("image/settings.png")
        
        self.settingsbtn = ImageTk.PhotoImage(settingsbtn)        
        self.risebtn_inactive = ImageTk.PhotoImage(risebtn_inactive)
        self.risebtn_active = ImageTk.PhotoImage(risebtn_active)
        
        self.pldtbtn_inactive = ImageTk.PhotoImage(pldtbtn_inactive)
        self.pldtbtn_active = ImageTk.PhotoImage(pldtbtn_active)
        
        self.apnbtn_inactive = ImageTk.PhotoImage(apnbtn_inactive)
        self.apnbtn_active = ImageTk.PhotoImage(apnbtn_active) 
        
        def update_ISP_Status():
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
            
            routerResponse = router.talk('/interface/print')
            PrimaryISP = routerResponse[0]

            Primarykeys = list(PrimaryISP.keys())  # Get the list of keys
            PrimaryName = Primarykeys[26]
            PrimaryStatus = PrimaryISP[PrimaryName]  # Access the value associated with the key
            
            SecondaryISP = routerResponse[1]

            Secondarykeys = list(SecondaryISP.keys())  # Get the list of keys
            SecondaryName = Secondarykeys[26]
            SecondaryStatus = SecondaryISP[SecondaryName]  # Access the value associated with the key
            
            # if PrimaryStatus == "true":
            #     self.RISE_label.configure(text=f"RISE: In Active", fg="gray")
                #print("main inactive", RISEStatus)
            # else:
            #     self.RISE_label.configure(text=f"RISE: Active", fg="black")
            #     #print("main active", RISEStatus)
                
            # if SecondaryStatus == "true":
            #     self.PLDT_label.configure(text=f"PLDT: In Active", fg="gray")
            #     #print("main inactive", RISEStatus)
            # else:
            #     self.PLDT_label.configure(text=f"PLDT: Active", fg="black")
            #     #print("main active", RISEStatus)
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        RISEBtnState = 0
        PLDTBtnState = 0
        
        # def riseOff():
        #     r = router.talk('/interface/ethernet/disable\n=numbers=0')
        #     print("RISE Disable")
        #     self.rise_btn.config(image=self.risebtn_inactive, command=riseOn)
        #     update_ISP_Status()
        # def riseOn():
        #     r = router.talk('/interface/ethernet/enable\n=numbers=0')
        #     print("RISE Enable")
        #     self.rise_btn.config(image=self.risebtn_active, command=riseOff)
        #     update_ISP_Status()
            
        # def pldtOff():
        #     r = router.talk('/interface/ethernet/disable\n=numbers=1')
        #     print("PLDT Disable")
        #     self.pldt_btn.config(image=self.pldtbtn_inactive, command=pldtOn)
        #     update_ISP_Status()
        # def pldtOn():
        #     r = router.talk('/interface/ethernet/enable\n=numbers=1')
        #     print("PLDT Enable")
        #     self.pldt_btn.config(image=self.pldtbtn_active, command=pldtOff)
        #     update_ISP_Status()
                
        # def RISEButton_cmd():
        #     if RISEBtnState == 1:
        #         riseOn()
        #         RISEBtnState == 0
        #     else:
        #         riseOff()
        #         RISEBtnState == 1
                
        # def PLDTButton_cmd():
        #     if PLDTBtnState == 1:
        #         pldtOn()
        #         PLDTBtnState == 0
        #     else:
        #         pldtOff()
        #         PLDTBtnState == 1
            
        self.rise_btn = tk.Button(self, image=self.risebtn_inactive, bg="white", bd=0, relief="sunken", activebackground="white", 
                                command="")
        self.rise_btn.place(x="220", y="350")
        
        self.pldt_btn = tk.Button(self, image=self.pldtbtn_inactive, bg="white", bd=0, relief="sunken", activebackground="white",
                                command="")
        self.pldt_btn.place(x="420", y="350")
        
        self.apn_btn = tk.Button(self, image=self.apnbtn_inactive, bg="white", bd=0, relief="sunken", activebackground="white")
        self.apn_btn.place(x="620", y="350")
        
        self.System = tk.LabelFrame(self, bg="white")
        self.System.pack(side="left", fill="both", ipadx="100", ipady="5", expand=False)
        
        #~~~ ISP Status ~~~#
        
        self.Status_label = tk.Label(self.System, text="ISP Status", bg="white", font=("Helvitica", 13))
        self.Status_label.place(x="10", y="50")
        
        self.RISE_label = tk.Label(self.System, text="", fg="black", bg="white", font=("Helvitica", 13))
        self.RISE_label.place(x="10", y="100")
        
        self.PLDT_label = tk.Label(self.System, text="PLDT:", bg="white", font=("Helvitica", 13))
        self.PLDT_label.place(x="10", y="150")
        
        self.APN_label = tk.Label(self.System, text="APN:", bg="white", font=("Helvitica", 13))
        self.APN_label.place(x="10", y="200")
        
        self.System_label = tk.Label(self.System, text="Router Health", bg="white", font=("Helvitica", 13))
        self.System_label.place(x="10", y="250")
        
    def update_welcome_message(self, username):
        self.Welcome.configure(text=f'Login as {username}')
        
    def update_router_identity(self, identityValue):
        self.RouterIdentity.configure(text=f'Router Identity : {identityValue}')
        
    # def query_Primary_Status(self, PrimaryStatus):
    #     if PrimaryStatus == "true":
    #         self.RISE_label.configure(text=f"RISE: In Active", fg="gray")
    #         self.rise_btn.config(image=self.risebtn_inactive)
    #         RISEBtnState = 0
    #         #print("main inactive", PrimaryStatus)
    #     else:
    #         self.RISE_label.configure(text=f"RISE: Active", fg="black")
    #         self.rise_btn.config(image=self.risebtn_active)
    #         RISEBtnState = 1
            #print("main active", PrimaryStatus)
            
    # def query_Secondary_Status(self, SecondaryStatus):
    #     if SecondaryStatus == "true":
    #         self.PLDT_label.configure(text=f"PLDT: In Active", fg="gray")
    #         self.pldt_btn.config(image=self.pldtbtn_inactive)
    #         PLDTBtnState = 0
    #         #print("main inactive", PrimaryStatus)
    #     else:
    #         self.PLDT_label.configure(text=f"PLDT: Active", fg="black")
    #         self.pldt_btn.config(image=self.pldtbtn_active)
    #         PLDTBtnState = 1
    #         #print("main active", PrimaryStatus)
            
        # def configISP():
        #     config = tk.Tk()
        #     config.title("ISP Configuration")
        #     config.geometry("300x200")
                    
            # configPrimary = tk.Label(configISP, text="Primary ISP", font=("Helvitica", 12))
            # configPrimary.place()
            # configSecondary = tk.Label(configISP, text="Secondary ISP", font=("Helvitica", 12))
            # configSecondary.place()
            # configTertiary = tk.Label(configISP, text="Tertiary ISP", font=("Helvitica", 12))
            # configTertiary.place()
        
        # settings_btn = tk.Button(self.NavFrame, image=self.settingsbtn, bg="#f2f2f2",
        #                             activeforeground="#f2f2f2", highlightbackground="#f2f2f2",
        #                             highlightcolor="white", border=0, bd=0, relief="sunken", activebackground="#f2f2f2", 
        #                             command="")
        # settings_btn.place(in_=self.NavFrame, x="715", y="1")
        
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.username = None
        self.ipaddress = None
        
        #create window
        window = tk.Frame(self)
        window.pack()
        self.title("BPOSeats ISP Switcher")
        self.iconbitmap("image/icon.ico")
        self.resizable(False,False)
        
        window.grid_rowconfigure(0, minsize = 500)
        window.grid_columnconfigure(0, minsize= 800)
                
        self.frames = {}
        for F in (Loginpage, Mainpage):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(Loginpage)
        
    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        
        if page == Mainpage:
            frame.update_welcome_message(self.username)
            frame.update_router_identity(self.identityValue)
            # frame.query_Primary_Status(self.PrimaryStatus)
            # frame.query_Secondary_Status(self.SecondaryStatus)
        
    def set_username(self, username):
        self.username = username
        
    def set_ipaddress(self, ipaddress):
        self.ipaddress = ipaddress
        
    def set_port(self, port):
        self.port = port
        
    def set_identity(self, identityValue):
        self.identityValue = identityValue
        
    # def Primary_Status(self, PrimaryStatus):
        # self.PrimaryStatus = PrimaryStatus

    # def Secondary_Status(self, SecondaryStatus):
    #     self.SecondaryStatus = SecondaryStatus
            

app = Application()
app.mainloop()