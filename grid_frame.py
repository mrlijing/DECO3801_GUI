import tkinter as tk

class GridFrame(tk.Frame):
    def __init__(self, parent, max_col):
        super().__init__(parent)
        self.max_col = max_col
        self.row_no = 0
        self.col_no = 0
        self.incre_row = False

    def create_cell(self, frame):

        frame.grid(row=self.row_no, column=self.col_no)

        self.change_row_col_no()

    def change_row_col_no(self):

        self.col_no += 1
        if self.col_no == self.max_col:

            self.col_no = 0
            self.row_no += 1

            self.incre_row = True