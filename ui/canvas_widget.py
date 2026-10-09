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
        # canvas position of the image's top-left corner
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.pan_start = None
        self.on_view_change = None

        self.bind('<Configure>', lambda e: self._refresh())
        self.bind('<MouseWheel>', self._on_mousewheel)
        # Linux sends the wheel as buttons 4 / 5
        self.bind('<Button-4>', lambda e: self._zoom(e.x, e.y, 1.1))
        self.bind('<Button-5>', lambda e: self._zoom(e.x, e.y, 1 / 1.1))
        self.bind('<ButtonPress-2>', self._on_pan_start)
        self.bind('<B2-Motion>', self._on_pan_move)

    def load_image(self, path):
        self.image = Image.open(path)
        self.image_path = path
        self.scale_factor = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0
        self._refresh()

    def to_image(self, x, y):
        s = self.scale_factor
        return (x - self.offset_x) / s, (y - self.offset_y) / s

    def to_canvas(self, x, y):
        s = self.scale_factor
        return x * s + self.offset_x, y * s + self.offset_y

    def clamp(self, x, y):
        w, h = self.image.size
        return min(max(x, 0), w), min(max(y, 0), h)

    def _refresh(self):
        self.delete('image')
        if not self.image:
            return

        s = self.scale_factor
        w, h = self.image.size
        # resize only the part of the image that is on screen
        left, top = self.to_image(0, 0)
        right, bottom = self.to_image(self.winfo_width(), self.winfo_height())
        x0, y0 = max(0, int(left)), max(0, int(top))
        x1, y1 = min(w, int(right) + 1), min(h, int(bottom) + 1)
        if x1 > x0 and y1 > y0:
            part = self.image.crop((x0, y0, x1, y1))
            size = (max(1, round((x1 - x0) * s)), max(1, round((y1 - y0) * s)))
            resample = Image.NEAREST if s >= 2 else Image.BILINEAR
            self.photo = ImageTk.PhotoImage(part.resize(size, resample))
            cx, cy = self.to_canvas(x0, y0)
            self.create_image(cx, cy, anchor='nw', image=self.photo, tags='image')
            self.tag_lower('image')

        if self.on_view_change:
            self.on_view_change()

    def _on_mousewheel(self, event):
        self._zoom(event.x, event.y, 1.1 if event.delta > 0 else 1 / 1.1)

    def _zoom(self, x, y, factor):
        if not self.image:
            return
        new_scale = self.scale_factor * factor
        if not (self.min_scale <= new_scale <= self.max_scale):
            return
        # keep the point under the mouse where it is
        self.offset_x = x - (x - self.offset_x) * factor
        self.offset_y = y - (y - self.offset_y) * factor
        self.scale_factor = new_scale
        self._refresh()

    def _on_pan_start(self, event):
        self.pan_start = (event.x, event.y)

    def _on_pan_move(self, event):
        if self.pan_start:
            self.offset_x += event.x - self.pan_start[0]
            self.offset_y += event.y - self.pan_start[1]
            self.pan_start = (event.x, event.y)
            self._refresh()
