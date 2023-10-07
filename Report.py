import tkinter as tk
from grid_frame import GridFrame

class Report(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.max_col = 3
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

    def create_file(self):

        if len(self.empty_cells) == 0:
            self.create_grid()

        cell = self.empty_cells.pop(0)
        img = tk.PhotoImage(file='folder.png')
        img_label = tk.Label(cell, image=img, bg='lightgrey')
        img_label.image = img
        img_label.pack(padx=20, pady=20)

        self.cell_folder[cell] = img_label