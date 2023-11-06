from users import User

class Statistics:
    def __init__(self, user:User, channel):
        self.user = user
        "The user whose statistics will be reported"
        self.channel = channel
        "The channel where the statistics will be reported"

    def display(self):
        
