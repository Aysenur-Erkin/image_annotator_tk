from models.annotation import BoxAnnotation

class BoxTool:
    def __init__(self, canvas, on_complete, get_color):
        self.canvas = canvas
        self.on_complete = on_complete
        self.get_color = get_color
        self.start_x = None
        self.start_y = None
        self.rect_id = None

    def activate(self):
        self.canvas.bind("<ButtonPress-1>",    self.on_button_press)
        self.canvas.bind("<B1-Motion>",        self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>",  self.on_button_release)

    def deactivate(self):
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        color = self.get_color()
        self.rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y,
            self.start_x, self.start_y,
            outline=color, width=2,
            tags="annotation"
        )

    def on_mouse_move(self, event):
        if not self.rect_id:
            return
        self.canvas.coords(
            self.rect_id,
            self.start_x, self.start_y,
            event.x, event.y
        )

    def on_button_release(self, event):
        if not self.rect_id:
            return
        x1, y1, x2, y2 = map(int, self.canvas.coords(self.rect_id))
        img_path = getattr(self.canvas, "image_path", None)
        color = self.get_color()
        if img_path:
            ann = BoxAnnotation.create(
                image_path=img_path,
                x1=x1, y1=y1, x2=x2, y2=y2
            )
            ann.color = color
            self.on_complete(ann)
        self.start_x = self.start_y = self.rect_id = None
