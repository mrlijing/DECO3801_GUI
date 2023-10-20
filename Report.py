import tkinter as tk
import os
from PIL import Image, ImageTk
from grid_frame import GridFrame
import cv2

# Original Work

class Report(tk.Frame):
    def __init__(self, parent, live_folder, navbar):
        super().__init__(parent, borderwidth=20)
        self.parent = parent
        self.navbar = navbar
        self.live_folder = live_folder
        self.max_col = 4
        self.grid = GridFrame(self, self.max_col) # Create a Grid Template with 4 columns 
        self.empty_cells = []

        self.create_folders()
        self.pack_items()

    def create_grid(self):
        for i in range(self.max_col):
            new_frame = tk.Frame(self.grid) # New frame for new cell
            self.empty_cells.append(new_frame) # Add newly created cells to list of empty cells
            self.grid.create_cell(new_frame)

    def pack_items(self):
        self.grid.pack(fill=tk.BOTH, expand=True)

    def create_folder_frame(self, name):

        def on_enter(e): # Hover effects when hovering over folders
            img_label.configure(cursor='hand2')
            img_label.configure(bg='white')
            name_label.configure(cursor='hand2')
            name_label.configure(bg='white')

        def on_leave(e): # Hover effects when hovering over folders stops
            img_label.configure(bg='lightgrey')
            name_label.configure(bg='lightgrey')

        if len(self.empty_cells) == 0:
            self.create_grid()

        cell = self.empty_cells.pop(0)

        img = tk.PhotoImage(file='folder.png')
        img_label = tk.Label(cell, image=img, bg='lightgrey')
        img_label.image = img
        img_label.bind('<Button 1>', lambda event, n=name: self.on_click(n))
        img_label.pack(fill=tk.X)

        name_label = tk.Label(cell, bg='lightgrey', text=name)
        name_label.bind('<Button 1>', lambda event, n=name: self.on_click(n))
        name_label.pack(fill=tk.X)

        cell.bind("<Enter>", on_enter)
        cell.bind("<Leave>", on_leave)
        cell.bind("<Button 1>", lambda event, n=name: self.on_click(n))
        cell.config(padx=20, pady=20)

    def create_folders(self):
        # Search for folder names in "live" folder
        names = [entry for entry in os.listdir(self.live_folder) if os.path.isdir(os.path.join(self.live_folder, entry))]
        for name in names:
            self.create_folder_frame(name)

    def on_click(self, name):

        def back():
            self.navbar.current_page = self
            album_frame.pack_forget()
            self.pack()

        self.pack_forget()
        album_frame = tk.Frame(self.parent)
        self.navbar.current_page = album_frame
        
        back_button = tk.Button(album_frame, text='Back', command=back)
        back_button.pack(side=tk.LEFT, padx=10)

        label = tk.Label(album_frame, text=name)
        label.pack(expand=True, fill='both')

        album = VideoAlbum(album_frame, name, self.live_folder)
        album.pack()

        album_frame.pack()

class VideoAlbum(tk.Frame):
    def __init__(self, parent, camera_name, live_folder):
        super().__init__(parent, borderwidth=20)
        self.parent = parent
        self.dir = live_folder + '/' + camera_name
        self.max_col = 4
        self.grid = GridFrame(self, self.max_col)
        self.empty_cells = []

        self.grid.pack(fill=tk.BOTH, expand=True)
        self.create_videos()

    def create_grid(self):
        for i in range(self.max_col):
            new_frame = tk.Frame(self.grid)
            self.empty_cells.append(new_frame)
            self.grid.create_cell(new_frame)

    def create_video_frame(self, name):
        def on_enter(e):
            video_label.configure(cursor='hand2')
            video_label.configure(bg='white')
            name_label.configure(cursor='hand2')
            name_label.configure(bg='white')

        def on_leave(e):
            video_label.configure(bg='lightgrey')
            name_label.configure(bg='lightgrey')

        if len(self.empty_cells) == 0:
            self.create_grid()

        video_dir = os.path.join(self.dir, name)
        cell = self.empty_cells.pop(0)
        is_playing = False

        def play_video():
            nonlocal is_playing
            if not is_playing:
                video_capture = cv2.VideoCapture(video_dir)

                def update_frame():
                    nonlocal is_playing
                    ret, frame = video_capture.read()
                    if not ret:
                        video_capture.release()
                        is_playing = False
                    else:
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        image = Image.fromarray(frame)
                        photo = ImageTk.PhotoImage(image=image)

                        video_label.configure(image=photo)
                        video_label.image = photo
                        if is_playing:
                            video_label.after(330, update_frame)

                is_playing = True
                update_frame()

        video_label = tk.Label(cell, text="Click to Play", bg='lightgrey')
        video_label.pack(fill=tk.X)
        video_label.bind("<Button-1>", lambda event: play_video())

        name_label = tk.Label(cell, text=name, bg='lightgrey')
        name_label.pack(fill=tk.X)

        cell.bind("<Enter>", on_enter)
        cell.bind('<Leave>', on_leave)
        cell.config(padx=20, pady=20)

    def create_videos(self):
        video_names = [entry for entry in os.listdir(self.dir) if entry.endswith('.mp4')]
        for name in video_names:
            self.create_video_frame(name)
