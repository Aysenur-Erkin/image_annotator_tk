from models.annotation import PolygonAnnotation

class PolyTool:
    def __init__(self, canvas, on_complete, get_color):
        self.canvas = canvas
        self.on_complete = on_complete
        self.get_color = get_color
        self.points = []      # image pixels
        self.mouse = None     # canvas position, for the dashed line
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
        if not self.canvas.image:
            return
        # Enter/Esc only reach the canvas when it has keyboard focus
        self.canvas.focus_set()
        x, y = self.canvas.clamp(*self.canvas.to_image(event.x, event.y))
        self.points.append((x, y))
        self.mouse = (event.x, event.y)
        self.redraw()

    def motion(self, event):
        if not self.points:
            return
        self.mouse = (event.x, event.y)
        self._draw_temp()

    def redraw(self):
        self.canvas.delete("preview")
        self.temp_line = None
        color = self.get_color()
        pts = [self.canvas.to_canvas(x, y) for x, y in self.points]
        r = 3
        for x, y in pts:
            self.canvas.create_oval(
                x-r, y-r, x+r, y+r,
                fill=color, tags="preview"
            )
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            self.canvas.create_line(
                x0, y0, x1, y1,
                fill=color, width=2,
                tags="preview"
            )
        self._draw_temp()

    def _draw_temp(self):
        if self.temp_line:
            self.canvas.delete(self.temp_line)
            self.temp_line = None
        if not self.points or not self.mouse:
            return
        x0, y0 = self.canvas.to_canvas(*self.points[-1])
        x1, y1 = self.mouse
        self.temp_line = self.canvas.create_line(
            x0, y0, x1, y1,
            dash=(4,2), fill=self.get_color(),
            tags="preview"
        )

    def finish(self, event):
        if len(self.points) < 3:
            self.cancel(event)
            return
        pts = [(round(x), round(y)) for x, y in self.points]
        self.cancel(event)
        img_path = self.canvas.image_path
        if img_path:
            ann = PolygonAnnotation.create(
                image_path=img_path,
                points=pts
            )
            self.on_complete(ann)

    def cancel(self, event):
        self.canvas.delete("preview")
        self.temp_line = None
        self.mouse = None
        self.points = []
