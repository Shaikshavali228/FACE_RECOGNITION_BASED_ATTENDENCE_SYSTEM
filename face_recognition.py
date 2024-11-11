import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import *
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import pymysql
from datetime import datetime, timedelta
from fpdf import FPDF
import os
import qrcode
import time

# Email credentials
sender_email = '99220041532@klu.ac.in'
sender_password = '99220041532'

class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        title_lbl = Label(self.root, text="FACE RECOGNITION", font=("times new roman", 35, "bold"), bg='white', fg='green')
        title_lbl.place(x=0, y=0, width=1530, height=45)

        # First Image
        img_top = Image.open(r"Images/studentpy1.jpg")
        img_top = img_top.resize((650, 700), Image.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)
        f_lbl = Label(self.root, image=self.photoimg_top)
        f_lbl.place(x=0, y=55, width=650, height=700)

        # Second Image
        img_bottom = Image.open(r"Images/studentpy2.jpg")
        img_bottom = img_bottom.resize((950, 700), Image.LANCZOS)
        self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)
        f_lbl = Label(self.root, image=self.photoimg_bottom)
        f_lbl.place(x=600, y=55, width=950, height=700)

        # Face Recognition Button
        b10_10 = Button(f_lbl, text="Face Recognition", command=self.face_recog, cursor="hand2", font=("times new roman", 18, "bold"), bg='darkgreen', fg='white')
        b10_10.place(x=365, y=620, width=200, height=40)

    def on_closing(self):
        """Handle the closing of both Tkinter and OpenCV windows."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            cv2.destroyAllWindows()

    def mark_attendance(self, student_id, roll, name, department, email):
        with open("attendance.csv", "r+", newline="\n") as f:
            myDataList = f.readlines()
            name_list = [line.split(",")[0] for line in myDataList]

            if student_id not in name_list:
                now = datetime.now()
                date_str = now.strftime("%d/%m/%Y")
                time_str = now.strftime("%H:%M:%S")
                f.writelines(f"\n{student_id},{roll},{name},{department},Present,{email},{time_str},{date_str}")
                self.generate_slip(student_id, roll, name, department)
                messagebox.showinfo("Recognition Successful", f"Student {name} recognized and attendance marked.")
            else:
                messagebox.showwarning("Duplicate Punch", f"Student {name} has already punched in today.")

    def generate_slip(self, student_id, roll, name, department):
        # Create a directory named "slip" if it doesn't exist
        if not os.path.exists("slip"):
            os.makedirs("slip")

        # Get current date and time
        now = datetime.now()
        current_date = now.strftime("%d/%m/%Y")
        current_time = now.strftime("%H:%M:%S")

        # Create a QR code with student details and current time
        qr_data = (f"ID: {student_id}, Name: {name}, Roll: {roll}, Department: {department}, "
                   f"Date: {current_date}, Time: {current_time}")
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill="black", back_color="white")
        
        # Save the QR code image
        qr_img_path = f"slip/qr_{student_id}.png"
        qr_img.save(qr_img_path)

        # Initialize PDF
        pdf = FPDF()
        pdf.add_page()

        # Set title
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, txt="Student Attendance Slip", ln=True, align="C")

        # Student details
        pdf.set_font("Arial", size=12)
        pdf.ln(10)  # Line break
        pdf.cell(200, 10, txt=f"Student ID: {student_id}", ln=True)
        pdf.cell(200, 10, txt=f"Roll Number: {roll}", ln=True)
        pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
        pdf.cell(200, 10, txt=f"Department: {department}", ln=True)

        # Add timestamp
        date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
        pdf.cell(200, 10, txt=f"Date & Time: {date_time}", ln=True)

        # Embed QR code image into the PDF
        pdf.image(qr_img_path, x=10, y=100, w=50, h=50)

        # Save the PDF with a unique name based on student ID and current time
        file_name = f"slip/{student_id}_{now.strftime('%Y%m%d%H%M%S')}.pdf"
        pdf.output(file_name)

        # Display a message box after the slip is generated
        messagebox.showinfo("Slip Generated", f"Slip for student {name} has been generated and saved at {file_name}.")

    def face_recog(self):
        start_time = datetime.now()
        recognized_students = set()

        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)
            coord = []

            for (x, y, w, h) in features:
                face_region = gray_image[y:y + h, x:x + w]
                id, predict = clf.predict(face_region)
                confidence = int((100 * (1 - predict / 300)))

                # Connect to the database
                conn = pymysql.connect(host="localhost", user="root", password="W7301@jqir#", database="face_recognizer")
                my_cursor = conn.cursor()

                # Fetch student details from the database, including email
                my_cursor.execute("SELECT Name, Roll, Dep, Student_id, Email FROM student WHERE Student_id = %s", (id,))
                student_data = my_cursor.fetchone()

                if student_data:
                    name, roll, department, student_id, email = student_data
                else:
                    name = roll = department = student_id = email = "Unknown"

                if confidence > 77:
                    cv2.putText(img, f"ID:{student_id}", (x, y - 75), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 3)
                    cv2.putText(img, f"Roll:{roll}", (x, y - 55), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 3)
                    cv2.putText(img, f"Name:{name}", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 3)
                    cv2.putText(img, f"Department:{department}", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 3)

                    self.mark_attendance(student_id, roll, name, department, email)
                    recognized_students.add(student_id)
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 3)

                coord = [x, y, w, h]

            return coord

        def recognize(img, clf, faceCascade):
            coord = draw_boundary(img, faceCascade, 1.1, 10, (255, 25, 255), "Face", clf)
            return img

        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        cam = cv2.VideoCapture(0)
        while True:
            ret, img = cam.read()
            img = recognize(img, clf, faceCascade)
            cv2.imshow("Face Recognition", img)

            if (datetime.now() - start_time).seconds > 60:  # Stop after 60 seconds
                break

        cam.release()
        cv2.destroyAllWindows()

        # Mark absent students
        self.mark_absentees(recognized_students)

    def mark_absentees(self, recognized_students):
        conn = pymysql.connect(host="localhost", user="root", password="W7301@jqir#", database="face_recognizer")
        my_cursor = conn.cursor()

        my_cursor.execute("SELECT Student_id, Name, Roll, Dep, Email FROM student")
        students = my_cursor.fetchall()

        absentees = []

        for student in students:
            student_id, name, roll, department, email = student
            if student_id not in recognized_students:
                absentees.append((student_id, name, roll, department, email))

        with open("attendance.csv", "r+", newline="\n") as f:
            myDataList = f.readlines()
            name_list = [line.split(",")[0] for line in myDataList]

            for student in absentees:
                student_id, name, roll, department, email = student
                if student_id not in name_list:
                    now = datetime.now()
                    date_str = now.strftime("%d/%m/%Y")
                    time_str = now.strftime("%H:%M:%S")
                    f.writelines(f"\n{student_id},{roll},{name},{department},Absent,{email},{time_str},{date_str}")

        self.send_emails(absentees)

    def send_emails(self, absentees):
        """Send email notifications to absent students."""
        for student in absentees:
            student_id, name, roll, department, email = student
            subject = "Attendance Alert"
            body = (f"Dear {name},\n\n"
                    f"This is to inform you that you were absent during the attendance period.\n\n"
                    f"Regards,\nKALASALINGAM UNIVERSITY")

            # Prepare email message
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = email
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))

            try:
                # Establish SMTP connection
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()  # Upgrade to a secure connection
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, email, message.as_string())
                    print(f"Email sent to {email}")
            except smtplib.SMTPException as e:
                print(f"Failed to send email to {email}: {e}")

if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()
