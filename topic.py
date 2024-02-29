class Topic:
    def get_title(self):
        raise NotImplementedError("Subclasses must implement get_title method")

    def get_content(self):
        raise NotImplementedError("Subclasses must implement get_content method")

    def set_title(self, new_title):
        raise NotImplementedError("Subclasses must implement set_title method")

    def set_content(self, new_content):
        raise NotImplementedError("Subclasses must implement set_content method")
