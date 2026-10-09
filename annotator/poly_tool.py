from models.annotation import PolygonAnnotation

class PolyTool:
    def __init__(self, canvas, on_complete, get_color):
        self.canvas = canvas
        self.on_complete = on_complete
        self.get_color = get_color
        self.points = []
        self.temp_line = None

    def activate(self):
        self.canvas.bind("<Button-1>", self.add_point)
        self.canvas.bind("<Motion>",   self.motion)
        self.canvas.bind("<Return>",   self.finish)
        self.canvas.bind("<Escape>",   self.cancel)

    def deactivate(self):
        self.cancel(None)
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<Return>")
        self.canvas.unbind("<Escape>")

    def add_point(self, event):
        x, y = event.x, event.y
        color = self.get_color()
        self.points.append((x, y))
        r = 3
        self.canvas.create_oval(
            x-r, y-r, x+r, y+r,
            fill=color, tags="preview"
        )
        if len(self.points) > 1:
            x0, y0 = self.points[-2]
            self.canvas.create_line(
                x0, y0, x, y,
                fill=color, width=2,
                tags="preview"
            )

    def motion(self, event):
        if not self.points:
            return
        if self.temp_line:
            self.canvas.delete(self.temp_line)
        x0, y0 = self.points[-1]
        x1, y1 = event.x, event.y
        color = self.get_color()
        self.temp_line = self.canvas.create_line(
            x0, y0, x1, y1,
            dash=(4,2), fill=color,
            tags="preview"
        )

    def finish(self, event):
        if len(self.points) < 3:
            self.cancel(event)
            return
        self.canvas.delete("preview")
        self.temp_line = None
        img_path = getattr(self.canvas, "image_path", None)
        if img_path:
            ann = PolygonAnnotation.create(
                image_path=img_path,
                points=self.points
            )
            self.on_complete(ann)
        self.points = []

    def cancel(self, event):
        self.canvas.delete("preview")
        self.temp_line = None
        self.points = []
