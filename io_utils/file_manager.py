import os

class FileManager:
    def __init__(self):
        self.files = []
        self.idx = -1

    def load_folder(self, folder_path):
        exts = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
        self.files = sorted([
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if f.lower().endswith(exts)
        ])
        self.idx = 0 if self.files else -1
        return self.current()

    def current(self):
        if 0 <= self.idx < len(self.files):
            return self.files[self.idx]
        return None

    def next(self):
        if self.idx < len(self.files)-1:
            self.idx += 1
        return self.current()

    def prev(self):
        if self.idx > 0:
            self.idx -= 1
        return self.current()
