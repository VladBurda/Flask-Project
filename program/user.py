class User:
    def __init__(self, user_id,  email, password, description):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.description = description
        self.groups = []

    def username(self):
        username = self.email.split('@')[0]
        return username
    
    def add_group(self, group):
        self.groups.append(group)   

    def show_user(self):
        return self.username(), self.email, self.description
    
    def change_user_description(self, new_description):
        self.description = new_description

    

