import tkinter as tk
from tkinter import simpledialog, messagebox

def update_class_list(self):
    self.class_listbox.delete(0, tk.END)
    for i, class_name in enumerate(self.classes):
        self.class_listbox.insert(tk.END, f"{i}: {class_name}")

def update_class_combo(self):
    self.class_combo['values'] = [f"{i}: {name}" for i, name in enumerate(self.classes)]
    if self.classes:
        self.class_combo.current(self.current_class)

def on_class_select(self, event):
    selection = self.class_combo.current()
    if selection >= 0:
        self.current_class = selection

def add_class(self):
    new_class = simpledialog.askstring("Add Class", "Enter class name:")
    if new_class and new_class not in self.classes:
        self.classes.append(new_class)
        self.update_class_list()
        self.update_class_combo()

def remove_class(self):
    selection = self.class_listbox.curselection()
    if selection:
        index = selection[0]
        if len(self.classes) > 1:  # Keep at least one class
            del self.classes[index]
            if self.current_class >= len(self.classes):
                self.current_class = len(self.classes) - 1
            self.update_class_list()
            self.update_class_combo()
        else:
            messagebox.showwarning("Warning", "Cannot remove the last class")
