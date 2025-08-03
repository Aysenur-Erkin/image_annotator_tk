import os
import random
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

from ui.controls_frame      import ControlsFrame
from ui.canvas_widget       import CanvasWidget
from io_utils.file_manager  import FileManager
from io_utils.annotation_io import (
    save_to_json, load_from_json,
    save_to_csv,  load_from_csv
)
from annotator.tool_manager import ToolManager
from annotator.box_tool     import BoxTool
from annotator.poly_tool    import PolyTool

class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        self.master = master

        self.light_bg = "#f0f0f0"
        self.light_fg = "#000000"
        self.dark_bg  = "#2e2e2e"
        self.dark_fg  = "#ffffff"
        self.dark_mode     = False
        self.dark_mode_var = tk.BooleanVar(value=False)

        def load_icon(name):
            path = os.path.join("resources", f"{name}.png")
            img  = Image.open(path).resize((16,16), Image.LANCZOS)
            return ImageTk.PhotoImage(img)

        self.icon_open     = load_icon("open")
        self.icon_save     = load_icon("save")
        self.icon_load     = load_icon("load")
        self.icon_exit     = load_icon("exit")
        self.icon_undo     = load_icon("undo")
        self.icon_redo     = load_icon("redo")
        self.icon_box      = load_icon("box")
        self.icon_poly     = load_icon("poly")
        self.icon_darkmode = load_icon("dark_mode")

        menubar = tk.Menu(master)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(
            label="Open…", accelerator="Ctrl+O",
            command=self._on_open,
            image=self.icon_open, compound="left"
        )
        file_menu.add_command(
            label="Save", accelerator="Ctrl+S",
            command=self._on_save_annotations,
            image=self.icon_save, compound="left"
        )
        file_menu.add_command(
            label="Load", accelerator="Ctrl+L",
            command=self._on_load_annotations,
            image=self.icon_load, compound="left"
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Exit", command=master.quit,
            image=self.icon_exit, compound="left"
        )
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(
            label="Undo", accelerator="Ctrl+Z",
            command=self._on_undo,
            image=self.icon_undo, compound="left"
        )
        edit_menu.add_command(
            label="Redo", accelerator="Ctrl+Y",
            command=self._on_redo,
            image=self.icon_redo, compound="left"
        )
        menubar.add_cascade(label="Edit", menu=edit_menu)

        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(
            label="Box", accelerator="B",
            command=lambda: self._on_tool_change("box"),
            image=self.icon_box, compound="left"
        )
        tools_menu.add_command(
            label="Poly", accelerator="P",
            command=lambda: self._on_tool_change("poly"),
            image=self.icon_poly, compound="left"
        )
        menubar.add_cascade(label="Tools", menu=tools_menu)

        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_checkbutton(
            label="Dark Mode",
            variable=self.dark_mode_var,
            onvalue=True, offvalue=False,
            command=self._toggle_dark_mode,
            image=self.icon_darkmode, compound="left"
        )
        menubar.add_cascade(label="View", menu=view_menu)

        master.config(menu=menubar)

        master.bind_all("<Control-o>", lambda e: self._on_open())
        master.bind_all("<Control-s>", lambda e: self._on_save_annotations())
        master.bind_all("<Control-l>", lambda e: self._on_load_annotations())
        master.bind_all("<Control-z>", lambda e: self._on_undo())
        master.bind_all("<Control-y>", lambda e: self._on_redo())
        master.bind_all("<Control-b>", lambda e: self._on_tool_change("box"))
        master.bind_all("<Control-p>", lambda e: self._on_tool_change("poly"))

        self.labels       = ["default"]
        self.label_colors = {"default": "red"}
        self.current_label = "default"

        self.annotations = []
        self.undo_stack  = []
        self.redo_stack  = []

        self.file_manager = FileManager()

        self.controls = ControlsFrame(
            self,
            on_tool_change  = self._on_tool_change,
            on_open         = self._on_open,
            on_prev         = self._on_prev,
            on_next         = self._on_next,
            on_undo         = self._on_undo,
            on_redo         = self._on_redo,
            on_save         = self._on_save_annotations,
            on_load         = self._on_load_annotations,
            labels          = self.labels,
            on_label_change = self._on_label_change
        )
        self.controls.pack(fill=tk.X)

        self.canvas = CanvasWidget(self)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.tool_manager = ToolManager(self.canvas)
        self.tool_manager.register_tool(
            "box",
            BoxTool(
                self.canvas,
                on_complete=self._on_new_annotation,
                get_color=self._get_current_color
            )
        )
        self.tool_manager.register_tool(
            "poly",
            PolyTool(
                self.canvas,
                on_complete=self._on_new_annotation,
                get_color=self._get_current_color
            )
        )
        self.tool_manager.set_tool("box")

        self._apply_theme()


    def _toggle_dark_mode(self):
        self.dark_mode = self.dark_mode_var.get()
        self._apply_theme()


    def _apply_theme(self):
        bg = self.dark_bg if self.dark_mode else self.light_bg
        fg = self.dark_fg if self.dark_mode else self.light_fg

        self.configure(bg=bg)
        self.master.configure(bg=bg)

        self.controls.configure(bg=bg)
        for child in self.controls.winfo_children():
            try:
                child.configure(bg=bg, fg=fg)
            except:
                pass

        self.canvas.configure(bg=bg)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TCombobox",
            fieldbackground=bg,
            background=bg,
            foreground=fg
        )


    def _get_current_color(self):
        return self.label_colors.get(self.current_label, "red")


    def _generate_color(self):
        return "#%06x" % random.randint(0, 0xFFFFFF)


    def _on_label_change(self, label):
        if label not in self.labels:
            self.labels.append(label)
            self.label_colors[label] = self._generate_color()
            self.controls.combo["values"] = self.labels
        self.current_label = label


    def _on_tool_change(self, tool_name):
        self.tool_manager.set_tool(tool_name)


    def _on_open(self):
        path = filedialog.askopenfilename(
            title="Bir resim seç",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if not path:
            return
        self.canvas.load_image(path)
        folder = os.path.dirname(path)
        self.file_manager.load_folder(folder)
        try:
            self.file_manager.idx = self.file_manager.files.index(path)
        except ValueError:
            pass
        self._redraw_annotations()


    def _on_prev(self):
        path = self.file_manager.prev()
        if path:
            self.canvas.load_image(path)
            self._redraw_annotations()


    def _on_next(self):
        path = self.file_manager.next()
        if path:
            self.canvas.load_image(path)
            self._redraw_annotations()


    def _on_new_annotation(self, ann):
        ann.label = self.current_label
        ann.color = self._get_current_color()
        self.annotations.append(ann)
        self.undo_stack.append(ann)
        self.redo_stack.clear()
        self._draw_annotation(ann)


    def _draw_annotation(self, ann):
        # Draw shape
        if hasattr(ann, "points"):
            pts = ann.points
            for i in range(len(pts)):
                x0, y0 = pts[i]
                x1, y1 = pts[(i+1) % len(pts)]
                self.canvas.create_line(
                    x0, y0, x1, y1,
                    fill=ann.color, width=2,
                    tags=("annotation", ann.id)
                )
        else:
            self.canvas.create_rectangle(
                ann.x1, ann.y1, ann.x2, ann.y2,
                outline=ann.color, width=2,
                tags=("annotation", ann.id)
            )
        # Draw label
        if hasattr(ann, "points"):
            xs, ys = zip(*ann.points)
            cx, cy = sum(xs)/len(xs), sum(ys)/len(ys)
            self.canvas.create_text(
                cx, cy, text=ann.label,
                fill=ann.color, tags=("annotation", ann.id),
                font=("Arial", 12, "bold")
            )
        else:
            x, y = ann.x1, ann.y1
            self.canvas.create_text(
                x, y-5, text=ann.label,
                fill=ann.color, tags=("annotation", ann.id),
                anchor="sw", font=("Arial", 10, "bold")
            )


    def _on_undo(self):
        if not self.undo_stack:
            return
        ann = self.undo_stack.pop()
        if ann in self.annotations:
            self.annotations.remove(ann)
        self.redo_stack.append(ann)
        self.canvas.delete(ann.id)


    def _on_redo(self):
        if not self.redo_stack:
            return
        ann = self.redo_stack.pop()
        self.annotations.append(ann)
        self.undo_stack.append(ann)
        self._draw_annotation(ann)


    def _on_save_annotations(self):
        if not self.annotations:
            messagebox.showinfo("Save", "No annotations to save.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"),
                       ("CSV files", "*.csv")]
        )
        if not path:
            return
        if path.lower().endswith(".csv"):
            save_to_csv(self.annotations, path)
        else:
            save_to_json(self.annotations, path)
        messagebox.showinfo("Save", f"Annotations saved:\n{path}")


    def _on_load_annotations(self):
        path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"),
                       ("CSV files", "*.csv")]
        )
        if not path:
            return
        if path.lower().endswith(".csv"):
            anns = load_from_csv(path)
        else:
            anns = load_from_json(path)
        self.annotations = anns
        img = self.file_manager.current()
        if not img and anns:
            img = anns[0].image_path
        if img:
            self.canvas.load_image(img)
        self._redraw_annotations()
        messagebox.showinfo("Load", f"{len(anns)} Annotation loaded.")


    def _redraw_annotations(self):
        current = self.file_manager.current()
        self.canvas.delete("annotation")
        for ann in self.annotations:
            if ann.image_path != current:
                continue
            self._draw_annotation(ann)
