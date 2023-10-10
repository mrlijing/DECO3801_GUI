import tkinter as tk
import os
from PIL import Image, ImageTk
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
        img_label.bind('<Button 1>', lambda event, n=name:self.on_click(n))
        img_label.pack(fill=tk.X)

        name_label = tk.Label(cell, bg='lightgrey', text=name)
        name_label.bind('<Button 1>', lambda event, n=name:self.on_click(n))
        name_label.pack(fill=tk.X)

        cell.bind("<Enter>", on_enter)
        cell.bind("<Leave>", on_leave)
        cell.bind("<Button 1>", lambda event, n=name:self.on_click(n))
        cell.config(padx=20, pady=20)

    def create_folders(self):
        for name in self.folder_names:
            self.create_folder_frame(name)

    def on_click(self, name):

        def back():
            top_bar.pack_forget()
            album.pack_forget()
            self.pack()

        self.pack_forget()
        top_bar = tk.Frame(self.parent, bg='darkgrey')
        
        back_button = tk.Button(top_bar, text='Back', command=back)
        back_button.pack(side='left', padx=10)

        label = tk.Label(top_bar, text=name)
        label.pack(expand=True, fill='both')

        top_bar.pack(fill=tk.X)

        album = Album(self.parent, name)
        album.pack()

class Album(tk.Frame):
    def __init__(self, parent, camera_name):
        super().__init__(parent, borderwidth=20)
        self.dir = 'cctv_screenshots/' + camera_name
        self.max_col = 4
        self.grid = GridFrame(self, self.max_col)
        self.empty_cells = []
        self.frame_img = {}

        self.grid.pack(fill=tk.BOTH, expand=True)
        self.create_pics()

    def create_grid(self):
        for i in range(self.max_col):
            new_frame = tk.Frame(self.grid)
            self.empty_cells.append(new_frame)
            self.grid.create_cell(new_frame)

    def resize_img(self, img_path):
        img = Image.open(img_path)
        resized = img.resize((80, 100), Image.ADAPTIVE)
        return ImageTk.PhotoImage(resized)

    def create_pic_frame(self, name):

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
        
        pic_dir = self.dir + '/' + name
        cell = self.empty_cells.pop(0)

        img = self.resize_img(pic_dir)
        img_label = tk.Label(cell, image=img, bg='lightgrey')
        img_label.label = img
        img_label.pack(fill=tk.X)

        name_label = tk.Label(cell, text=name, bg='lightgrey')
        name_label.pack(fill=tk.X)

        cell.bind("<Enter>", on_enter)
        cell.bind('<Leave>', on_leave)
        cell.config(padx=20, pady=20)

    def create_pics(self):
        pic_names = os.listdir(self.dir)

        for name in pic_names:
            self.create_pic_frame(name)
            
def main():

    root = tk.Tk()

    folder_path = 'cctv_screenshots'

    names = [entry for entry in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, entry))]
    report = Report(root, names)

    report.pack()
    root.geometry("1200x700")
    root.mainloop()

if __name__ == "__main__":
    main()