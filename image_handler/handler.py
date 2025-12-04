from pathlib import Path
import tkinter as tk
import os
from tkinter import messagebox
from PIL import Image, ImageTk

def load_images(self):
    if not self.image_folder:
        return

    extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif')

    self.image_files = []
    
    p = Path(self.image_folder)
    
    for f in os.listdir(self.image_folder):
        file_path = p / f 
        if file_path.is_file() and str(file_path).lower().endswith(extensions):
            self.image_files.append(str(file_path))

    self.image_files.sort() 
    if self.image_files:
        self.current_image_index = 0
        self.folder_label.config(text=f"Loaded {len(self.image_files)} images")
        self.prev_btn.config(state=tk.NORMAL)
        self.next_btn.config(state=tk.NORMAL)
        self.load_current_image()
    else:
        messagebox.showwarning("Warning", "No image files found in the selected folder")


def load_current_image(self):
    if not self.image_files:
        return
    
    image_path = self.image_files[self.current_image_index]
    image_name = Path(image_path).name
    
    try:
        # Load and resize image
        self.current_image = Image.open(image_path)
        
        # Calculate scale factor to fit canvas
        img_width, img_height = self.current_image.size
        scale_x = self.canvas_width / img_width
        scale_y = self.canvas_height / img_height
        self.scale_factor = min(scale_x, scale_y, 1.0)  # Don't upscale
        
        # Resize image
        new_width = int(img_width * self.scale_factor)
        new_height = int(img_height * self.scale_factor)
        
        display_image = self.current_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(display_image)
        
        # Clear canvas and display image
        self.canvas.delete("all")
        
        # Center the image on canvas
        x_offset = (self.canvas_width - new_width) // 2
        y_offset = (self.canvas_height - new_height) // 2
        
        self.canvas_image = self.canvas.create_image(x_offset, y_offset, 
                                                    anchor=tk.NW, image=self.photo)
        
        # Draw existing annotations
        self.draw_annotations()
        
        # Update UI
        self.image_info.config(text=f"{self.current_image_index + 1}/{len(self.image_files)}: {image_name}")
        self.update_annotation_list()
        self.status_var.set(f"Loaded: {image_name} ({img_width}x{img_height})")
        
    except Exception as e:
        messagebox.showerror("Error", f"Could not load image: {e}")