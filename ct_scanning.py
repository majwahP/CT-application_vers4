from topic import Topic

class CT_scanning(Topic):
    def __init__(self):
        self.title = "CT scanning"
        self.sub_title = []
        self.sub_title.append("CT")
        self.content = "This text will give info @ This should be paragraph 2 @ This should be"
        

    def get_title(self):
        return self.title

    def get_content(self):
        return self.content

    def set_title(self, new_title):
        self.title = new_title

    def set_content(self, new_content):
        self.content = new_content
