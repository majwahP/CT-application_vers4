from topic import Topic
import os
import matplotlib.pyplot as plt
from PIL import Image


class Dose(Topic):
    def __init__(self):
            super().__init__()
            self.title = "Dose"
            self.content = []      
            self.add_images("Dose_wiki")

    def get_title(self):
        return self.title

    def get_content(self):
        return self.content

    def set_title(self, new_title):
        self.title = new_title

    def set_content(self, new_content):
        self.content = new_content
    

    
    def add_images(self, folder_path):
        try:
            for filename in os.listdir(folder_path):
                if filename.lower().endswith(".png"):
                    img_path = os.path.join(folder_path, filename)
                    img = Image.open(img_path)
                    self.content.append(img)
        except FileNotFoundError:
            print(f"Folder '{folder_path}' not found.")
        except Exception as e:
            print(f"Error loading images from folder '{folder_path}': {e}")
    