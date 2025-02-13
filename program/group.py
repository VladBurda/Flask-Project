class Group:
    def __init__(self, group_name, description, group_id, group_owner, privacy):
        self.group_owner = group_owner
        self.group_name = group_name
        self.description = description
        self.group_id = group_id
        self.privacy = privacy
        self.users = []
        self.topics ={}
        self.reserved_topics = {}

    #Add user to group
    def add_user(self, user_id):
        self.users.append(user_id)

    #Make corrections to description
    def make_corrections(self, group_name, description):
        self.group_name = group_name
        self.description = description
