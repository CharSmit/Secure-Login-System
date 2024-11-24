# SecureLogin System

The **SecureLogin System** is a Python-based application for secure user registration and authentication using **bcrypt** for password hashing and **OTP (One-Time Password)** for two-factor authentication via email. 

---

## Features

1. **User Management**:
   - Stores usernames, password hashes (encrypted using bcrypt), and email addresses securely in a `users.database` file.
   - Provides options to **register** a new user or **log in** with an existing account.

2. **Login Flow**:
   - Upon entering a valid username and password, the system sends a randomly generated OTP to the registered email address.
   - The registered email for each user is stored during registration.

3. **Environment Configuration**:
   - Email credentials used to send OTPs are securely stored in a `.env` file. This file must include the following fields:
     ```env
     EMAIL_HOST=smtp.gmail.com
     EMAIL_PORT=465
     EMAIL_ADDRESS=<your-email@example.com>
     EMAIL_PASSWORD=<your-email-password>
     ```

4. **Secure OTP Delivery**:
   - OTPs are sent via the specified email configured in the `.env` file.
   - OTPs are time-sensitive and expire after 5 minutes.

5. **Password Management**:
   - Users can change their password after successfully logging in and verifying the OTP.
   - Upon changing the password, the user is logged out to enhance security.

---

## How It Works

1. **Registration**:
   - Users register by providing a **username**, **email**, and **password**.
   - The password is hashed and stored securely alongside the username and email.

2. **Login**:
   - Users provide their **username** and **password**.
   - If credentials are correct, an OTP is sent to the user's registered email.

3. **OTP Verification**:
   - Users enter the OTP they receive to complete the login process.
   - The OTP is validated, ensuring it matches the sent code and hasn't expired.

4. **Password Change**:
   - After successfully logging in, users can update their password.
   - Once the password is changed, the system automatically logs the user out.

---

## Requirements

- Python 3.x
- **Dependencies**:
  - `tkinter` (for UI)
  - `smtplib` (for email)
  - `dotenv` (to load environment variables)
  - `bcrypt` (for password hashing)
  - `random` and `string` (for OTP generation)

---

