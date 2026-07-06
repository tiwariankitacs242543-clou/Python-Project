print("Ankita Tiwari F127 Python Project")

import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# ==================== Database Setup ====================
def init_db():
    conn = sqlite3.connect("student_management.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cursor.execute("SELECT * FROM users WHERE username = 'ankita'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (username, password) VALUES ('ankita', 'ankita123')")

    

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        roll_no TEXT PRIMARY KEY,
        name TEXT,
        class TEXT,
        section TEXT,
        contact TEXT,
        gender TEXT,
        dob TEXT
    )
    """)

    conn.commit()
    conn.close()

# ==================== Student Management ====================
def open_student_management():
    login_window.destroy()

    root = tk.Tk()
    root.title("Student Database Management System")
    root.geometry("1220x700")
    root.configure(bg="white")

    title = tk.Label(root, text="Student Database Management System", font=("Arial", 20, "bold"), bg="lightblue", fg="black", pady=10)
    title.pack(fill=tk.X)

    input_frame = tk.LabelFrame(root, text="Student Details", font=("Helvetica", 14, "bold"), bg="#e1e5ea", padx=15, pady=15)
    input_frame.place(x=20, y=80, width=400, height=580)

    # Entry Fields
    tk.Label(input_frame, text="Roll No:", font=("Arial", 12, "bold"), bg="#e1e5ea").grid(row=0, column=0, pady=5, sticky="w")
    rollno_ent = tk.Entry(input_frame, font=("Arial", 12))
    rollno_ent.grid(row=0, column=1, pady=5)

    tk.Label(input_frame, text="Name:", font=("Arial", 12, "bold"), bg="#e1e5ea").grid(row=1, column=0, pady=5, sticky="w")
    name_ent = tk.Entry(input_frame, font=("Arial", 12))
    name_ent.grid(row=1, column=1, pady=5)

    tk.Label(input_frame, text="Class:", font=("Arial", 12, "bold"), bg="#e1e5ea").grid(row=2, column=0, pady=5, sticky="w")
    class_ent = tk.Entry(input_frame, font=("Arial", 12))
    class_ent.grid(row=2, column=1, pady=5)

    tk.Label(input_frame, text="Section:", font=("Arial", 12, "bold"), bg="#e1e5ea").grid(row=3, column=0, pady=5, sticky="w")
    section_ent = tk.Entry(input_frame, font=("Arial", 12))
    section_ent.grid(row=3, column=1, pady=5)

    tk.Label(input_frame, text="Contact:", font=("Arial", 12, "bold"), bg="#e1e5ea").grid(row=4, column=0, pady=5, sticky="w")
    contact_ent = tk.Entry(input_frame, font=("Arial", 12))
    contact_ent.grid(row=4, column=1, pady=5)

    tk.Label(input_frame, text="Gender:", font=("Arial", 12, "bold"), bg="#e1e5ea").grid(row=5, column=0, pady=5, sticky="w")
    gender_ent = ttk.Combobox(input_frame, values=["Male", "Female", "Other"], font=("Arial", 12), state="readonly")
    gender_ent.grid(row=5, column=1, pady=5)

    tk.Label(input_frame, text="D.O.B:", font=("Arial", 12, "bold"), bg="#e1e5ea").grid(row=6, column=0, pady=5, sticky="w")
    dob_ent = tk.Entry(input_frame, font=("Arial", 12))
    dob_ent.grid(row=6, column=1, pady=5)

    def fetch_data():
        conn = sqlite3.connect("student_management.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        conn.close()

        tree.delete(*tree.get_children())
        for row in rows:
            tree.insert("", tk.END, values=row)

    def add_student():
        conn = sqlite3.connect("student_management.db")
        cursor = conn.cursor()

        if not rollno_ent.get() or not name_ent.get():
            messagebox.showerror("Error", "Roll No and Name are required!")
            return

        try:
            cursor.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?)", (
                rollno_ent.get(), name_ent.get(), class_ent.get(), section_ent.get(),
                contact_ent.get(), gender_ent.get(), dob_ent.get()
            ))
            conn.commit()
            fetch_data()
            messagebox.showinfo("Success", "Student added successfully!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Roll No must be unique!")
        finally:
            conn.close()

    def delete_student():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a student to delete.")
            return

        roll_no = tree.item(selected_item, "values")[0]

        conn = sqlite3.connect("student_management.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE roll_no=?", (roll_no,))
        conn.commit()
        conn.close()
        fetch_data()
        messagebox.showinfo("Success", "Student deleted successfully!")

    def update_student():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a student to update.")
            return

        roll_no = tree.item(selected_item, "values")[0]

        conn = sqlite3.connect("student_management.db")
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE students SET name=?, class=?, section=?, contact=?, gender=?, dob=? WHERE roll_no=?
        """, (
            name_ent.get(), class_ent.get(), section_ent.get(),
            contact_ent.get(), gender_ent.get(), dob_ent.get(), roll_no
        ))
        conn.commit()
        conn.close()
        fetch_data()
        clear_fields()
        messagebox.showinfo("Success", "Student updated successfully!")

    def clear_fields():
        rollno_ent.delete(0, tk.END)
        name_ent.delete(0, tk.END)
        class_ent.delete(0, tk.END)
        section_ent.delete(0, tk.END)
        contact_ent.delete(0, tk.END)
        gender_ent.set("")
        dob_ent.delete(0, tk.END)

    # Buttons
    tk.Button(input_frame, text="Add", command=add_student, font=("Arial", 12, "bold"), bg="#4682B4", fg="white").grid(row=7, column=0, columnspan=2, pady=10, ipadx=40)
    tk.Button(input_frame, text="Delete", command=delete_student, font=("Arial", 12, "bold"), bg="#4682B4", fg="white").grid(row=8, column=0, columnspan=2, pady=10, ipadx=40)
    tk.Button(input_frame, text="Update", command=update_student, font=("Arial", 12, "bold"), bg="#4682B4", fg="white").grid(row=9, column=0, columnspan=2, pady=10, ipadx=40)
    tk.Button(input_frame, text="Clear", command=clear_fields, font=("Arial", 12, "bold"), bg="#4682B4", fg="white").grid(row=10, column=0, columnspan=2, pady=10, ipadx=40)

    # Right Frame - Data Table
    table_frame = tk.Frame(root, bg="white", bd=2, relief=tk.GROOVE)
    table_frame.place(x=440, y=100, width=740, height=550)

    columns = ("Roll No", "Name", "Class", "Section", "Contact", "Gender", "D.O.B")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=25)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    tree.pack(fill="both", expand=True)

    def on_row_select(event):
        selected_item = tree.selection()
        if not selected_item:
            return
        values = tree.item(selected_item, 'values')
        rollno_ent.delete(0, tk.END)
        rollno_ent.insert(0, values[0])
        name_ent.delete(0, tk.END)
        name_ent.insert(0, values[1])
        class_ent.delete(0, tk.END)
        class_ent.insert(0, values[2])
        section_ent.delete(0, tk.END)
        section_ent.insert(0, values[3])
        contact_ent.delete(0, tk.END)
        contact_ent.insert(0, values[4])
        gender_ent.set(values[5])
        dob_ent.delete(0, tk.END)
        dob_ent.insert(0, values[6])

    tree.bind("<ButtonRelease-1>", on_row_select)
    fetch_data()
    root.mainloop()

# ==================== Login ====================
def login():
    username = entry_username.get()
    password = entry_password.get()

    conn = sqlite3.connect("student_management.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        open_student_management()
    else:
        messagebox.showerror("Error", "Invalid Username or Password")

# ==================== Dashboard ====================
def open_login():
    dashboard.destroy()

    global login_window
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("400x300")
    login_window.configure(bg="#f0f0f0")

    frame = tk.Frame(login_window, bg="white", padx=20, pady=20)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    login_title = tk.Label(frame, text="Login", font=("Arial", 18, "bold"), bg="white")
    login_title.grid(row=0, column=0, columnspan=2, pady=(0, 10))

    tk.Label(frame, text="Username", font=("Arial", 12), bg="white").grid(row=1, column=0, sticky="w")
    global entry_username
    entry_username = tk.Entry(frame, font=("Arial", 12))
    entry_username.grid(row=1, column=1, pady=5)

    tk.Label(frame, text="Password", font=("Arial", 12), bg="white").grid(row=2, column=0, sticky="w")
    global entry_password
    entry_password = tk.Entry(frame, show="*", font=("Arial", 12))
    entry_password.grid(row=2, column=1, pady=5)

    login_btn = tk.Button(frame, text="Login", command=login, font=("Arial", 12, "bold"), bg="#4682B4", fg="white", padx=10)
    login_btn.grid(row=3, column=0, columnspan=2, pady=10)

    login_window.mainloop()

def show_credits():
    messagebox.showinfo("Credits", "Developed by Ankita Tiwari\nF127\nPython Project")

def exit_app():
    dashboard.destroy()

# ==================== Launch Dashboard ====================
init_db()
dashboard = tk.Tk()
dashboard.title("Welcome")
dashboard.geometry("800x400")
dashboard.configure(bg="#e6f2ff")

tk.Label(dashboard, text="Welcome to Student Database Management System", font=("Arial", 22, "bold"), bg="#e6f2ff", fg="#333").pack(pady=40)

tk.Button(dashboard, text="Login", command=open_login, font=("Arial", 14), bg="#4682B4", fg="white", width=15).pack(pady=10)
tk.Button(dashboard, text="Exit", command=exit_app, font=("Arial", 14), bg="red", fg="white", width=15).pack(pady=10)

dashboard.mainloop()
