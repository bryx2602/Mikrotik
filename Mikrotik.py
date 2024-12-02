import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import ros_api

# ~~~ LOGIN Page ~~~ #
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
        
        # ~~~ Text Inputs ~~~ #
        def on_focus(e, placeholder_text):
            entry = e.widget
            current_value = entry.get()
            if e.type == '9':
                if current_value == placeholder_text:
                    entry.delete(0, 'end')
            elif e.type == '10':
                if current_value == '':
                    entry.insert(0, placeholder_text)
            else:
                print('error')
        
        def create_entry(placeholder_text):
            entry = ttk.Entry(self.border, width=20, foreground="gray", font=('Calibre', 10))
            entry.insert(0, placeholder_text)
            entry.bind('<FocusIn>', lambda e: on_focus(e, placeholder_text))
            entry.bind('<FocusOut>', lambda e: on_focus(e, placeholder_text))
            return entry

        # Port
        self.port_entry = create_entry("Port #")
        self.port_entry.pack(pady=12, padx=10)
        
        # IP Address
        self.ipaddress_entry = create_entry("IP Address")
        self.ipaddress_entry.pack(pady=12, padx=10)
        
        # Username
        self.user_entry = create_entry("Username")
        self.user_entry.pack(pady=12, padx=10)
        
        # Password
        self.password_entry = create_entry("Password")
        self.password_entry.pack(pady=12, padx=10)

        # Styling
        style = ttk.Style(self)
        style.theme_use("clam")
        
        # Login Button
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

        # ~~~ ISP Status ~~~ #
        global PrimaryStatus
        global SecondaryStatus
        global TertiaryStatus

        # ~~~ Buttons ~~~ #
        global RISEBtnState
        global PLDTBtnState
        global APNBtnState
                
        try:
            if (ipaddress == 'IP Address' or username == 'Username' or password == 'Password' or port == 'Port #'):
                messagebox.showerror('Login error', 'Please input credentials')
            else:
                router = ros_api.Api(ipaddress, user=username, password=password, verbose=False, use_ssl=False, port=port)
                messagebox.showinfo("Login", "Login Successful")
                self.controller.set_username(username)
                self.controller.set_ipaddress(ipaddress)
                self.controller.set_port(port)
                
                #~~~ Router Identity ~~~#
                routerResponse = router.talk('/system/identity/print')
                identity = routerResponse[0]
                identityName = identity['name']

                self.controller.set_identity(identityName)
                
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ISP STATUS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
                
                routerResponse = router.talk('/interface/print')

                # ~~~ RISE ~~~ #
                PrimaryISP = routerResponse[0]
                PrimaryStatus = PrimaryISP['disabled']

                # ~~~ PLDT ~~~ #
                SecondaryISP = routerResponse[1]
                SecondaryStatus = SecondaryISP['disabled']

                # ~~~ APN ~~~ #
                TertiaryISP = routerResponse[2]
                TertiaryStatus = TertiaryISP['disabled']
                
                # ~~~~~~~~~~ RISE ~~~~~~~~~~ #
                if PrimaryStatus == "true":
                        RISEBtnState = 1
                        self.controller.Primary_Status(PrimaryStatus)
                else:
                    RISEBtnState = 0
                    self.controller.Primary_Status(PrimaryStatus)
                
                # ~~~~~~~~~~ PLDT ~~~~~~~~~~ #
                if SecondaryStatus == "true":
                        PLDTBtnState = 1
                        self.controller.Secondary_Status(SecondaryStatus)
                else:
                    PLDTBtnState = 0
                    self.controller.Secondary_Status(SecondaryStatus)

                # ~~~~~~~~~~ APN ~~~~~~~~~~ #
                if TertiaryStatus == "true":
                        APNBtnState = 1
                        self.controller.Tertiary_Status(TertiaryStatus)
                else:
                    APNBtnState = 0
                    self.controller.Tertiary_Status(TertiaryStatus)
                
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
                
                self.controller.show_frame(Mainpage)
        except:
            messagebox.showinfo("Login Error", "Incorrect credentials")
            

class Mainpage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # ~~~ Logout ~~~ #
        def logout():
            self.controller.show_frame(Loginpage)
        
        self.controller = controller
        
        self.configure(bg="white")
        
        self.NavFrame = tk.LabelFrame(self)
        self.NavFrame.pack(anchor="n", fill="both", ipadx="20", ipady="15",expand=False)
        
        self.Welcome = tk.Label(self.NavFrame, text="", bg="#f2f2f2", font=("Helvitica", 10))
        self.Welcome.place(in_=self.NavFrame, x="10", y="3")
        
        self.RouterIdentity =tk.Label(self.NavFrame, text="", bg="#f2f2f2", font=("Helvitica", 10))
        self.RouterIdentity.place(in_=self.NavFrame, x="150", y="3")
        
        # ~~~ LOGOUT Button ~~~ #
        Button = tk.Button(self.NavFrame, text="Logout",
                            background="#0099ff",
                            foreground="white",
                            activebackground="#008ae6",
                            activeforeground="white",
                            highlightthickness=2,
                            highlightbackground="#0099ff",
                            highlightcolor="white",
                            border=0,
                            command=logout)
        
        Button.place(in_=self.NavFrame, x="747", y="1" )
        
        # ~~~ RISE button image ~~~ #
        risebtn_inactive = Image.open("image/rise_btn_inact.png")
        risebtn_active = Image.open("image/rise_btn_act.png")

        # ~~~ PLDT button image ~~~ #
        pldtbtn_inactive = Image.open("image/pldt_btn_inact.png")
        pldtbtn_active = Image.open("image/pldt_btn_act.png")

        # ~~~ APN button image ~~~ #
        apnbtn_inactive = Image.open("image/apn_btn_inact.png")
        apnbtn_active = Image.open("image/apn_btn_act.png")

        settingsbtn = Image.open("image/settings.png")
        
        self.settingsbtn = ImageTk.PhotoImage(settingsbtn)

        # ~~~ RISE button image ~~~ #
        self.risebtn_inactive = ImageTk.PhotoImage(risebtn_inactive)
        self.risebtn_active = ImageTk.PhotoImage(risebtn_active)
        
        # ~~~ PLDT button image ~~~ #
        self.pldtbtn_inactive = ImageTk.PhotoImage(pldtbtn_inactive)
        self.pldtbtn_active = ImageTk.PhotoImage(pldtbtn_active)
        
        # ~~~ APN button image ~~~ #
        self.apnbtn_inactive = ImageTk.PhotoImage(apnbtn_inactive)
        self.apnbtn_active = ImageTk.PhotoImage(apnbtn_active) 
        
        # ~~~ Update ISP ~~~ #
        def update_ISP_Status():
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

            routerResponse = router.talk('/interface/print')

            # ~~~ RISE ~~~ #
            PrimaryISP = routerResponse[0]
            PrimaryStatus = PrimaryISP['disabled']

            # ~~~ PLDT ~~~ #
            SecondaryISP = routerResponse[1]
            SecondaryStatus = SecondaryISP['disabled']

            # ~~~ APN ~~~ #
            TertiaryISP = routerResponse[2]
            TertiaryStatus = TertiaryISP['disabled']
            
            # ~~~ RISE ~~~ #
            if PrimaryStatus == "true":
                self.RISE_label.configure(text=f"RISE: Inactive", fg="gray")
            else:
                self.RISE_label.configure(text=f"RISE: Active", fg="black")
            
            # ~~~ PLDT ~~~ #
            if SecondaryStatus == "true":
                self.PLDT_label.configure(text=f"PLDT: Inactive", fg="gray")
            else:
                self.PLDT_label.configure(text=f"PLDT: Active", fg="black")
            
            # ~~~ APN ~~~ #
            if TertiaryStatus == "true":
                self.APN_label.configure(text=f"APN: Inactive", fg="gray")
            else:
                self.APN_label.configure(text=f"APN: Active", fg="black")
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        
        # ~~~ RISE ~~~ #
        def riseOff():
            r = router.talk('/interface/ethernet/disable\n=numbers=0')
            self.rise_btn.config(image=self.risebtn_inactive, command=riseOn)
            update_ISP_Status()

        def riseOn():
            r = router.talk('/interface/ethernet/enable\n=numbers=0')
            self.rise_btn.config(image=self.risebtn_active, command=riseOff)
            update_ISP_Status()
        
        # ~~~ PLDT ~~~ #
        def pldtOff():
            r = router.talk('/interface/ethernet/disable\n=numbers=1')
            self.pldt_btn.config(image=self.pldtbtn_inactive, command=pldtOn)
            update_ISP_Status()

        def pldtOn():
            r = router.talk('/interface/ethernet/enable\n=numbers=1')
            self.pldt_btn.config(image=self.pldtbtn_active, command=pldtOff)
            update_ISP_Status()

        # ~~~ APN ~~~ #
        def apnOff():
            r = router.talk('/interface/ethernet/disable\n=numbers=2')
            self.apn_btn.config(image=self.apnbtn_inactive, command=apnOn)
            update_ISP_Status()

        def apnOn():
            r = router.talk('/interface/ethernet/enable\n=numbers=2')
            self.apn_btn.config(image=self.apnbtn_active, command=apnOff)
            update_ISP_Status()

        # ~~~ RISE ~~~ #      
        def RISEButton_cmd():
            if RISEBtnState == 1:
                riseOn()
                RISEBtnState == 0
            else:
                riseOff()
                RISEBtnState == 1

        # ~~~ PLDT ~~~ #      
        def PLDTButton_cmd():
            if PLDTBtnState == 1:
                pldtOn()
                PLDTBtnState == 0
            else:
                pldtOff()
                PLDTBtnState == 1

        # ~~~ APN ~~~ #
        def APNButton_cmd():
            if APNBtnState == 1:
                apnOn()
                APNBtnState == 0
            else:
                apnOff()
                APNBtnState == 1
        
        # ~~~ RISE button ~~~ #
        self.rise_btn = tk.Button(self, image=self.risebtn_inactive,
                                  bg="white", bd=0,
                                  relief="sunken",
                                  activebackground="white", 
                                  command=RISEButton_cmd)
        
        self.rise_btn.place(x="220", y="350")
        # ~~~ PLDT button ~~~ #
        self.pldt_btn = tk.Button(self, image=self.pldtbtn_inactive,
                                  bg="white",
                                  bd=0,
                                  relief="sunken",
                                  activebackground="white",
                                  command=PLDTButton_cmd)
        
        self.pldt_btn.place(x="420", y="350")
        # ~~~ APN button ~~~ #
        self.apn_btn = tk.Button(self, image=self.apnbtn_inactive,
                                 bg="white",
                                 bd=0,
                                 relief="sunken",
                                 activebackground="white",
                                 command=APNButton_cmd)
        
        self.apn_btn.place(x="620", y="350")
        
        self.System = tk.LabelFrame(self, bg="white")
        self.System.pack(side="left", fill="both", ipadx="100", ipady="5", expand=False)
        
        #~~~ ISP Status ~~~#
        
        self.Status_label = tk.Label(self.System, text="ISP Status", bg="white", font=("Helvitica", 13))
        self.Status_label.place(x="10", y="50")
        
        self.RISE_label = tk.Label(self.System, text="RISE:", fg="black", bg="white", font=("Helvitica", 13))
        self.RISE_label.place(x="10", y="100")
        
        self.PLDT_label = tk.Label(self.System, text="PLDT:", bg="white", font=("Helvitica", 13))
        self.PLDT_label.place(x="10", y="150")
        
        self.APN_label = tk.Label(self.System, text="APN:", bg="white", font=("Helvitica", 13))
        self.APN_label.place(x="10", y="200")
        
        self.System_label = tk.Label(self.System, text="Router Health", bg="white", font=("Helvitica", 13))
        self.System_label.place(x="10", y="250")
        
    def update_welcome_message(self, username):
        self.Welcome.configure(text=f'Login as {username}')
        
    def update_router_identity(self, identityName):
        self.RouterIdentity.configure(text=f'Router Identity : {identityName}')
    
    # ~~~ RISE ~~~ #
    def query_Primary_Status(self, PrimaryStatus):
        if PrimaryStatus == "true":
            self.RISE_label.configure(text=f"RISE: Inactive", fg="gray")
            self.rise_btn.config(image=self.risebtn_inactive)
            RISEBtnState = 0
        else:
            self.RISE_label.configure(text=f"RISE: Active", fg="black")
            self.rise_btn.config(image=self.risebtn_active)
            RISEBtnState = 1

    # ~~~ PLDT ~~~ #
    def query_Secondary_Status(self, SecondaryStatus):
        if SecondaryStatus == "true":
            self.PLDT_label.configure(text=f"PLDT: Inactive", fg="gray")
            self.pldt_btn.config(image=self.pldtbtn_inactive)
            PLDTBtnState = 0
        else:
            self.PLDT_label.configure(text=f"PLDT: Active", fg="black")
            self.pldt_btn.config(image=self.pldtbtn_active)
            PLDTBtnState = 1

    # ~~~ APN ~~~ #
    def query_Tertiary_Status(self, TertiaryStatus):
        if TertiaryStatus == "true":
            self.APN_label.configure(text=f"APN: Inactive", fg="gray")
            self.apn_btn.config(image=self.apnbtn_inactive)
            APNBtnState = 0
        else:
            self.APN_label.configure(text=f"APN: Active", fg="black")
            self.apn_btn.config(image=self.apnbtn_active)
            APNBtnState = 1
            
        def configISP():
            config = tk.Tk()
            config.title("ISP Configuration")
            config.geometry("300x200")
                    
            configPrimary = tk.Label(configISP, text="Primary ISP", font=("Helvitica", 12))
            configPrimary.place()
            configSecondary = tk.Label(configISP, text="Secondary ISP", font=("Helvitica", 12))
            configSecondary.place()
            configTertiary = tk.Label(configISP, text="Tertiary ISP", font=("Helvitica", 12))
            configTertiary.place()
        
        settings_btn = tk.Button(self.NavFrame, image=self.settingsbtn, bg="#f2f2f2",
                                    activeforeground="#f2f2f2", highlightbackground="#f2f2f2",
                                    highlightcolor="white", border=0, bd=0, relief="sunken", activebackground="#f2f2f2", 
                                    command="")
        settings_btn.place(in_=self.NavFrame, x="715", y="1")
        
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
            frame.update_router_identity(self.identityName)
            frame.query_Primary_Status(self.PrimaryStatus)
            frame.query_Secondary_Status(self.SecondaryStatus)
            frame.query_Tertiary_Status(self.TertiaryStatus)

    def set_username(self, username):
        self.username = username
        
    def set_ipaddress(self, ipaddress):
        self.ipaddress = ipaddress
        
    def set_port(self, port):
        self.port = port
        
    def set_identity(self, identityName):
        self.identityName = identityName
    
    # ~~~ RISE ~~~ #
    def Primary_Status(self, PrimaryStatus):
        self.PrimaryStatus = PrimaryStatus

    # ~~~ PLDT ~~~ #
    def Secondary_Status(self, SecondaryStatus):
        self.SecondaryStatus = SecondaryStatus

    # ~~~ APN ~~~ #
    def Tertiary_Status(self, TertiaryStatus):
        self.TertiaryStatus = TertiaryStatus
            

app = Application()
app.mainloop()