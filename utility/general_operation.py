from tkinter import filedialog

def select_folder(self):
    folder = filedialog.askdirectory(title="Select Image Folder")
    if folder:
        self.image_folder = folder
        self.load_images()
        self.load_existing_annotations()


def prev_image(self):
    if self.current_image_index > 0:
        self.current_image_index -= 1
        self.load_current_image()

def next_image(self):
    if self.current_image_index < len(self.image_files) - 1:
        self.current_image_index += 1
        self.load_current_image()