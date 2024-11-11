from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import pymysql
import cv2

class Help:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("face Recognition System")

        title_lbl = Label(self.root,text="Help Desk",font=("times new roman",35,"bold"),bg='white',fg='green')
        title_lbl.place(x=0,y=0,width=1530,height=45)

        img_top = Image.open(r"Images\bgReg.jpg")
        img_top = img_top.resize((1530,720),Image.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)

        f_lbl = Label(self.root,image=self.photoimg_top)
        f_lbl.place(x=0,y=55,width=1530,height=720)

        hel_label=Label(self.root,text="Email:99220041532@klu.ac.in",font=("times new roman",18,"bold"),bg="white",fg="blue")
        hel_label.place(x=300,y=400)


if __name__ == "__main__":
    root=Tk()
    obj = Help(root)
    root.mainloop()