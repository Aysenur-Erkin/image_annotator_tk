import tkinter as tk
from PIL import Image, ImageTk

class CanvasWidget(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, bg='lightgray', highlightthickness=0)
        self.image = None
        self.photo = None
        self.image_path = None
        self.scale_factor = 1.0
        self.min_scale = 0.1
        self.max_scale = 10.0
        self.pan_start = None

        self.bind('<Configure>', lambda e: self._refresh())
        self.bind('<MouseWheel>', self._on_mousewheel)
        self.bind('<Button-4>', self._on_mousewheel)
        self.bind('<Button-5>', self._on_mousewheel)
        self.bind('<ButtonPress-2>', self._on_pan_start)
        self.bind('<B2-Motion>', self._on_pan_move)

    def load_image(self, path):
        self.image = Image.open(path)
        self.image_path = path
        self.scale_factor = 1.0
        self.delete('all')
        self._refresh()

    def _refresh(self):
        self.delete('all')
        if not self.image:
            return

        w, h = self.image.size
        new_size = (int(w * self.scale_factor), int(h * self.scale_factor))
        resized = self.image.resize(new_size, resample=Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(resized)
        self.create_image(0, 0, anchor='nw', image=self.photo)
        self.configure(scrollregion=self.bbox('all'))

    def _on_mousewheel(self, event):
        if hasattr(event, 'delta'):
            factor = 1.1 if event.delta > 0 else 0.9
        else:
            factor = 1.1 if event.num == 4 else 0.9

        new_scale = self.scale_factor * factor
        if not (self.min_scale <= new_scale <= self.max_scale):
            return
        self.scale_factor = new_scale
        super().scale('all', event.x, event.y, factor, factor)
        self.configure(scrollregion=self.bbox('all'))

    def _on_pan_start(self, event):
        self.pan_start = (event.x, event.y)

    def _on_pan_move(self, event):
        if self.pan_start:
            dx = event.x - self.pan_start[0]
            dy = event.y - self.pan_start[1]
            self.move('all', dx, dy)
            self.pan_start = (event.x, event.y)