import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class ControlsFrame(tk.Frame):
    def __init__(self, master,
                 on_tool_change,
                 on_open, on_prev, on_next,
                 on_undo, on_redo,
                 on_save, on_load,
                 labels=None,
                 on_label_change=None):
        super().__init__(master, bd=2, relief=tk.RAISED)
        self.on_label_change = on_label_change

        def load_icon(name):
            path = os.path.join('resources', f'{name}.png')
            img = Image.open(path).resize((20,20), Image.LANCZOS)
            return ImageTk.PhotoImage(img)

        self.ic_undo = load_icon('undo')
        self.ic_redo = load_icon('redo')
        self.ic_box  = load_icon('box')
        self.ic_poly = load_icon('poly')
        self.ic_open = load_icon('open')
        self.ic_load = load_icon('load')
        self.ic_save = load_icon('save')

        btn = tk.Button(self, image=self.ic_undo, command=on_undo)
        btn.pack(side=tk.LEFT, padx=3, pady=3)
        btn = tk.Button(self, image=self.ic_redo, command=on_redo)
        btn.pack(side=tk.LEFT, padx=3, pady=3)

        btn = tk.Button(self, image=self.ic_box,
                        command=lambda: on_tool_change('box'))
        btn.pack(side=tk.LEFT, padx=3, pady=3)
        btn = tk.Button(self, image=self.ic_poly,
                        command=lambda: on_tool_change('poly'))
        btn.pack(side=tk.LEFT, padx=3, pady=3)

        btn = tk.Button(self, image=self.ic_open, command=on_open)
        btn.pack(side=tk.LEFT, padx=3, pady=3)

        btn = tk.Button(self, text='< Prev', command=on_prev)
        btn.pack(side=tk.LEFT, padx=3, pady=3)
        btn = tk.Button(self, text='Next >', command=on_next)
        btn.pack(side=tk.LEFT, padx=3, pady=3)

        btn = tk.Button(self, image=self.ic_load,
                        text=' Load JSON', compound='left', command=on_load)
        btn.pack(side=tk.LEFT, padx=3, pady=3)
        btn = tk.Button(self, image=self.ic_save,
                        text=' Save JSON', compound='left', command=on_save)
        btn.pack(side=tk.LEFT, padx=3, pady=3)

        tk.Label(self, text='Label:').pack(side=tk.RIGHT, padx=4, pady=3)
        self.label_var = tk.StringVar(value=(labels[0] if labels else 'default'))
        self.combo = ttk.Combobox(
            self,
            textvariable=self.label_var,
            values=(labels if labels else ['default']),
            state='normal',
            width=15
        )
        self.combo.pack(side=tk.RIGHT, padx=4, pady=3)
        self.combo.bind('<<ComboboxSelected>>', self._on_combo)
        self.combo.bind('<FocusOut>', self._on_combo)

    def _on_combo(self, event):
        label = self.label_var.get().strip()
        if label and self.on_label_change:
            self.on_label_change(label)
