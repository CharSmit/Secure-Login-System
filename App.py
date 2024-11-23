import tkinter as tk
from tkinter import messagebox
from User import User
from UserDatabase import * 


initialize_database()

def register_user():
    username = entry_register_username.get()
    password = entry_register_password.get()
    if not username or not password:
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    
    if get_user(username):
        messagebox.showerror("Error", "Username already exists. Please choose another.")
        return

  
    user = User(username, password)
    add_user(user.username, user.password.decode())  
    messagebox.showinfo("Success", "User registered successfully!")


def login_user():
    username = entry_login_username.get()
    password = entry_login_password.get()
    
    if not username or not password:
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    
    print(f"Attempting to log in with username: {username} and password: {password}")
    
    user_data = get_user(username)
    if not user_data:
        messagebox.showerror("Error", "Username not found.")
        return

    print(f"User found: {user_data}")
    
   
    retrieved_user = User(user_data["username"], None)
    retrieved_user.password = user_data["password_hash"]
    
    if retrieved_user.check_password(password):
        messagebox.showinfo("Success", "Login successful!")
    else:
        messagebox.showerror("Error", "Incorrect password.")


root = tk.Tk()
root.title("Secure Login System")
root.geometry("400x300")

#
frame_register = tk.Frame(root, padx=10, pady=10)
frame_register.pack(side=tk.TOP, fill=tk.X)

tk.Label(frame_register, text="Register", font=("Helvetica", 16)).pack()
tk.Label(frame_register, text="Username").pack()
entry_register_username = tk.Entry(frame_register)
entry_register_username.pack()
tk.Label(frame_register, text="Password").pack()
entry_register_password = tk.Entry(frame_register, show="*")
entry_register_password.pack()
tk.Button(frame_register, text="Register", command=register_user).pack(pady=5)

frame_login = tk.Frame(root, padx=10, pady=10)
frame_login.pack(side=tk.TOP, fill=tk.X)

tk.Label(frame_login, text="Login", font=("Helvetica", 16)).pack()
tk.Label(frame_login, text="Username").pack()
entry_login_username = tk.Entry(frame_login)
entry_login_username.pack()
tk.Label(frame_login, text="Password").pack()  
entry_login_password = tk.Entry(frame_login, show="*")  
entry_login_password.pack()
tk.Button(frame_login, text="Login", command=login_user).pack(pady=5)


root.mainloop()
