# Image annotator

I wanted a small desktop tool to mark objects on images, mostly boxes, sometimes polygons. Tkinter was enough, so there is no web UI.

You open a folder or one file, draw on the canvas, give each shape a label, and save JSON or CSV. Prev / Next walks the folder. Ctrl+Z and Ctrl+Y are undo and redo. The wheel zooms, the middle mouse pans. Dark mode is under View.

Box is drag. Polygon is a click per corner, Enter closes it, Esc drops the current one. A new label can be typed in the dropdown.

## Run

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

On Linux or mac, `source .venv/bin/activate`. The only dependency is Pillow. Tkinter comes with the Python install.

| key | |
|---|---|
| Ctrl+O | open |
| Ctrl+S | save |
| Ctrl+L | load |
| Ctrl+Z | undo |
| Ctrl+Y | redo |
| Ctrl+B | box |
| Ctrl+P | polygon |

Icons are in `resources/`. Theme colors are in `ui/main_window.py`.

MIT. See LICENSE.
