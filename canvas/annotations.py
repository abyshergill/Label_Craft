import tkinter as tk
from tkinter import messagebox
from pathlib import Path

def draw_annotations(self):
    if not self.current_image:
        return
    
    image_name = Path(self.image_files[self.current_image_index]).stem
    annotations = self.annotations.get(image_name, [])
    
    img_width, img_height = self.current_image.size
    
    x_offset = (self.canvas_width - int(img_width * self.scale_factor)) // 2
    y_offset = (self.canvas_height - int(img_height * self.scale_factor)) // 2
    
    colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'cyan', 'magenta']
    
    for i, (class_id, x_center, y_center, width, height) in enumerate(annotations):
        x1 = (x_center - width/2) * img_width * self.scale_factor + x_offset
        y1 = (y_center - height/2) * img_height * self.scale_factor + y_offset
        x2 = (x_center + width/2) * img_width * self.scale_factor + x_offset
        y2 = (y_center + height/2) * img_height * self.scale_factor + y_offset
        
        color = colors[class_id % len(colors)]
        
        self.canvas.create_rectangle(x1, y1, x2, y2, 
                                    outline=color, width=2, tags="annotation")
        
        class_name = self.classes[class_id] if class_id < len(self.classes) else f"Class {class_id}"
        self.canvas.create_text(x1, y1-5, text=class_name, 
                                fill=color, anchor=tk.SW, tags="annotation")


def load_existing_annotations(self):
    self.annotations = {}
    
    for image_file in self.image_files:
        image_name = Path(image_file).stem
        txt_file = Path(self.image_folder) / f"{image_name}.txt"
        
        if txt_file.exists():
            try:
                with open(txt_file, 'r') as f:
                    annotations = []
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) == 5:
                            class_id = int(parts[0])
                            x, y, w, h = map(float, parts[1:5])
                            annotations.append((class_id, x, y, w, h))
                    self.annotations[image_name] = annotations
            except Exception as e:
                print(f"Error loading annotations for {image_name}: {e}")

    
def update_annotation_list(self):
    self.ann_listbox.delete(0, tk.END)
    
    if not self.image_files:
        return
    
    image_name = Path(self.image_files[self.current_image_index]).stem
    annotations = self.annotations.get(image_name, [])
    
    for i, (class_id, x, y, w, h) in enumerate(annotations):
        class_name = self.classes[class_id] if class_id < len(self.classes) else f"Class {class_id}"
        self.ann_listbox.insert(tk.END, f"{i}: {class_name} ({w:.3f}x{h:.3f})")
    

def delete_annotation(self):
    selection = self.ann_listbox.curselection()
    if not selection:
        return

    image_name = Path(self.image_files[self.current_image_index]).stem
    annotations = self.annotations.get(image_name, [])

    index = selection[0]
    if 0 <= index < len(annotations):
        del annotations[index]
        if not annotations:
            del self.annotations[image_name]
        
        self.canvas.delete("annotation")
        self.draw_annotations()
        self.update_annotation_list()
        self.status_var.set("Deleted annotation")

def export_annotations(self):
    if not self.annotations:
        messagebox.showwarning("Warning", "No annotations to export")
        return
    
    # Create classes.txt file
    classes_file = Path(self.image_folder) / "classes.txt"
    with open(classes_file, 'w') as f:
        for class_name in self.classes:
            f.write(f"{class_name}\n")
    
    # Export YOLO format annotations
    exported_count = 0
    for image_name, annotations in self.annotations.items():
        txt_file = Path(self.image_folder) / f"{image_name}.txt"
        with open(txt_file, 'w') as f:
            for class_id, x_center, y_center, width, height in annotations:
                f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
        exported_count += 1
    
    messagebox.showinfo("Export Complete", 
                        f"Exported {exported_count} annotation files and classes.txt to:\n{self.image_folder}")
    self.status_var.set(f"Exported {exported_count} annotation files")
