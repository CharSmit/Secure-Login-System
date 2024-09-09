import random
language = []
language += [chr(i) for i in range(65, 91)]
language += [chr(i) for i in range(97, 123)]
language += [chr(i) for i in range(48,58)]

class User:
    def __init__(self) -> None:
        self.username = None
        self.password = None
        self.phone = None
        self.email = None
        self.password = None
    
    def setUsername(self, user):
        try:
            with open('usernames.txt', 'a+') as read:
                read.seek(0)
                usernames = read.readlines()
                usernames = [user.strip() for user in usernames]
                if user in usernames:
                    return False
                read.write(user + '\n')
                return True
        except FileNotFoundError:
            with open(usernames.txt, 'w') as file:
                file.write(user + '\n')
                return True
    
    def set_password(self):
        passw = input('Enter the password for the user')
        self.password = self.encrypt_password(passw)


    def create_key(self, string):
        key = []
        for i in range(len(string)):
            key.append(random.randint(0, 62))
        return key

    def encrypt_password(self, password):
        key = create_key(password)
        encrypted_word = ''
        for i in range(len(key)):
            new_index = (language.index(password[i]) + key[i]) % 62
            encrypted_word += language[new_index]
        return encrypted_word





