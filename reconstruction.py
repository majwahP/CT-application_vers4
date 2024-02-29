from topic import Topic

class Reconstruction(Topic):
    def __init__(self):
        self.title = "Reconstruction"
        self.sub_title = []
        self.sub_title.append("ghghghbg")
        self.sub_title.append("kblkglkn")
        self.content = "This text will give info @ This should be paragraph 2 @ This should be"
        

    def get_title(self):
        return self.title

    def get_content(self):
        return self.content

    def set_title(self, new_title):
        self.title = new_title

    def set_content(self, new_content):
        self.content = new_content
