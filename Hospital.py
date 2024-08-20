import tkinter as tk
from tkinter import messagebox, ttk, Frame, Label, Entry, Button
from PIL import Image, ImageTk
import os
import sqlite3

from app import SimpleHospitalBackend
 
 
def switch_to_dashboard():
    root.destroy()
    main()
 
def switch_to_signup():
    login_frame.place_forget()
    create_signup_frame()
 
def switch_to_login():
    signup_frame.place_forget()
    create_login_frame()
 
def on_enter(e, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, 'end')
        if 'Password' in placeholder:
            entry.config(show='*')
 
def on_leave(e, entry, placeholder):
    if entry.get() == '':
        entry.insert(0, placeholder)
        if 'Password' in placeholder:
            entry.config(show='')
 
def create_login_frame():
    global login_frame
    login_frame = Frame(frame1, width=350, height=400, bg='white')
    login_frame.place(x=425, y=60)
 
    heading = Label(login_frame, text='Login', fg='black', bg='white', font=('Arial', 20, 'bold'))
    heading.place(x=140, y=20)
 
    username = Entry(login_frame, width=37, fg='black', border=0, font=('Arial', 11))
    username.place(x=20, y=80)
    username.insert(0, 'Username')
    username.bind('<FocusIn>', lambda e: on_enter(e, username, 'Username'))
    username.bind('<FocusOut>', lambda e: on_leave(e, username, 'Username'))
    Frame(login_frame, width=300, height=2, bg='black').place(x=20, y=105)
 
    password = Entry(login_frame, width=37, fg='black', border=0, font=('Arial', 11))
    password.place(x=20, y=130)
    password.insert(0, 'Password')
    password.bind('<FocusIn>', lambda e: on_enter(e, password, 'Password'))
    password.bind('<FocusOut>', lambda e: on_leave(e, password, 'Password'))
    Frame(login_frame, width=300, height=2, bg='black').place(x=20, y=155)
 
    login_button = Button(login_frame, width=8, text='LOGIN', fg='white', bg='blue', border=0, font=('Arial', 10, 'bold'), command=switch_to_dashboard)
    login_button.place(x=135, y=200)
 
    signup_label = Label(login_frame, text="Don't have an account?", bg='white', fg='black', font=('Arial', 10))
    signup_label.place(x=75, y=250)
    signup_button = Button(login_frame, width=6, text='Sign Up', border=0, bg='white', fg='turquoise', font=('Arial', 10), command=switch_to_signup)
    signup_button.place(x=218, y=249)
 
def create_signup_frame():
    global signup_frame
    signup_frame = Frame(frame1, width=350, height=400, bg='white')
    signup_frame.place(x=425, y=60)
 
    heading = Label(signup_frame, text='Sign up', fg='black', bg='white', font=('Arial', 20, 'bold'))
    heading.place(x=120, y=20)
 
    mail = Entry(signup_frame, width=37, fg='black', border=0, font=('Arial', 11))
    mail.place(x=20, y=80)
    mail.insert(0, 'Email')
    mail.bind('<FocusIn>', lambda e: on_enter(e, mail, 'Email'))
    mail.bind('<FocusOut>', lambda e: on_leave(e, mail, 'Email'))
    Frame(signup_frame, width=300, height=2, bg='black').place(x=20, y=105)
 
    user = Entry(signup_frame, width=37, fg='black', border=0, font=('Arial', 11))
    user.place(x=20, y=130)
    user.insert(0, 'Create Username')
    user.bind('<FocusIn>', lambda e: on_enter(e, user, 'Create Username'))
    user.bind('<FocusOut>', lambda e: on_leave(e, user, 'Create Username'))
    Frame(signup_frame, width=300, height=2, bg='black').place(x=20, y=155)
 
    password = Entry(signup_frame, width=37, fg='black', border=0, font=('Arial', 11))
    password.place(x=20, y=180)
    password.insert(0, 'Create Password')
    password.bind('<FocusIn>', lambda e: on_enter(e, password, 'Create Password'))
    password.bind('<FocusOut>', lambda e: on_leave(e, password, 'Create Password'))
    Frame(signup_frame, width=300, height=2, bg='black').place(x=20, y=205)
 
    confirm_password = Entry(signup_frame, width=37, fg='black', border=0, font=('Arial', 11))
    confirm_password.place(x=20, y=230)
    confirm_password.insert(0, 'Confirm Password')
    confirm_password.bind('<FocusIn>', lambda e: on_enter(e, confirm_password, 'Confirm Password'))
    confirm_password.bind('<FocusOut>', lambda e: on_leave(e, confirm_password, 'Confirm Password'))
    Frame(signup_frame, width=300, height=2, bg='black').place(x=20, y=255)
 
    signup_button = Button(signup_frame, width=8, text='SIGN UP', fg='white', bg='blue', border=0, font=('Arial', 10, 'bold'), command=switch_to_dashboard)
    signup_button.place(x=135, y=275)
 
    account = Label(signup_frame, text="I already have an account.", bg='white', fg='black', font=('Arial', 10))
    account.place(x=65, y=330)
    login_button = Button(signup_frame, width=6, text='Login', border=0, bg='white', fg='turquoise', font=('Arial', 10), command=switch_to_login)
    login_button.place(x=218, y=329)
 
def init_db():
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS patients''')
    c.execute('''CREATE TABLE IF NOT EXISTS patients (
                patient_id TEXT PRIMARY KEY,
                name TEXT,
                medical_history TEXT)''')
    conn.commit()
    conn.close()
 
def save_patient_to_db(patient_id, name, medical_history):
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO patients (patient_id, name, medical_history) VALUES (?, ?, ?)",
                  (patient_id, name, medical_history))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Patient with ID {patient_id} already exists in the database.")
    conn.close()
 
def load_patients_from_db():
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    c.execute("SELECT patient_id, name, medical_history FROM patients")
    patients = {row[0]: {'name': row[1], 'medical_history': row[2]} for row in c.fetchall()}
    conn.close()
    return patients
 
def save_patient(patient_id, name, medical_history):
    save_patient_to_db(patient_id, name, medical_history)
    print("Patient data saved to the database.")
 
def load_all_patients():
    db_patients = load_patients_from_db()
    print("Patients from SQLite:", db_patients)
 
def register_patient(patient_id, name, medical_history):
    patients = load_patients_from_db()
    if patient_id in patients:
        print("Patient ID already exists.")
    else:
        save_patient(patient_id, name, medical_history)
        print("Patient registered successfully.")
 
def view_patient(patient_id):
    patients = load_patients_from_db()
    if patient_id in patients:
        patient = patients[patient_id]
        print(f"Patient ID: {patient_id}\nName: {patient['name']}\nMedical History: {patient['medical_history']}")
    else:
        print("Patient not found.")
init_db()
 
 
def main():
    root = tk.Tk()
    root.title("Meditech Hospital")
    root.geometry("825x550")
 
    # Set the window icon
    root.iconbitmap('abc.ico')
 
    title_frame = ttk.Frame(root)
    title_frame.pack(fill=tk.X, padx=10, pady=10)
   
    title_label = ttk.Label(title_frame, text="Meditech Hospital", font=("Helvetica", 24, "bold"))
    title_label.pack()
   
    subtitle_label = ttk.Label(title_frame, text="Appointment Booking System", font=("Helvetica", 14))
    subtitle_label.pack()
 
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
 
    patient_tree = create_patient_tab(notebook) # type: ignore
    doctor_tree = create_doctor_tab(notebook) # type: ignore
    appointment_tree = create_appointment_tab(notebook) # type: ignore
 
root = tk.Tk()
root.title('Meditech Hospital')
root.geometry('825x500')
root.configure(bg='#fff')
root.resizable(False, False)
 
frame1 = Frame(root, width=825, height=500)
frame1.place(x=0, y=0)
 
image = Image.open('hosp.jpg')
photo = ImageTk.PhotoImage(image)
my_label = Label(frame1, image=photo, bg='white')
my_label.place(y=0)
 
root.iconbitmap('abc.ico')
 
import tkinter as tk
from tkinter import ttk, messagebox
 
def create_patient_tab(notebook):
    patient_frame = ttk.Frame(notebook)
    notebook.add(patient_frame, text="Patient Information")
 
    # Patient Information
    ttk.Label(patient_frame, text="Patient ID:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    patient_id_entry = ttk.Entry(patient_frame)
    patient_id_entry.grid(row=0, column=1, padx=5, pady=5)
 
    ttk.Label(patient_frame, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
    patient_name_entry = ttk.Entry(patient_frame)
    patient_name_entry.grid(row=1, column=1, padx=5, pady=5)
 
    ttk.Label(patient_frame, text="Age:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
    patient_age_entry = ttk.Entry(patient_frame)
    patient_age_entry.grid(row=2, column=1, padx=5, pady=5)
 
    ttk.Label(patient_frame, text="Gender:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
    patient_gender_combo = ttk.Combobox(patient_frame, values=["Male", "Female", "Other"])
    patient_gender_combo.grid(row=3, column=1, padx=5, pady=5)
 
    ttk.Label(patient_frame, text="Address:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
    patient_address_entry = ttk.Entry(patient_frame)
    patient_address_entry.grid(row=4, column=1, padx=5, pady=5)
 
    ttk.Label(patient_frame, text="Contact Number:").grid(row=5, column=0, padx=5, pady=5, sticky='e')
    patient_contact_entry = ttk.Entry(patient_frame)
    patient_contact_entry.grid(row=5, column=1, padx=5, pady=5)
 
    ttk.Button(patient_frame, text="Add Patient", command=lambda: add_patient(patient_id_entry, patient_name_entry, patient_age_entry, patient_gender_combo, patient_address_entry, patient_contact_entry, patient_listbox)).grid(row=6, column=0, columnspan=2, pady=10)
 
    # Patient List
    patient_listbox = tk.Listbox(patient_frame, width=80, height=10)
    patient_listbox.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')
 
    # Add scrollbar to the listbox
    scrollbar = tk.Scrollbar(patient_frame, orient=tk.VERTICAL, command=patient_listbox.yview)
    scrollbar.grid(row=7, column=2, sticky='ns')
    patient_listbox.config(yscrollcommand=scrollbar.set)
 
    # Configure the grid to expand properly
    patient_frame.columnconfigure(1, weight=1)
    patient_frame.rowconfigure(7, weight=1)
 
    return patient_listbox
 
def create_doctor_tab(notebook):
    doctor_frame = ttk.Frame(notebook)
    notebook.add(doctor_frame, text="Doctor Information")
 
    # Doctor Information
    ttk.Label(doctor_frame, text="Doctor ID:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    doctor_id_entry = ttk.Entry(doctor_frame)
    doctor_id_entry.grid(row=0, column=1, padx=5, pady=5)
 
    ttk.Label(doctor_frame, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
    doctor_name_entry = ttk.Entry(doctor_frame)
    doctor_name_entry.grid(row=1, column=1, padx=5, pady=5)
 
    ttk.Label(doctor_frame, text="Specialization:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
    doctor_specialization_entry = ttk.Entry(doctor_frame)
    doctor_specialization_entry.grid(row=2, column=1, padx=5, pady=5)
 
    ttk.Button(doctor_frame, text="Add Doctor", command=lambda: add_doctor(doctor_id_entry, doctor_name_entry, doctor_specialization_entry, doctor_listbox)).grid(row=3, column=0, columnspan=2, pady=10)
 
    # Doctor List
    doctor_listbox = tk.Listbox(doctor_frame, width=80, height=10)
    doctor_listbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')
 
    # Add scrollbar to the listbox
    scrollbar = tk.Scrollbar(doctor_frame, orient=tk.VERTICAL, command=doctor_listbox.yview)
    scrollbar.grid(row=4, column=2, sticky='ns')
    doctor_listbox.config(yscrollcommand=scrollbar.set)
 
    # Configure the grid to expand properly
    doctor_frame.columnconfigure(1, weight=1)
    doctor_frame.rowconfigure(4, weight=1)
 
    return doctor_listbox
 
def create_appointment_tab(notebook):
    appointment_frame = ttk.Frame(notebook)
    notebook.add(appointment_frame, text="Appointment System")
 
    # Appointment Information
    ttk.Label(appointment_frame, text="Patient ID:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    appointment_patient_id_entry = ttk.Entry(appointment_frame)
    appointment_patient_id_entry.grid(row=0, column=1, padx=5, pady=5)
 
    ttk.Label(appointment_frame, text="Doctor ID:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
    appointment_doctor_id_entry = ttk.Entry(appointment_frame)
    appointment_doctor_id_entry.grid(row=1, column=1, padx=5, pady=5)
 
    ttk.Label(appointment_frame, text="Date:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
    appointment_date_entry = ttk.Entry(appointment_frame)
    appointment_date_entry.grid(row=2, column=1, padx=5, pady=5)
 
    ttk.Label(appointment_frame, text="Time:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
    appointment_time_entry = ttk.Entry(appointment_frame)
    appointment_time_entry.grid(row=3, column=1, padx=5, pady=5)
 
    ttk.Button(appointment_frame, text="Schedule Appointment", command=lambda: schedule_appointment(appointment_patient_id_entry, appointment_doctor_id_entry, appointment_date_entry, appointment_time_entry, appointment_listbox)).grid(row=4, column=0, columnspan=2, pady=10)
 
    # Appointment List
    appointment_listbox = tk.Listbox(appointment_frame, width=80, height=10)
    appointment_listbox.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')
 
    # Add scrollbar to the listbox
    scrollbar = tk.Scrollbar(appointment_frame, orient=tk.VERTICAL, command=appointment_listbox.yview)
    scrollbar.grid(row=5, column=2, sticky='ns')
    appointment_listbox.config(yscrollcommand=scrollbar.set)
 
    # Configure the grid to expand properly
    appointment_frame.columnconfigure(1, weight=1)
    appointment_frame.rowconfigure(5, weight=1)
 
    return appointment_listbox
 
def add_patient(patient_id_entry, patient_name_entry, patient_age_entry, patient_gender_combo, patient_address_entry, patient_contact_entry, patient_listbox):
    patient_id = patient_id_entry.get()
    name = patient_name_entry.get()
    age = patient_age_entry.get()
    gender = patient_gender_combo.get()
    address = patient_address_entry.get()
    contact = patient_contact_entry.get()
 
    if patient_id and name and age and gender and address and contact:
        patient_listbox.insert(tk.END, f"{patient_id} | {name} | {age} | {gender} | {address} | {contact}")
        messagebox.showinfo("Add Patient", "Patient added successfully!")
        clear_entries([patient_id_entry, patient_name_entry, patient_age_entry, patient_address_entry, patient_contact_entry]) # type: ignore
        patient_gender_combo.set("")
    else:
        messagebox.showwarning("Input Error", "Please fill all fields.")
 
def add_doctor(doctor_id_entry, doctor_name_entry, doctor_specialization_entry, doctor_listbox):
    doctor_id = doctor_id_entry.get()
    name = doctor_name_entry.get()
    specialization = doctor_specialization_entry.get()
 
    if doctor_id and name and specialization:
        doctor_listbox.insert(tk.END, f"{doctor_id} | {name} | {specialization}")
        messagebox.showinfo("Add Doctor", "Doctor added successfully!")
        clear_entries([doctor_id_entry, doctor_name_entry, doctor_specialization_entry]) # type: ignore
    else:
        messagebox.showwarning("Input Error", "Please fill all fields.")
 
def schedule_appointment(appointment_patient_id_entry, appointment_doctor_id_entry, appointment_date_entry, appointment_time_entry, appointment_listbox):
    patient_id = appointment_patient_id_entry.get()
    doctor_id = appointment_doctor # type: ignore
 
 
 
 
create_login_frame()
 
root.mainloop()
import tkinter as tk
from tkinter import messagebox, ttk, Frame, Label, Entry, Button
from PIL import Image, ImageTk
import os
 
# Define the function to switch to the main dashboard
def switch_to_dashboard():
    root.destroy()
    main()
 
def switch_to_signup():
    login_frame.place_forget()
    create_signup_frame()
 
def switch_to_login():
    signup_frame.place_forget()
    create_login_frame()
 
def on_enter(e, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, 'end')
        if 'Password' in placeholder:
            entry.config(show='*')
 
def on_leave(e, entry, placeholder):
    if entry.get() == '':
        entry.insert(0, placeholder)
        if 'Password' in placeholder:
            entry.config(show='')
 
def create_login_frame():
    global login_frame
    login_frame = Frame(frame1, width=350, height=400, bg='white')
    login_frame.place(x=425, y=60)
 
    heading = Label(login_frame, text='Login', fg='black', bg='white', font=('Arial', 20, 'bold'))
    heading.place(x=140, y=20)
 
    username = Entry(login_frame, width=37, fg='black', border=0, font=('Arial', 11))
    username.place(x=20, y=80)
    username.insert(0, 'Username')
    username.bind('<FocusIn>', lambda e: on_enter(e, username, 'Username'))
    username.bind('<FocusOut>', lambda e: on_leave(e, username, 'Username'))
    Frame(login_frame, width=300, height=2, bg='black').place(x=20, y=105)
 
    password = Entry(login_frame, width=37, fg='black', border=0, font=('Arial', 11))
    password.place(x=20, y=130)
    password.insert(0, 'Password')
    password.bind('<FocusIn>', lambda e: on_enter(e, password, 'Password'))
    password.bind('<FocusOut>', lambda e: on_leave(e, password, 'Password'))
    Frame(login_frame, width=300, height=2, bg='black').place(x=20, y=155)
 
    login_button = Button(login_frame, width=8, text='LOGIN', fg='white', bg='blue', border=0, font=('Arial', 10, 'bold'), command=switch_to_dashboard)
    login_button.place(x=135, y=200)
 
    signup_label = Label(login_frame, text="Don't have an account?", bg='white', fg='black', font=('Arial', 10))
    signup_label.place(x=75, y=250)
    signup_button = Button(login_frame, width=6, text='Sign Up', border=0, bg='white', fg='turquoise', font=('Arial', 10), command=switch_to_signup)
    signup_button.place(x=218, y=249)
 
def create_signup_frame():
    global signup_frame
    signup_frame = Frame(frame1, width=350, height=400, bg='white')
    signup_frame.place(x=425, y=60)
 
    heading = Label(signup_frame, text='Sign up', fg='black', bg='white', font=('Arial', 20, 'bold'))
    heading.place(x=120, y=20)
 
    mail = Entry(signup_frame, width=37, fg='black', border=0, font=('Arial', 11))
    mail.place(x=20, y=80)
    mail.insert(0, 'Email')
    mail.bind('<FocusIn>', lambda e: on_enter(e, mail, 'Email'))
    mail.bind('<FocusOut>', lambda e: on_leave(e, mail, 'Email'))
    Frame(signup_frame, width=300, height=2, bg='black').place(x=20, y=105)
 
    user = Entry(signup_frame, width=37, fg='black', border=0, font=('Arial', 11))
    user.place(x=20, y=130)
    user.insert(0, 'Create Username')
    user.bind('<FocusIn>', lambda e: on_enter(e, user, 'Create Username'))
    user.bind('<FocusOut>', lambda e: on_leave(e, user, 'Create Username'))
    Frame(signup_frame, width=300, height=2, bg='black').place(x=20, y=155)
 
    password = Entry(signup_frame, width=37, fg='black', border=0, font=('Arial', 11))
    password.place(x=20, y=180)
    password.insert(0, 'Create Password')
    password.bind('<FocusIn>', lambda e: on_enter(e, password, 'Create Password'))
    password.bind('<FocusOut>', lambda e: on_leave(e, password, 'Create Password'))
    Frame(signup_frame, width=300, height=2, bg='black').place(x=20, y=205)
 
    confirm_password = Entry(signup_frame, width=37, fg='black', border=0, font=('Arial', 11))
    confirm_password.place(x=20, y=230)
    confirm_password.insert(0, 'Confirm Password')
    confirm_password.bind('<FocusIn>', lambda e: on_enter(e, confirm_password, 'Confirm Password'))
    confirm_password.bind('<FocusOut>', lambda e: on_leave(e, confirm_password, 'Confirm Password'))
    Frame(signup_frame, width=300, height=2, bg='black').place(x=20, y=255)
 
    signup_button = Button(signup_frame, width=8, text='SIGN UP', fg='white', bg='blue', border=0, font=('Arial', 10, 'bold'), command=switch_to_dashboard)
    signup_button.place(x=135, y=275)
 
    account = Label(signup_frame, text="I already have an account.", bg='white', fg='black', font=('Arial', 10))
    account.place(x=65, y=330)
    login_button = Button(signup_frame, width=6, text='Login', border=0, bg='white', fg='turquoise', font=('Arial', 10), command=switch_to_login)
    login_button.place(x=218, y=329)
 
def main():
    root = tk.Tk()
    root.title("Meditech Hospital")
    root.geometry("825x550")
 
    # Set the window icon
    root.iconbitmap('abc.ico')
 
    title_frame = ttk.Frame(root)
    title_frame.pack(fill=tk.X, padx=10, pady=10)
   
    title_label = ttk.Label(title_frame, text="Meditech Hospital", font=("Helvetica", 24, "bold"))
    title_label.pack()
   
    subtitle_label = ttk.Label(title_frame, text="Appointment Booking System", font=("Helvetica", 14))
    subtitle_label.pack()
 
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
 
    patient_tree = create_patient_tab(notebook) # type: ignore
    doctor_tree = create_doctor_tab(notebook) # type: ignore
    appointment_tree = create_appointment_tab(notebook) # type: ignore
 
root = tk.Tk()
root.title('Meditech Hospital')
root.geometry('825x500')
root.configure(bg='#fff')
root.resizable(False, False)
 
frame1 = Frame(root, width=825, height=500)
frame1.place(x=0, y=0)
 
image = Image.open('hosp.jpg')
photo = ImageTk.PhotoImage(image)
my_label = Label(frame1, image=photo, bg='white')
my_label.place(y=0)
 
root.iconbitmap('abc.ico')
 
import tkinter as tk
from tkinter import ttk, messagebox
 
def create_patient_tab(notebook):
    patient_frame = ttk.Frame(notebook)
    notebook.add(patient_frame, text="Patient Information")
 
    ttk.Label(patient_frame, text="Patient ID:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    patient_id_entry = ttk.Entry(patient_frame)
    patient_id_entry.grid(row=0, column=1, padx=5, pady=5)
 
    ttk.Label(patient_frame, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
    patient_name_entry = ttk.Entry(patient_frame)
    patient_name_entry.grid(row=1, column=1, padx=5, pady=5)
 
    ttk.Label(patient_frame, text="Age:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
    patient_age_entry = ttk.Entry(patient_frame)
    patient_age_entry.grid(row=2, column=1, padx=5, pady=5)
 
    ttk.Label(patient_frame, text="Gender:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
    patient_gender_combo = ttk.Combobox(patient_frame, values=["Male", "Female", "Other"])
    patient_gender_combo.grid(row=3, column=1, padx=5, pady=5)
 
    ttk.Label(patient_frame, text="Address:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
    patient_address_entry = ttk.Entry(patient_frame)
    patient_address_entry.grid(row=4, column=1, padx=5, pady=5)
 
    ttk.Label(patient_frame, text="Contact Number:").grid(row=5, column=0, padx=5, pady=5, sticky='e')
    patient_contact_entry = ttk.Entry(patient_frame)
    patient_contact_entry.grid(row=5, column=1, padx=5, pady=5)
 
    ttk.Button(patient_frame, text="Add Patient", command=lambda: add_patient(patient_id_entry, patient_name_entry, patient_age_entry, patient_gender_combo, patient_address_entry, patient_contact_entry, patient_listbox)).grid(row=6, column=0, columnspan=2, pady=10)
 
    patient_listbox = tk.Listbox(patient_frame, width=80, height=10)
    patient_listbox.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')
 
    scrollbar = tk.Scrollbar(patient_frame, orient=tk.VERTICAL, command=patient_listbox.yview)
    scrollbar.grid(row=7, column=2, sticky='ns')
    patient_listbox.config(yscrollcommand=scrollbar.set)
 
    patient_frame.columnconfigure(1, weight=1)
    patient_frame.rowconfigure(7, weight=1)
 
    return patient_listbox
 
def create_doctor_tab(notebook):
    doctor_frame = ttk.Frame(notebook)
    notebook.add(doctor_frame, text="Doctor Information")
 
    ttk.Label(doctor_frame, text="Doctor ID:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    doctor_id_entry = ttk.Entry(doctor_frame)
    doctor_id_entry.grid(row=0, column=1, padx=5, pady=5)
 
    ttk.Label(doctor_frame, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
    doctor_name_entry = ttk.Entry(doctor_frame)
    doctor_name_entry.grid(row=1, column=1, padx=5, pady=5)
 
    ttk.Label(doctor_frame, text="Specialization:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
    doctor_specialization_entry = ttk.Entry(doctor_frame)
    doctor_specialization_entry.grid(row=2, column=1, padx=5, pady=5)
 
    ttk.Button(doctor_frame, text="Add Doctor", command=lambda: add_doctor(doctor_id_entry, doctor_name_entry, doctor_specialization_entry, doctor_listbox)).grid(row=3, column=0, columnspan=2, pady=10)
 
    doctor_listbox = tk.Listbox(doctor_frame, width=80, height=10)
    doctor_listbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')
 
    scrollbar = tk.Scrollbar(doctor_frame, orient=tk.VERTICAL, command=doctor_listbox.yview)
    scrollbar.grid(row=4, column=2, sticky='ns')
    doctor_listbox.config(yscrollcommand=scrollbar.set)
 
    doctor_frame.columnconfigure(1, weight=1)
    doctor_frame.rowconfigure(4, weight=1)
 
    return doctor_listbox
 
def create_appointment_tab(notebook):
    appointment_frame = ttk.Frame(notebook)
    notebook.add(appointment_frame, text="Appointment System")
 
    ttk.Label(appointment_frame, text="Patient ID:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    appointment_patient_id_entry = ttk.Entry(appointment_frame)
    appointment_patient_id_entry.grid(row=0, column=1, padx=5, pady=5)
 
    ttk.Label(appointment_frame, text="Doctor ID:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
    appointment_doctor_id_entry = ttk.Entry(appointment_frame)
    appointment_doctor_id_entry.grid(row=1, column=1, padx=5, pady=5)
 
    ttk.Label(appointment_frame, text="Date:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
    appointment_date_entry = ttk.Entry(appointment_frame)
    appointment_date_entry.grid(row=2, column=1, padx=5, pady=5)
 
    ttk.Label(appointment_frame, text="Time:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
    appointment_time_entry = ttk.Entry(appointment_frame)
    appointment_time_entry.grid(row=3, column=1, padx=5, pady=5)
 
    ttk.Button(appointment_frame, text="Schedule Appointment", command=lambda: schedule_appointment(appointment_patient_id_entry, appointment_doctor_id_entry, appointment_date_entry, appointment_time_entry, appointment_listbox)).grid(row=4, column=0, columnspan=2, pady=10)
 
    appointment_listbox = tk.Listbox(appointment_frame, width=80, height=10)
    appointment_listbox.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')
 
    scrollbar = tk.Scrollbar(appointment_frame, orient=tk.VERTICAL, command=appointment_listbox.yview)
    scrollbar.grid(row=5, column=2, sticky='ns')
    appointment_listbox.config(yscrollcommand=scrollbar.set)
 
    appointment_frame.columnconfigure(1, weight=1)
    appointment_frame.rowconfigure(5, weight=1)
 
    return appointment_listbox
 
def add_patient(patient_id_entry, patient_name_entry, patient_age_entry, patient_gender_combo, patient_address_entry, patient_contact_entry, patient_listbox):
    patient_id = patient_id_entry.get()
    name = patient_name_entry.get()
    age = patient_age_entry.get()
    gender = patient_gender_combo.get()
    address = patient_address_entry.get()
    contact = patient_contact_entry.get()
 
    if patient_id and name and age and gender and address and contact:
        patient_listbox.insert(tk.END, f"{patient_id} | {name} | {age} | {gender} | {address} | {contact}")
        messagebox.showinfo("Add Patient", "Patient added successfully!")
        clear_entries([patient_id_entry, patient_name_entry, patient_age_entry, patient_address_entry, patient_contact_entry]) # type: ignore
        patient_gender_combo.set("")
    else:
        messagebox.showwarning("Input Error", "Please fill all fields.")
 
def add_doctor(doctor_id_entry, doctor_name_entry, doctor_specialization_entry, doctor_listbox):
    doctor_id = doctor_id_entry.get()
    name = doctor_name_entry.get()
    specialization = doctor_specialization_entry.get()
 
    if doctor_id and name and specialization:
        doctor_listbox.insert(tk.END, f"{doctor_id} | {name} | {specialization}")
        messagebox.showinfo("Add Doctor", "Doctor added successfully!")
        clear_entries([doctor_id_entry, doctor_name_entry, doctor_specialization_entry]) # type: ignore
    else:
        messagebox.showwarning("Input Error", "Please fill all fields.")
 
def schedule_appointment(appointment_patient_id_entry, appointment_doctor_id_entry, appointment_date_entry, appointment_time_entry, appointment_listbox):
    patient_id = appointment_patient_id_entry.get()
    doctor_id = appointment_doctor # type: ignore
 
def __init__(self, db_name='hospital.db'):
        try:
            print("Connecting to database...")
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            self._create_tables()
            print("Connected to database successfully.")
        except Exception as e:
            print(f"Failed to connect to the database: {e}")
 
def _create_tables(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT,
                                    age INTEGER,
                                    gender TEXT)''')
 
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS doctors (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT,
                                    specialization TEXT)''')
 
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
                                    patient_id INTEGER,
                                    doctor_id INTEGER,
                                    date TEXT,
                                    PRIMARY KEY (patient_id, doctor_id))''')
 
            self.conn.commit()
            print("Tables created successfully.")
        except Exception as e:
            print(f"Failed to create tables: {e}")
try:
    backend = SimpleHospitalBackend()
except Exception as e:
    print(f"Failed to initialize SimpleHospitalBackend: {e}")
 
 
 
create_login_frame()
 
root.mainloop()