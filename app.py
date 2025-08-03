import tkinter as tk
from ui.main_window import MainWindow

def main():
    root = tk.Tk()
    root.title("Image Annotation Tool")
    root.geometry("1024x768")
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
