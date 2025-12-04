from tkinter import messagebox
       
def welcome_message():
    welcome_msg = (
        "Welcome to Label Craft V 0.2 \n\n"
        "Instructions :\n"
        "- Click 'Select Image Folder' to start\n"
        "- Use arrows to navigate images\n"
        "- Press 0-9 to quickly select classes\n"
        "- Click and drag to draw bounding boxes\n"
        "- Right-click or ESC to cancel drawing\n"
        "- Export creates a separate folder with images and annotations\n\n"
        "Happy annotating!"
        )
    messagebox.showinfo("Welcome", welcome_msg)