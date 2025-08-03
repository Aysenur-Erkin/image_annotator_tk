from models.annotation import PolygonAnnotation

class PolyTool:
    def __init__(self, canvas, on_complete, get_color):
        self.canvas = canvas
        self.on_complete = on_complete
        self.get_color = get_color
        self.points = []
        self.line_ids = []
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
            fill=color, tags="annotation"
        )
        if len(self.points) > 1:
            x0, y0 = self.points[-2]
            lid = self.canvas.create_line(
                x0, y0, x, y,
                fill=color, width=2,
                tags="annotation"
            )
            self.line_ids.append(lid)

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
            tags="annotation"
        )

    def finish(self, event):
        if len(self.points) < 3:
            self.cancel(event)
            return
        x0, y0 = self.points[0]
        x1, y1 = self.points[-1]
        color = self.get_color()
        self.line_ids.append(
            self.canvas.create_line(
                x1, y1, x0, y0,
                fill=color, width=2,
                tags="annotation"
            )
        )
        self._clear_temp()
        img_path = getattr(self.canvas, "image_path", None)
        if img_path:
            ann = PolygonAnnotation.create(
                image_path=img_path,
                points=self.points
            )
            ann.color = color
            self.on_complete(ann)
        self.points = []
        self.line_ids = []

    def cancel(self, event):
        for lid in self.line_ids:
            self.canvas.delete(lid)
        self._clear_temp()
        self.points = []
        self.line_ids = []

    def _clear_temp(self):
        if self.temp_line:
            self.canvas.delete(self.temp_line)
            self.temp_line = None
