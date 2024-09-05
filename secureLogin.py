
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

user1 = User()
print(user1.setUsername('HELLO'))
user2 = User()

print(user2.setUsername('steve'))

user3 = User()
print(user3.setUsername('HELLO'))

