import bcrypt

class User:


    def __init__(self, username, password) -> None:
        
        self.username = username
        if password:
            self.password = self.encrypt_password(password)
        else:
            self.password = None
    def encrypt_password(self, password):

        
        # Hashes the supplied password and salt returning the value, which will be stored in self.password 
        encrypted = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return encrypted

    def check_password(self, passattempt):
        '''
        Hashes the password supplied with the same salt as the original hashing.
        Compares the result with the stored hash value for that user instance, returns result.
        '''
        if isinstance(self.password, str):
            self.password = self.password.encode()
        return bcrypt.checkpw(passattempt.encode(), self.password)
            
        
        
    def update_password(self, oldpassword, newpassword):
        '''
        Checks if the oldpassword variable hashes to the same value as the stored password hash.
        Takes the new password variable and passes it into encryptpassword function.
        Sets the value of self.password as the value of that function
        '''
        if self.check_password(oldpassword):
            self.password = self.encrypt_password(newpassword)
            return True
        else:
            return False
