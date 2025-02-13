class Replie:
    def __init__(self, reply_id, reply_text, user):
        self.reply_id = reply_id
        self.reply_text = reply_text
        self.user = user
        self.likes = 0

    def correct_reply(self, reply_id, new_reply_text):
        self.reply_id = reply_id
        self.reply_text = new_reply_text

    def show_reply(self):
        return self.user, self.reply_text
