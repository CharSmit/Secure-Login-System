import bcrypt

class User:


    def __init__(self, username, password) -> None:
        
        self.username = username
        self.password = self.encrypt_password(password)
    
    def encrypt_password(self, password):

        # Generates a salt for this user instance, is regenerated everytime password is updated
        self.salt = bcrypt.gensalt()
        # Hashes the supplied password and salt returning the value, which will be stored in self.password 
        encrypted = bcrypt.hashpw(password.encode(), self.salt)
        return encrypted

    def check_password(self, passattempt):

        # Hashes the password supplied with the same salt as the original hashing.
        # Compares the result with the stored hash value for that user instance, returns result.
        if self.password == bcrypt.hashpw(passattempt.encode(), self.salt):
            return True
        
        return False
     
    def update_password(self, oldpassword, newpassword):

        # Checks if the oldpassword variable hashes to the same value as the stored password hash.
        # Takes the new password variable and passes it into encryptpassword function.
        # Sets the value of self.password as the value of that function
        if self.check_password(oldpassword):
            self.password = self.encrypt_password(newpassword)
            return True
        else:
            return False
