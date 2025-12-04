import tkinter as tk
from gui import YOLOAnnotator
from utility.welcome_window import welcome_message

def main():
    welcome_message()
    root = tk.Tk()
    app = YOLOAnnotator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
	
	
