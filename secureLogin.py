
class User:
    def __init__(self) -> None:
        self.username = None
        self.password = None
        self.phone = None
        self.email = None
    
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


