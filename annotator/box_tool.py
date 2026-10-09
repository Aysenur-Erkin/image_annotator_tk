from models.annotation import BoxAnnotation

class BoxTool:
    def __init__(self, canvas, on_complete, get_color):
        self.canvas = canvas
        self.on_complete = on_complete
        self.get_color = get_color
        self.start = None
        self.rect_id = None

    def activate(self):
        self.canvas.bind("<ButtonPress-1>",    self.on_button_press)
        self.canvas.bind("<B1-Motion>",        self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>",  self.on_button_release)

    def deactivate(self):
        self.cancel(None)
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def _image_point(self, event):
        return self.canvas.clamp(*self.canvas.to_image(event.x, event.y))

    def on_button_press(self, event):
        if not self.canvas.image:
            return
        self.start = self._image_point(event)
        x, y = self.canvas.to_canvas(*self.start)
        self.rect_id = self.canvas.create_rectangle(
            x, y, x, y,
            outline=self.get_color(), width=2,
            tags="preview"
        )

    def on_mouse_move(self, event):
        if not self.rect_id:
            return
        x0, y0 = self.canvas.to_canvas(*self.start)
        x1, y1 = self.canvas.to_canvas(*self._image_point(event))
        self.canvas.coords(self.rect_id, x0, y0, x1, y1)

    def on_button_release(self, event):
        if not self.rect_id:
            return
        sx, sy = self.start
        ex, ey = self._image_point(event)
        self.cancel(event)
        # store in image pixels, top-left first
        x1, x2 = sorted((round(sx), round(ex)))
        y1, y2 = sorted((round(sy), round(ey)))
        img_path = self.canvas.image_path
        if img_path and x2 > x1 and y2 > y1:
            ann = BoxAnnotation.create(
                image_path=img_path,
                x1=x1, y1=y1, x2=x2, y2=y2
            )
            self.on_complete(ann)

    def cancel(self, event):
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.start = self.rect_id = None
