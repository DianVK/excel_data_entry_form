import re
import os
import bcrypt
import pandas as pd
from openpyxl import Workbook
from tkinter import *
from tkinter import messagebox


def check_file():
    # checks if the excel file exists,if not - creates it
    wb = Workbook()
    ws = wb.active
    current_file_dir = os.getcwd()
    database_file_dir = str(current_file_dir) + "\\user_data.xlsx"
    file_exists = os.path.isfile(database_file_dir)
    if not file_exists:
        wb = Workbook()
        ws = wb.active
        ws.append(["username", "password", "salary", "e-mail"])
        wb.save("user_data.xlsx")


def username_validation(name):
    # valid username should contain - between 6 and 30 chars, letters ,numbers, dots ,underscores and dashes
    valid_username = re.compile(r'^(?![-._])(?!.*[_.-]{2})[\w.-]{6,30}(?<![-._])$')
    if valid_username.match(name) is None:
        messagebox.showerror("Error", "Invalid username!\n"
                                      "Username should contain minimum 6 to 30 characters!\n"
                                      "Letters, numbers, dots, underscores and dashes are allowed!")
        return False
    return True


def password_validation(password):
    # valid password should contain atleast - 8 chars, an upper and a lower letter , a digit and a special symbol
    valid_password = re.compile(r'^(?=.*?[A-Z])(?=(.*[a-z]){1,})(?=(.*[\d]){1,})(?=(.*[\W]){1,})(?!.*\s).{8,}$')
    if valid_password.match(password) is None:
        messagebox.showerror("Error", "Invalid password!\n"
                                      "Password should contain minimum 8 characters, an upper and a lower letter, a digit and a special symbol!")
        return False
    return True


def encrypted_password(password):
    # Encode password into a readable utf-8 byte code
    password = password.encode('utf-8')
    # Hash the encoded password and generate a salt
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_password


def salary_validation(salary):
    if len(salary) < 4:
        messagebox.showerror("Error", "Invalid salary!\nSalary should contain at least 4 digits!")
        return False

    for char in range(len(salary)):
        current_char = salary[char]
        if not current_char.isdigit():
            messagebox.showerror("Error", "Invalid salary!\nSalary should contain only digits!")
            return False
    return True


def email_validation(email):
    valid_email = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")
    if valid_email.match(email) is None:
        messagebox.showerror("Error", "Invalid e-mail!")
        return False
    return True


def submit_data():
    path = 'user_data.xlsx'
    df1 = pd.read_excel(path)
    row_a = df1['username']
    row_b = df1['password']
    row_c = df1['salary']
    row_d = df1['e-mail']

    username, password, salary, email = entry_username.get(), entry_password.get(), entry_salary.get(), entry_email.get()
    if username_validation(username) and password_validation(password) and salary_validation(salary) \
            and email_validation(email):
        final_password = encrypted_password(password)
        A = pd.Series(username)
        B = pd.Series(final_password)
        C = pd.Series(salary)
        D = pd.Series(email)
        row_a = row_a.append(A)
        row_b = row_b.append(B)
        row_c = row_c.append(C)
        row_d = row_d.append(D)
        df2 = pd.DataFrame({"username": row_a, "password": row_b, "salary": row_c + "$", "e-mail": row_d})
        df2.to_excel(path, index=False)
        entry_username.delete(0, END)
        entry_password.delete(0, END)
        entry_salary.delete(0, END)
        entry_email.delete(0, END)


def check_data():
    os.system("user_data.xlsx")


check_file()
master = Tk()
Label(master, text="username").grid(row=0)
Label(master, text="password").grid(row=1)
Label(master, text="salary").grid(row=2)
Label(master, text="e-mail").grid(row=3)

entry_username = Entry(master)
entry_password = Entry(master)
entry_salary = Entry(master)
entry_email = Entry(master)

entry_username.grid(row=0, column=1)
entry_password.grid(row=1, column=1)
entry_salary.grid(row=2, column=1)
entry_email.grid(row=3, column=1)

Button(master, text='Check data', command=check_data).grid(row=5, column=0, pady=4)
Button(master, text='Submit', command=submit_data).grid(row=5, column=1, pady=4)
Button(master, text='Quit', command=master.quit).grid(row=6, column=1, pady=4)

master.mainloop()
