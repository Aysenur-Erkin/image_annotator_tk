# Image annotator

Tkinter app for drawing boxes and polygons on images and saving the labels as JSON or CSV.

## Run

```bash
git clone https://github.com/Aysenur-Erkin/image_annotator_tk.git
cd image_annotator_tk
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Linux/mac: `source .venv/bin/activate`.

## Use

File, Open loads a folder or one image. Prev / Next moves through the folder. Box is click and drag. Polygon is click for each corner, Enter to close, Esc to cancel. Label comes from the dropdown, or type a new one and press Enter.

Ctrl+Z undo, Ctrl+Y redo. Wheel zooms, middle mouse pans. Save and load are in the File menu. View, Dark Mode switches the theme.

| key | |
|---|---|
| Ctrl+O | open |
| Ctrl+S | save |
| Ctrl+L | load |
| Ctrl+Z | undo |
| Ctrl+Y | redo |
| Ctrl+B | box |
| Ctrl+P | polygon |

Icons live in `resources/`. Colors are in `ui/main_window.py`.

MIT. See LICENSE.
