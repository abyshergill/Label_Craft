import tkinter as tk
from tkinter import ttk, messagebox

from canvas.annotations import( draw_annotations, load_existing_annotations,
                               update_annotation_list, delete_annotation, export_annotations)
from canvas.action import (on_canvas_click, on_canvas_drag, on_canvas_release, on_key_press)

from image_handler.handler import (load_images, load_current_image)

from utility.class_operation import (update_class_list, update_class_combo, on_class_select,
                                     add_class, remove_class)

from utility.general_operation import (prev_image, next_image, select_folder)


class YOLOAnnotator:
    def __init__(self, root):
        self.root = root
        self.root.title("Label Craft V 0.2")
        self.root.geometry("1200x800")
        try:
            self.root.iconbitmap('icon/icon.ico')
        except:
            pass
		
        self.image_folder = ""
        self.image_files = []
        self.current_image_index = 0
        self.current_image = None
        self.photo = None
        self.canvas_image = None
        
        self.classes = ["Default Class"]  
        self.current_class = 0
        self.annotations = {}  
        self.current_bbox = None
        self.bbox_start = None
        self.temp_rect = None
        
        self.scale_factor = 1.0
        self.canvas_width = 800
        self.canvas_height = 600
        
        self.setup_ui()
        self.bind_events()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        left_panel = ttk.Frame(main_frame, width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        folder_frame = ttk.LabelFrame(left_panel, text="Dataset", padding=10)
        folder_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(folder_frame, text="Select Image Folder", 
                  command=self.select_folder).pack(fill=tk.X)
        
        self.folder_label = ttk.Label(folder_frame, text="No folder selected", 
                                     wraplength=250)
        self.folder_label.pack(pady=(5, 0))
        
        class_frame = ttk.LabelFrame(left_panel, text="Classes", padding=10)
        class_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(class_frame, text="Current Classes:").pack(anchor=tk.W)
        
        listbox_frame = ttk.Frame(class_frame)
        listbox_frame.pack(fill=tk.X, pady=(5, 10))
        
        self.class_listbox = tk.Listbox(listbox_frame, height=4)
        self.class_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.class_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.class_listbox.yview)
        
        class_btn_frame = ttk.Frame(class_frame)
        class_btn_frame.pack(fill=tk.X)
        
        ttk.Button(class_btn_frame, text="Add Class", 
                  command=self.add_class).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(class_btn_frame, text="Remove Class", 
                  command=self.remove_class).pack(side=tk.LEFT)
        
        ttk.Label(class_frame, text="Active Class:").pack(anchor=tk.W, pady=(10, 5))
        self.class_var = tk.StringVar()
        self.class_combo = ttk.Combobox(class_frame, textvariable=self.class_var, 
                                       state="readonly")
        self.class_combo.pack(fill=tk.X)
        self.class_combo.bind('<<ComboboxSelected>>', self.on_class_select)
        
        nav_frame = ttk.LabelFrame(left_panel, text="Navigation", padding=10)
        nav_frame.pack(fill=tk.X, pady=(0, 10))
        
        nav_btn_frame = ttk.Frame(nav_frame)
        nav_btn_frame.pack(fill=tk.X)
        
        self.prev_btn = ttk.Button(nav_btn_frame, text="Previous", 
                                  command=self.prev_image, state=tk.DISABLED)
        self.prev_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.next_btn = ttk.Button(nav_btn_frame, text="Next", 
                                  command=self.next_image, state=tk.DISABLED)
        self.next_btn.pack(side=tk.LEFT)
        
        self.image_info = ttk.Label(nav_frame, text="No images loaded")
        self.image_info.pack(pady=(10, 0))
        
        ann_frame = ttk.LabelFrame(left_panel, text="Current Annotations", padding=10)
        ann_frame.pack(fill=tk.BOTH, expand=True)
        
        ann_listbox_frame = ttk.Frame(ann_frame)
        ann_listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.ann_listbox = tk.Listbox(ann_listbox_frame)
        self.ann_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ann_scrollbar = ttk.Scrollbar(ann_listbox_frame, orient=tk.VERTICAL)
        ann_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.ann_listbox.config(yscrollcommand=ann_scrollbar.set)
        ann_scrollbar.config(command=self.ann_listbox.yview)
        
        ttk.Button(ann_frame, text="Delete Selected", 
                  command=self.delete_annotation).pack(pady=(10, 0))
        
        export_frame = ttk.LabelFrame(left_panel, text="Export", padding=10)
        export_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(export_frame, text="Export YOLO Annotations", 
                  command=self.export_annotations).pack(fill=tk.X)
        
        canvas_frame = ttk.LabelFrame(main_frame, text="Image", padding=10)
        canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg='gray', 
                               width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(expand=True)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Select a folder to begin")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.update_class_list()
        self.update_class_combo()
    
    def bind_events(self):
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.root.bind("<Key>", self.on_key_press)
        self.root.focus_set()
    
    def select_folder(self):
        select_folder(self)
    
    def load_images(self):
        load_images(self)
    
    def load_existing_annotations(self):
       load_existing_annotations(self)
    
    def load_current_image(self):
        load_current_image(self)
    
    def draw_annotations(self):
        draw_annotations(self)
    
    def on_canvas_click(self, event):
        on_canvas_click(self, event)
    
    def on_canvas_drag(self, event):
        on_canvas_drag(self, event)
    
    def on_canvas_release(self, event):
        on_canvas_release(self, event)
    
    def on_key_press(self, event):
        on_key_press(self, event)
    
    def prev_image(self):
        prev_image(self)
    
    def next_image(self):
        next_image(self)
    
    def add_class(self):
        add_class(self)
    
    def remove_class(self):
        remove_class(self)

    def update_class_list(self):
        update_class_list(self)
    
    def update_class_combo(self):
        update_class_combo(self)
    
    def on_class_select(self, event):
       on_class_select(self, event)

    def update_annotation_list(self):
        update_annotation_list(self)

    def delete_annotation(self):
        delete_annotation(self)
    
    def export_annotations(self):
        export_annotations(self)

def main():
    root = tk.Tk()
    app = YOLOAnnotator(root)
    root.mainloop()

if __name__ == "__main__":
    main()