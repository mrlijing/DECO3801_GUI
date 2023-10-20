import tkinter as tk
import os
from PIL import Image, ImageTk
from grid_frame import GridFrame # From custom gridframe class created
import cv2

# This class represents the "Report" section of the GUI, which is used to store video recordings 
# https://stackoverflow.com/questions/62659251/switching-frames-with-menubutton-in-python 
# This code helped me understand the structure of buttons and switching frames, along with using grids
#additionally chat GPT prompts were used for background color codes and binding processes
#prompt 1: Can you give me an example of binding a cell to perform enter and leave actions
#prompt 2: I want to set the color of various frames, can you give me the syntax of say white, black, and grey colours
class Report(tk.Frame):
    def __init__(self, parent, screenshots_folder, navbar):
        super().__init__(parent, borderwidth=20)
        self.parent = parent
        self.navbar = navbar
        self.screenshots_folder = screenshots_folder
        self.max_col = 4 #max number of columns in the grid can be 4
        self.grid = GridFrame(self, self.max_col) # Create a grid for organizing items
        self.empty_cells = [] # Store empty grid cells for adding items

        self.create_folders()
        self.pack_items()

    #to create the grid
    def create_grid(self):
        for i in range(self.max_col):
            new_frame = tk.Frame(self.grid)
            self.empty_cells.append(new_frame)
            self.grid.create_cell(new_frame)

    def pack_items(self):
        self.grid.pack(fill=tk.BOTH, expand=True) # Pack the grid to the parent frame

    def create_folder_frame(self, name):
        # Function to handle mouse hover enter event
        def on_enter(e):
            img_label.configure(cursor='hand2')
            img_label.configure(bg='white')
            name_label.configure(cursor='hand2')
            name_label.configure(bg='white')
        # Function to handle mouse hover leave event
        def on_leave(e):
            img_label.configure(bg='lightgrey')
            name_label.configure(bg='lightgrey')

        if len(self.empty_cells) == 0:
            self.create_grid()

        cell = self.empty_cells.pop(0)

        img = tk.PhotoImage(file='folder.png') # Create an image label, for showing as icon
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

    #this function creats the folders within specified path
    def create_folders(self):
        names = [entry for entry in os.listdir(self.screenshots_folder) if os.path.isdir(os.path.join(self.screenshots_folder, entry))]
        for name in names:
            self.create_folder_frame(name)

    def on_click(self, name):
        # Function to handle the "Back" button click
        def back():
            self.navbar.current_page = self
            album_frame.pack_forget()
            self.pack()

        self.pack_forget()
        album_frame = tk.Frame(self.parent)
        self.navbar.current_page = album_frame # Set the current page to the album frame
        
        top_bar = tk.Frame(album_frame, bg='darkgrey')
        
        back_button = tk.Button(top_bar, text='Back', command=back) # Create a "Back" button using in built tkinter library
        back_button.pack(side='left', padx=10)

        label = tk.Label(top_bar, text=name)
        label.pack(expand=True, fill='both')

        top_bar.pack(fill=tk.X)

        album = VideoAlbum(album_frame, name) # Create a VideoAlbum for the selected folder, the purpose is to handle mp4 files
        album.pack() # Pack the album

        album_frame.pack() # Pack the album frame

class VideoAlbum(tk.Frame):
    def __init__(self, parent, camera_name):
        super().__init__(parent, borderwidth=20)
        self.parent = parent
        self.dir = 'clips/' + camera_name# Set the directory path for video clips to be accessed from
        self.max_col = 4
        self.grid = GridFrame(self, self.max_col) # Create a grid for organizing video frames using custom grid frame function
        self.empty_cells = [] # Store empty grid cells for adding video frames

        self.grid.pack(fill=tk.BOTH, expand=True)
        self.create_videos() # Create video frames

    #To perform grid creation within video album
    def create_grid(self):
        for i in range(self.max_col):
            new_frame = tk.Frame(self.grid)
            self.empty_cells.append(new_frame)
            self.grid.create_cell(new_frame)

    def create_video_frame(self, name):
        # Function to handle mouse hover enter event
        def on_enter(e):
            video_label.configure(cursor='hand2')
            video_label.configure(bg='white')
            name_label.configure(cursor='hand2')
            name_label.configure(bg='white')

        # Function to handle mouse hover leave event
        def on_leave(e):
            video_label.configure(bg='lightgrey')
            name_label.configure(bg='lightgrey')

        if len(self.empty_cells) == 0:
            self.create_grid()

        video_dir = os.path.join(self.dir, name)#set path to video directory 
        cell = self.empty_cells.pop(0)
        is_playing = False

        def play_video():
            nonlocal is_playing #acts as global flag to check if video is playing.
            # Check if the video is not currently playing
            if not is_playing:
                # Open the video file located at previously defined video directory
                video_capture = cv2.VideoCapture(video_dir)

                # Define a function to continuously update and display video frames
                def update_frame():
                    nonlocal is_playing #local variable which acts as flag to check if video is playing
                    ret, frame = video_capture.read()# Read a single frame from the video
                    # Check if the video has reached its end
                    if not ret:
                        video_capture.release()
                        is_playing = False # Set 'is_playing' to False to stop playback, this tells is_playing variable in global scope that no video is playing
                    else:
                        # Convert the OpenCV BGR frame to RGB
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        image = Image.fromarray(frame) # Create a PIL Image from the frame
                        photo = ImageTk.PhotoImage(image=image) # Convert the PIL Image to a PhotoImage (displayable in Tkinter)

                        video_label.configure(image=photo) # Configure the video_label to display the current frame
                        video_label.image = photo
                        if is_playing:
                            video_label.after(330, update_frame)# Adjust the delay for video playback, this is used to lower frame rate

                is_playing = True
                update_frame()

        video_label = tk.Label(cell, text="Click to Play", bg='lightgrey')
        video_label.pack(fill=tk.X)
        video_label.bind("<Button-1>", lambda event: play_video())  # Bind the video playback function

        name_label = tk.Label(cell, text=name, bg='lightgrey')
        name_label.pack(fill=tk.X)

        cell.bind("<Enter>", on_enter)
        cell.bind('<Leave>', on_leave)
        cell.config(padx=20, pady=20)

    def create_videos(self):
        video_names = [entry for entry in os.listdir(self.dir) if entry.endswith('.mp4')] #handles entries with extension mp4
        for name in video_names:
            self.create_video_frame(name) # Create video frames for each video file