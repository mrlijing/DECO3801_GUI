import tkinter as tk
from grid_frame import GridFrame

class Report(tk.Frame):
    def __init__(self, parent, folder_names):
        super().__init__(parent, borderwidth=20)
        self.parent = parent
        self.folder_names = folder_names
        self.max_col = 4
        self.grid = GridFrame(self, self.max_col)
        self.empty_cells = []

        self.create_folders()
        self.pack_items()

    def create_grid(self):
        for i in range(self.max_col):
            new_frame = tk.Frame(self.grid)
            self.empty_cells.append(new_frame)
            self.grid.create_cell(new_frame)

    def pack_items(self):

        self.grid.pack(fill=tk.BOTH, expand=True)

    def create_folder_frame(self, name):

        def on_enter(e):
            img_label.configure(cursor='hand2')
            img_label.configure(bg='white')
            name_label.configure(cursor='hand2')
            name_label.configure(bg='white')

        def on_leave(e):
            img_label.configure(bg='lightgrey')
            name_label.configure(bg='lightgrey')

        if len(self.empty_cells) == 0:
            self.create_grid()

        cell = self.empty_cells.pop(0)

        img = tk.PhotoImage(file='folder.png')
        img_label = tk.Label(cell, image=img, bg='lightgrey')
        img_label.image = img
        img_label.pack(fill=tk.X)

        name_label = tk.Label(cell, bg='lightgrey', text=name)
        name_label.pack(fill=tk.X)

        cell.bind("<Enter>", on_enter)
        cell.bind("<Leave>", on_leave)
        cell.config(padx=20, pady=20)

    def create_folders(self):
        for name in self.folder_names:
            self.create_folder_frame(name)

    def on_click(self, frame: tk.Frame):

        None

class Album(tk.Frame):
    def __init__(self, parent, camera_name):
        super().__init__(parent)
        self.camera_name = camera_name
        self.max_col = 5
        self.grid = GridFrame(self, self.max_col)
        self.empty_cell = []
        self.frame_img = {}

        self.grid.pack(fill=tk.BOTH, expand=True)

    def create_grid(self):
        for i in range(self.max_col):
            new_frame = tk.Frame(self.grid)
            self.empty_cell.append(new_frame)
            self.grid.create_cell(new_frame)
            
def main():

    root = tk.Tk()

    names = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6']
    report = Report(root, names)

    report.pack()
    root.geometry("800x800")
    root.mainloop()

if __name__ == "__main__":
    main()