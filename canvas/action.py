from pathlib import Path

def on_canvas_click(self, event):
    if not self.current_image:
        return

    img_width, img_height = self.current_image.size
    x_offset = (self.canvas_width - int(img_width * self.scale_factor)) // 2
    y_offset = (self.canvas_height - int(img_height * self.scale_factor)) // 2
    
    if (x_offset <= event.x <= x_offset + img_width * self.scale_factor and
        y_offset <= event.y <= y_offset + img_height * self.scale_factor):
        
        self.bbox_start = (event.x, event.y)
        self.status_var.set("Drawing bounding box...")

def on_canvas_drag(self, event):
    if not self.bbox_start:
        return
    
    # Remove previous temporary rectangle
    if self.temp_rect:
        self.canvas.delete(self.temp_rect)
    
    # Draw temporary rectangle
    x1, y1 = self.bbox_start
    x2, y2 = event.x, event.y
    
    self.temp_rect = self.canvas.create_rectangle(x1, y1, x2, y2, 
                                                outline='white', width=2, dash=(5, 5))
    
def on_canvas_release(self, event):
    if not self.bbox_start or not self.current_image:
        return
    
    # Remove temporary rectangle
    if self.temp_rect:
        self.canvas.delete(self.temp_rect)
        self.temp_rect = None
    
    x1, y1 = self.bbox_start
    x2, y2 = event.x, event.y
    
    # Ensure we have a valid rectangle
    if abs(x2 - x1) < 10 or abs(y2 - y1) < 10:
        self.bbox_start = None
        self.status_var.set("Bounding box too small")
        return
    
    # Convert to image coordinates
    img_width, img_height = self.current_image.size
    x_offset = (self.canvas_width - int(img_width * self.scale_factor)) // 2
    y_offset = (self.canvas_height - int(img_height * self.scale_factor)) // 2
    
    # Convert canvas coordinates to image coordinates
    img_x1 = (min(x1, x2) - x_offset) / self.scale_factor
    img_y1 = (min(y1, y2) - y_offset) / self.scale_factor
    img_x2 = (max(x1, x2) - x_offset) / self.scale_factor
    img_y2 = (max(y1, y2) - y_offset) / self.scale_factor
    
    # Clamp to image bounds
    img_x1 = max(0, min(img_x1, img_width))
    img_y1 = max(0, min(img_y1, img_height))
    img_x2 = max(0, min(img_x2, img_width))
    img_y2 = max(0, min(img_y2, img_height))
    
    # Convert to YOLO format
    x_center = (img_x1 + img_x2) / (2 * img_width)
    y_center = (img_y1 + img_y2) / (2 * img_height)
    width = (img_x2 - img_x1) / img_width
    height = (img_y2 - img_y1) / img_height
    
    # Add annotation
    image_name = Path(self.image_files[self.current_image_index]).stem
    if image_name not in self.annotations:
        self.annotations[image_name] = []
    
    self.annotations[image_name].append((self.current_class, x_center, y_center, width, height))
    
    # Redraw
    self.canvas.delete("annotation")
    self.draw_annotations()
    self.update_annotation_list()
    
    self.bbox_start = None
    self.status_var.set(f"Added {self.classes[self.current_class]} annotation")

def on_key_press(self, event):
    if event.keysym == 'Left':
        self.prev_image()
    elif event.keysym == 'Right':
        self.next_image()
    elif event.char.isdigit():
        class_num = int(event.char)
        if 0 <= class_num < len(self.classes):
            self.current_class = class_num
            self.class_combo.current(class_num)