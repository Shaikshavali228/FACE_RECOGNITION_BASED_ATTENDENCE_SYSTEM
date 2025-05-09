# Face Recognition-Based Attendance System

## Modules Overview

### Module 1: Login Page
- **Functionality**: The login page enables users to authenticate using their email ID as the username and password.
- **New User Registration**: Provides functionality for new users to create an account.
- **Forgot Password**: Allows users to reset their password by answering security questions they set during registration.

### Module 2: Face Recognition-Based Attendance System
This module enables the attendance system through face recognition. The main page includes 8 functionalities as outlined below.

#### 1. **Student Details**
- **Input and Store**: Students' information such as name, ID, course, year, register number, email ID, and contact details are stored.
- **Edit and Update**: Existing student records can be edited, updated, or deleted.
- **Display**: Student details are shown in a table format.

#### 2. **Face Recognition**
- **Real-Time Image Capture**: The system captures real-time images using a webcam.
- **Preprocessing**: Images are preprocessed using grayscale conversion and resizing.
- **Face Detection**: Various algorithms like Haar Cascade and DNN are used for face detection.
- **Recognition and Matching**: The system recognizes faces and matches them with stored images, displaying details such as Student ID, name, Roll No, and Department.
- **Absence Notification**: If the face is not recognized, an email is sent to the parents of the student.

#### 3. **Attendance**
- **Recording Attendance**: Attendance is marked using recognized faces along with current timestamps.
- **Database Storage**: All attendance records are saved in a database.
- **Attendance Reports**: Attendance records can be displayed in a tabular format and exported to Excel.

#### 4. **Help Desk**
- **User Support**: The help desk feature enables users to send queries and get support via email for any clarifications or assistance.

#### 5. **Train the Data**
- **Model Training**: The system trains the face recognition model using stored photos.
- **Data Update**: New student data is incorporated to improve the model.
- **Model Saving**: Trained models are saved for future use, and a confirmation message appears when training is completed.

#### 6. **Photos**
- **Capture and Store Photos**: Student photos are captured and stored for face recognition.
- **Manual Upload**: Students' photos can be manually uploaded.
- **Preprocessing**: Photos are preprocessed for optimal face recognition.

#### 7. **Developer**
- **Developer Info**: Displays details about the developers of the system, including contact information.
- **Credits**: Includes credits for libraries and tools used in the project.

#### 8. **Exit**
- **Secure Exit**: The system prompts for confirmation before exiting, ensuring all data is saved and no information is lost.


### Benefits for Universities:
- **Accuracy**: The Face Recognition-Based Attendance System eliminates the errors associated with manual attendance methods by automating the process.
- **Efficiency**: The system ensures more reliable and efficient attendance management, replacing outdated manual methods.
- **Robust Performance**: The algorithm is capable of detecting multiple faces simultaneously, ensuring stable performance.
- **Help Desk**: Provides support and assistance to users encountering issues with the system.

### Additional Features:
- **Attendance in Excel**: Generates and maintains attendance records in Excel format for easy access and management.
- **Login Page**: Ensures secure access to the system by verifying user identity before granting access.
- **Automatic Slip Generation**: When a student is recognized, a slip is generated, and absentees are marked absent and notified via email.

---

## Technologies Used
- **Face Recognition**: LBPH Algorithm, Haar Cascade Classifier

- **Database**: SQL (for storing student details and attendance records)
