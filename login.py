from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import pymysql
from main import Face_Recognition_System

def main():
    win=Tk()
    app=Login_Window(win)
    win.mainloop()

class Login_Window:
    def __init__(self,root):
        self.root=root
        self.root.title("Login")
        self.root.geometry("1550x800+0+0")
        self.new_window=None

        #variables
        self.var_email=StringVar()
        self.var_pass=StringVar()

        self.bg=ImageTk.PhotoImage(file=r"Images\bg3.jpg")
        lbl_bg=Label(self.root,image=self.bg)
        lbl_bg.place(x=0,y=0,relwidth=1,relheight=1)

        #Frame
        frame=Frame(self.root,bg="black")
        frame.place(x=610,y=170,width=340,height=450)

        img1=Image.open("log1.png")
        img1 = img1.resize((100,100),Image.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)

        lblimg1 = Label(self.root,image=self.photoimg1,bg="black",borderwidth=0)
        lblimg1.place(x=730,y=175,width=100,height=100)

        get_str=Label(frame,text="Get Started",font=("times new roman",20,"bold"),fg="white",bg="black")
        get_str.place(x=95,y=100)

        #Username label
        usernamelbl=Label(frame,text="Username",font=("times new roman",15,"bold"),fg="white",bg="black")
        usernamelbl.place(x=70,y=155)

        self.txtuser=ttk.Entry(frame,font=("times new roman",15,"bold"))
        self.txtuser.place(x=40,y=180,width=270)

        passwordlbl=Label(frame,text="Password",font=("times new roman",15,"bold"),fg="white",bg="black")
        passwordlbl.place(x=70,y=225)

        self.passuser=ttk.Entry(frame,font=("times new roman",15,"bold"))
        self.passuser.place(x=40,y=250,width=270)

        #****ICON IMAGES*****

        img2=Image.open("log1.png")
        img2 = img2.resize((25,25),Image.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)

        lblimg2 = Label(image=self.photoimg2,bg="black",borderwidth=0)
        lblimg2.place(x=650,y=323,width=25,height=25)

        img3=Image.open(r"Images\password_icon.jpg")
        img3 = img3.resize((25,25),Image.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)

        lblimg3 = Label(image=self.photoimg3,bg="black",borderwidth=0)
        lblimg3.place(x=650,y=395,width=25,height=25)

        #Login Button

        loginbtn=Button(frame,text="Login",command=self.login,font=("times new roman",15,"bold"),bd=3,relief=RIDGE,fg="white",bg="blue",activeforeground="white",activebackground="blue")
        loginbtn.place(x=110,y=300,width=120,height=35)

        #Register Button

        registerbtn=Button(frame,text="New User Register",command=self.register_window,font=("times new roman",10,"bold"),borderwidth=0,fg="white",bg="black",activeforeground="white",activebackground="black")
        registerbtn.place(x=15,y=350,width=160)

        #Forgot Password

        btn=Button(frame,text="Forgot Password",command=self.forgot_password_window,font=("times new roman",10,"bold"),borderwidth=0,fg="white",bg="black",activeforeground="white",activebackground="black")
        btn.place(x=10,y=370,width=160)
    
    def register_window(self):
        self.new_window=Toplevel(self.root)
        self.app = Register(self.new_window)

    def login(self):
        if self.txtuser.get()=="" or self.passuser.get()=="":
            messagebox.showerror("Error","All Fields Requrired")
        elif self.txtuser.get()=="kapu" and self.passuser.get()=="ashu":
            messagebox.showinfo("Sucess","welcome to the Kalasalingam University face Recognition system")
        else:
            try:
                conn = pymysql.connect(host="localhost",user="root",password="W7301@jqir#",database="register")
                my_cursor=conn.cursor()
                query=("select * from register where email=%s and password=%s")
                value=(self.txtuser.get(),self.passuser.get())
                my_cursor.execute(query,value)
                row=my_cursor.fetchone()
                if row==None:
                    messagebox.showerror("Invalid Username and password")
                else:
                    open_main=messagebox.askyesno("YesNo","Acsess only admin")
                    if open_main >0:
                        self.new_window=Toplevel(self.new_window)
                        self.app=Face_Recognition_System(self.new_window)
                    else:
                        if not open_main:
                            return
            except Exception as e:
                messagebox.showerror("error",f"Error due to {e}")
                    
            conn.commit()
            conn.close()
    # Reset password Window
    def reset_password(self):
        if self.combo_security_Q.get()=="Select":
            messagebox.showerror("Error","Select Security Question",parent=self.root2)
        elif self.txt_security.get()=="":
            messagebox.showerror("Error","Please Enter the answer",parent=self.root2)
        elif self.new_password.get()=="":
            messagebox.showerror("Error","Please enter the new password",parent=self.root2)
        else:
            try:
                conn = pymysql.connect(host="localhost",user="root",password="W7301@jqir#",database="register")
                my_cursor=conn.cursor()
                query=("select * from register where email=%s and securityQ=%s and securityA=%s")
                value=(self.txtuser.get(),self.combo_security_Q.get(),self.txt_security.get())
                my_cursor.execute(query,value)
                row=my_cursor.fetchone()
                if row is None:
                    messagebox.showerror("Error","Please enter the correct answer",parent=self.root2)
                else:
                    query=("update register set password=%s where email=%s")
                    value=(self.new_password.get(),self.txtuser.get())
                    my_cursor.execute(query,value)

                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Info","Password hs been Reset",parent=self.root2)
                    self.root2.destroy()
            except Exception as e:
                messagebox.showerror("Error",f"Error due to {str(e)}")


    # Forgot Password Window
    def forgot_password_window(self):
        if self.txtuser.get()=="":
            messagebox.showerror("Error","Please enter email address to reset password")
        else:
            try:
                conn = pymysql.connect(host="localhost",user="root",password="W7301@jqir#",database="register")
                my_cursor=conn.cursor()
                query=("select * from register where email=%s")
                value=(self.txtuser.get(),)
                my_cursor.execute(query,value)
                row=my_cursor.fetchone()
                if row is None:
                    messagebox.showerror("My Error","Please Enter the Valid username")
                else:
                    conn.close()
                    self.root2=Toplevel()
                    self.root2.title("Forgot Password")
                    self.root2.geometry("340x450+610+170")
                    l=Label(self.root2,text="Forgot Password",font=("times new roman",15,"bold"),fg="red",bg="white")
                    l.place(x=0,y=10,relwidth=1)
                    security_Q=Label(self.root2,text="Select Security Questions",font=("times new roman",15,"bold"),bg="white")
                    security_Q.place(x=50,y=80)

                    self.combo_security_Q=ttk.Combobox(self.root2,font=("times new roman",13,"bold"),state="read only")
                    self.combo_security_Q["values"] =("Select","Your Birth Place","Your Friend Name","Your Pet name")
        
                    self.combo_security_Q.place(x=50,y=110,width=250)
                    self.combo_security_Q.current(0)



                    security_A=Label(self.root2,text="Security Answer",font=("times new roman",15,"bold"),bg="white")
                    security_A.place(x=50,y=150)

                    self.txt_security=ttk.Entry(self.root2,font=("times new roman",15,"bold"))
                    self.txt_security.place(x=50,y=180,width=250)

                    new_password=Label(self.root2,text="New Password",font=("times new roman",15,"bold"),bg="white")
                    new_password.place(x=50,y=220)

                    self.new_password=ttk.Entry(self.root2,font=("times new roman",15,"bold"))
                    self.new_password.place(x=50,y=250,width=250)

                    btn=Button(self.root2,command=self.reset_password,text="Reset",font=("times new roman",10,"bold"),borderwidth=0,fg="white",bg="green")
                    btn.place(x=100,y=290)
            except Exception as e:
                messagebox.showerror('Error',f"error Due to {str(e)}")


class Register:
    def __init__(self,root):
        self.root = root
        self.root.title("Register")
        self.root.geometry("1600x900+0+0")

        #****Variables*****
        self.var_fname=StringVar()
        self.var_lname=StringVar()
        self.var_contact=StringVar()
        self.var_email=StringVar()
        self.var_securityQ=StringVar()
        self.var_securityA=StringVar()
        self.var_pass=StringVar()
        self.var_confirmpass=StringVar()

        #Back ground Image

        self.bg=ImageTk.PhotoImage(file="bg3.jpg")
        bg_lbl=Label(self.root,image=self.bg)
        bg_lbl.place(x=0,y=0,relwidth=1,relheight=1)

        # Left Image

        self.bg1=ImageTk.PhotoImage(file="banner1.jpg")
        left_lbl=Label(self.root,image=self.bg1)
        left_lbl.place(x=50,y=100,width=470,height=550)

        #Frame

        frame=Frame(self.root,bg="white")
        frame.place(x=520,y=100,width=800,height=550)

        
        register_lbl=Label(frame,text="REGISTER HERE",font=("times new roman",20,"bold"),fg="darkgreen",bg="white")
        register_lbl.place(x=20,y=20)

        # Labels and Entry Fields

        fname=Label(frame,text="First Name",font=("times new roman",15,"bold"),bg="white")
        fname.place(x=50,y=100)

        fname_entry=ttk.Entry(frame,textvariable=self.var_fname,font=("times new roman",15,"bold"))
        fname_entry.place(x=50,y=130,width=250)

        l_name=Label(frame,text="Last Name",font=("times new roman",15,"bold"),bg="white")
        l_name.place(x=370,y=100)

        self.txt_lname=ttk.Entry(frame,textvariable=self.var_lname,font=("times new roman",15,"bold"))
        self.txt_lname.place(x=370,y=130,width=250)

        contact=Label(frame,text="Contact No",font=("times new roman",15,"bold"),bg="white")
        contact.place(x=50,y=170)

        self.txt_contact=ttk.Entry(frame,textvariable=self.var_contact,font=("times new roman",15,"bold"))
        self.txt_contact.place(x=50,y=200,width=250)

        email=Label(frame,text="Email",font=("times new roman",15,"bold"),bg="white")
        email.place(x=370,y=170)

        self.txt_email=ttk.Entry(frame,textvariable=self.var_email,font=("times new roman",15,"bold"))
        self.txt_email.place(x=370,y=200,width=250)

        security_Q=Label(frame,text="Select Security Questions",font=("times new roman",15,"bold"),bg="white")
        security_Q.place(x=50,y=240)

        self.combo_security_Q=ttk.Combobox(frame,textvariable=self.var_securityQ,font=("times new roman",13,"bold"),state="read only")
        self.combo_security_Q["values"] =("Select","Your Birth Place","Your Friend Name","Your Pet name")
        
        self.combo_security_Q.place(x=50,y=270,width=250)
        self.combo_security_Q.current(0)



        security_A=Label(frame,text="Security Answer",font=("times new roman",15,"bold"),bg="white")
        security_A.place(x=370,y=240)

        self.txt_security=ttk.Entry(frame,textvariable=self.var_securityA,font=("times new roman",15,"bold"))
        self.txt_security.place(x=370,y=270,width=250)

        pswd=Label(frame,text="Password",font=("times new roman",15,"bold"),bg="white")
        pswd.place(x=50,y=310)

        self.txt_pswd=ttk.Entry(frame,textvariable=self.var_pass,font=("times new roman",15,"bold"))
        self.txt_pswd.place(x=50,y=340,width=250)

        
        confirm_pswd=Label(frame,text="Confirm password",font=("times new roman",15,"bold"),bg="white")
        confirm_pswd.place(x=370,y=310)

        self.txt_confirm_pswd=ttk.Entry(frame,textvariable=self.var_confirmpass,font=("times new roman",15,"bold"))
        self.txt_confirm_pswd.place(x=370,y=340,width=250)

        #Check Button
        self.var_check=IntVar()
        checkbtn=Checkbutton(frame,variable=self.var_check,text="I agree the Terms & Conditions",font=("times new roman",12,"bold"),bg="white",onvalue=1,offvalue=0)
        checkbtn.place(x=50,y=380)

        #BUTTONS

        img = Image.open(r"Images\register.jpg")
        img = img.resize((200,50),Image.LANCZOS)
        self.photoimage = ImageTk.PhotoImage(img)

        b1 = Button(frame,command=self.register_data,image=self.photoimage,borderwidth=0,cursor="hand2")
        b1.place(x=10,y=420,width=200)

        img1 = Image.open(r"Images\login.jpg")
        img1 = img1.resize((200,50),Image.LANCZOS)
        self.photoimage1 = ImageTk.PhotoImage(img1)

        b2 = Button(frame,image=self.photoimage1,command=self.return_login,borderwidth=0,cursor="hand2")
        b2.place(x=330,y=420,width=200)

    #****FUNCTION DECLARATION*******
    def register_data(self):
        if self.var_fname.get()=="" or self.var_email.get()=="" or self.var_securityQ.get()=="":
            messagebox.showerror("Error","All fields are Required")
        elif self.var_pass.get() != self.var_confirmpass.get():
            messagebox.showerror("Error","Password & Confirm Password must be same")
        elif self.var_check.get()==0:
            messagebox.showerror("Error","Please agree the the terms & conditions")
        else:
            conn = pymysql.connect(host="localhost",user="root",password="W7301@jqir#",database="register")
            my_cursor=conn.cursor()
            query=("select * from register where email=%s")
            value=(self.var_email.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            if row != None:
                messagebox.showerror("Error","user already exists"," Please try with another email")
            else:
                my_cursor.execute("insert into register values (%s,%s,%s,%s,%s,%s,%s)",(
                            
                                                                                        self.var_fname.get(),
                                                                                        self.var_lname.get(),
                                                                                        self.var_contact.get(),
                                                                                        self.var_email.get(),
                                                                                        self.var_securityQ.get(),
                                                                                        self.var_securityA.get(),
                                                                                        self.var_pass.get()
                                                                                                                
                                                                                        ))
                conn.commit()
                conn.close()
                messagebox.showinfo("Sucess")
    def return_login(self):
        self.root.destroy()

                
if __name__== "__main__":
    main()
