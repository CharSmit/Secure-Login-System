import tkinter as tk
from tkinter import messagebox
from User import User
from UserDatabase import *

# Initialize the database
initialize_database()

# Tracks login status
logged_in_user = None

'''Function that handles registering a new user, and the messages that are displayed when this happens'''
def register_user():
    username = entry_register_username.get()
    password = entry_register_password.get()
    if not username or not password:
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    
    # Check if the username already exists
    if get_user(username):
        messagebox.showerror("Error", "Username already exists. Please choose another.")
        return

    # Create a new user and add to the database
    user = User(username, password)
    add_user(user.username, user.password.decode()) 
    messagebox.showinfo("Success", "User registered successfully!")

# Function to handle login
def login_user():
    global logged_in_user
    username = entry_login_username.get()
    password = entry_login_password.get()
    
    if not username or not password:
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    
   
    # Retrieve user data from the database
    user_data = get_user(username)
    if not user_data:
        messagebox.showerror("Error", "Username not found.")
        return


    
    # Verify the password
    retrieved_user = User(user_data["username"], None)
    retrieved_user.password = user_data["password_hash"]
    
    if retrieved_user.check_password(password):
        logged_in_user = retrieved_user
        messagebox.showinfo("Success", "Login successful!")
        login_frame.pack_forget()   
        register_frame.pack_forget()  
        change_password_frame.pack(side=tk.TOP, fill=tk.X)  
        display_logged_in_username()  
    else:
        messagebox.showerror("Error", "Incorrect password.")

# Function to change the password
def change_password():
    current_password = entry_change_current_password.get()
    new_password = entry_change_new_password.get()
    
    if not current_password or not new_password:
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    
    
    if logged_in_user.check_password(current_password):
        
        if logged_in_user.update_password(current_password, new_password):
           
            update_user_password(logged_in_user.username, logged_in_user.password.decode())  
            messagebox.showinfo("Success", "Password changed successfully!")
        else:
            messagebox.showerror("Error", "Failed to change password.")
    else:
        messagebox.showerror("Error", "Incorrect current password.")


def display_logged_in_username():
    logged_in_label.config(text=f"Logged in as: {logged_in_user.username}")


root = tk.Tk()
root.title("Secure Login System")
root.geometry("400x400")

register_frame = tk.Frame(root, padx=10, pady=10)
register_frame.pack(side=tk.TOP, fill=tk.X)

tk.Label(register_frame, text="Register", font=("Helvetica", 16)).pack()
tk.Label(register_frame, text="Username").pack()
entry_register_username = tk.Entry(register_frame)
entry_register_username.pack()
tk.Label(register_frame, text="Password").pack()
entry_register_password = tk.Entry(register_frame, show="*")
entry_register_password.pack()
tk.Button(register_frame, text="Register", command=register_user).pack(pady=5)

# Login Frame
login_frame = tk.Frame(root, padx=10, pady=10)
login_frame.pack(side=tk.TOP, fill=tk.X)

tk.Label(login_frame, text="Login", font=("Helvetica", 16)).pack()
tk.Label(login_frame, text="Username").pack()
entry_login_username = tk.Entry(login_frame)
entry_login_username.pack()
tk.Label(login_frame, text="Password").pack()  
entry_login_password = tk.Entry(login_frame, show="*") 
entry_login_password.pack()
tk.Button(login_frame, text="Login", command=login_user).pack(pady=5)


change_password_frame = tk.Frame(root, padx=10, pady=10)

tk.Label(change_password_frame, text="Change Password", font=("Helvetica", 16)).pack()
tk.Label(change_password_frame, text="Current Password").pack()
entry_change_current_password = tk.Entry(change_password_frame, show="*")
entry_change_current_password.pack()
tk.Label(change_password_frame, text="New Password").pack()
entry_change_new_password = tk.Entry(change_password_frame, show="*")
entry_change_new_password.pack()
tk.Button(change_password_frame, text="Change Password", command=change_password).pack(pady=5)

'''displays logged in username'''
logged_in_label = tk.Label(root, text="Not logged in", font=("Helvetica", 12))
logged_in_label.pack(side=tk.BOTTOM, pady=10)


root.mainloop()
