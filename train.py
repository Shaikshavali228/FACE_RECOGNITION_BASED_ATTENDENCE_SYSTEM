from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import pymysql
import cv2
import os
import numpy as np

class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        title_lbl = Label(self.root, text="TRAIN DATASET", font=("times new roman", 35, "bold"), bg='white', fg='red')
        title_lbl.place(x=0, y=0, width=1530, height=45)

        img_top = Image.open(r"Images\face_img.jpg")
        img_top = img_top.resize((1530, 325), Image.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)

        f_lbl = Label(self.root, image=self.photoimg_top)
        f_lbl.place(x=0, y=55, width=1530, height=325)

        b9_9 = Button(self.root, text="Train Data", command=self.train_classifier, cursor="hand2", font=("times new roman", 30, "bold"), bg='red', fg='white')
        b9_9.place(x=0, y=380, width=1530, height=60)

        img_bottom = Image.open(r"Images/studentpy2.jpg")
        img_bottom = img_bottom.resize((1530, 325), Image.LANCZOS)
        self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)

        f_lbl = Label(self.root, image=self.photoimg_bottom)
        f_lbl.place(x=0, y=440, width=1530, height=325)

    def train_classifier(self):
        data_dir = "data"
        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if file.endswith(('jpg', 'png'))]
        faces = []
        ids = []
        for image in path:
            img = Image.open(image).convert('L')  # Gray Scale Image
            imageNp = np.array(img, 'uint8')
            id = int(os.path.split(image)[1].split('.')[1])  # Extracting ID from filename
            faces.append(imageNp)
            ids.append(id)
            cv2.imshow("Training", imageNp)
            if cv2.waitKey(1) == 13:  # Wait for Enter key
                break
        ids = np.array(ids)

        # Train the Classifier and Save
        try:
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.train(faces, ids)
            clf.save("classifier.xml")  # Save the trained model
            cv2.destroyAllWindows()
            messagebox.showinfo("Result", "Training datasets completed!")

        except Exception as e:
            messagebox.showerror("Error", f"Due to : {e}")

if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()
