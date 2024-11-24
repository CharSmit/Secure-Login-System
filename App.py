import tkinter as tk
from tkinter import messagebox
from User import User
from UserDatabase import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
import os
from dotenv import load_dotenv
import time
import re

load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 465))
otps = {}

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def send_otp(email):
    try:
        otp_code = generate_otp()
        otps[email] = (otp_code, time.time())
        server = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        message = MIMEMultipart()
        message["From"] = EMAIL_ADDRESS
        message["To"] = email
        message["Subject"] = "Your 2FA Code"
        body = f"Your 2FA code is: {otp_code}"
        message.attach(MIMEText(body, "plain"))
        server.sendmail(EMAIL_ADDRESS, email, message.as_string())
        server.quit()
        print("2FA code sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

def verify_otp(user_email, input_otp):
    """Verify the OTP provided by the user."""
    current_time = time.time()
    if user_email in otps:
        stored_otp, timestamp = otps[user_email]
        if current_time - timestamp > 300:  
            print("OTP has expired.")
            del otps[user_email]
            return False
        if stored_otp == input_otp:
            print("OTP verified successfully.")
            del otps[user_email]
            return True
    print("Invalid OTP.")
    return False

# Initialize the database
initialize_database()

# Tracks logged in user
logged_in_user = None

def switch_frame(frame_to_show):
    """Hide all frames and show the selected frame."""
    if frame_to_show == login_frame:
        change_password_frame.pack_forget()
        register_frame.pack(fill=tk.X)
        login_frame.pack(fill=tk.X)
    
    else:
        for frame in [register_frame, login_frame, change_password_frame]:
            frame.pack_forget() 
        frame_to_show.pack(fill=tk.X)  


'''Function that handles registering a new user, and the messages that are displayed when this happens'''
def register_user():
    username = entry_register_username.get()
    email = entry_register_email.get()
    password = entry_register_password.get()

    # Validate fields are not empty
    if not username or not email or not password:
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    
    # Email Structure regular language
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        messagebox.showerror("Error", "Invalid email address.")
        return
    
    # Check if username or email already exists
    if get_user(username):
        messagebox.showerror("Error", "Username already exists.")
        return

    # Create a new user and store in the database
    user = User(username, password)
    add_user(user.username, email, user.password.decode())  # Pass email to add_user
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

        # Send OTP to user's email
        user_email = user_data["email"]
        send_otp(user_email)

        
        otp_window = tk.Toplevel(root)
        otp_window.title("Enter OTP")
        tk.Label(otp_window, text="Enter the OTP sent to your email:").pack()
        entry_otp = tk.Entry(otp_window)
        entry_otp.pack()

        def verify_otp_code():
            entered_otp = entry_otp.get()
            outcome = verify_otp(user_email, entered_otp)
            print(outcome)
            if outcome:
                messagebox.showinfo("Success", "Login successful!")
                otp_window.destroy()
                display_logged_in_username()
                switch_frame(change_password_frame)
            else:
                messagebox.showerror("Error", "Invalid or expired OTP.")
        tk.Button(otp_window, text="Verify", command=verify_otp_code).pack(pady=10)
    else:
        messagebox.showerror("Error", "Incorrect password.")


# Function to change the password
def change_password():
    global logged_in_user
    current_password = entry_change_current_password.get()
    new_password = entry_change_new_password.get()
    
    if not current_password or not new_password:
        messagebox.showerror("Error", "Please fill in all fields.")
        
    if logged_in_user.check_password(current_password):
        
        if logged_in_user.update_password(current_password, new_password):
        
            update_user_password(logged_in_user.username, logged_in_user.password.decode())  
            messagebox.showinfo("Success", "Password changed successfully!")
            logged_in_user = None
            switch_frame(login_frame)
            display_logged_in_username()

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

# Register Frame
tk.Label(register_frame, text="Register", font=("Helvetica", 16)).pack()
tk.Label(register_frame, text="Username").pack()
entry_register_username = tk.Entry(register_frame)
entry_register_username.pack()

tk.Label(register_frame, text="Email").pack()  # Email field
entry_register_email = tk.Entry(register_frame)
entry_register_email.pack()

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
