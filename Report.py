import tkinter as tk
from grid_frame import GridFrame

class Report(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, borderwidth=20)
        self.max_col = 4
        self.grid = GridFrame(self, self.max_col)
        self.cell_folder = {}
        self.empty_cells = []

        self.create_grid()
        self.pack_items()

    def create_grid(self):
        for i in range(self.max_col):
            new_frame = tk.Frame(self.grid)
            self.cell_folder[new_frame] = None
            self.empty_cells.append(new_frame)
            self.grid.create_cell(new_frame)

    def pack_items(self):

        self.grid.pack(fill=tk.BOTH, expand=True)

    def create_file(self, name):

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
        folder_frame = tk.Frame(cell)

        img = tk.PhotoImage(file='folder.png')
        img_label = tk.Label(folder_frame, image=img, bg='lightgrey')
        img_label.image = img
        img_label.pack(fill=tk.X)

        name_label = tk.Label(folder_frame, bg='lightgrey', text=name)
        name_label.pack(fill=tk.X)

        folder_frame.bind("<Enter>", on_enter)
        folder_frame.bind("<Leave>", on_leave)
        folder_frame.pack(padx=20, pady=20)

        self.cell_folder[cell] = folder_frame

    def on_click(self, frame: tk.Frame):

        None