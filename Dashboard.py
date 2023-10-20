import tkinter as tk
from PIL import Image, ImageTk
import os
from model import detect_live_camera
import threading
import argparse
import time

#Almost all work in this file is original with the exception of some very basic chatgpt promtps. These are mentioned on line 24,38 and 90
class DashboardHome(tk.Frame):
    def __init__(self, parent: tk.Frame, yolo_output_folder, num_cams=2):
        super().__init__(parent, bg='#333333')
        self.yolo_output_folder = yolo_output_folder
        self.num_cams = num_cams
        self.camera_frames = []
        self.camera_labels = []
        self.num_columns = 2
        self.create_dashboard_widgets()
        main(self.num_cams)

    def create_dashboard_widgets(self):
        self.configure(bg='#444444')  # Adjust background color for the main frame

        #prompt 1: can you improve the below text label with dark grey background and 20 font size: label = tk.Label(self, text='Dashboard Page', font=('Helvetica'), bg='white')
        label = tk.Label(self, text='Dashboard Page', font=('Helvetica', 20), bg='#444444', fg='#FFFFFF')  # Improved label
        label.pack(padx=20, pady=20)

        # Create a container frame for the camera placeholders
        camera_container = tk.Frame(self, bg='#444444')  # Improved background color
        camera_container.pack(padx=20, pady=20)

        for i in range(self.num_cams):
            # Calculate the row and column for the camera frame
            row = i // self.num_columns
            col = i % self.num_columns

            camera_frame = tk.Frame(camera_container, bg='black', width=320, height=240)
            #prompt 2: give me an example of padding rows and columns using tkinter
            camera_frame.grid(row=row, column=col, padx=10, pady=10)

            self.camera_frames.append(camera_frame)
            self.camera_labels.append(tk.Label(camera_frame))

        

        # Start a thread to update the camera images
        self.update_camera_images()

    def update_camera_images(self):
        for i, (camera_frame, camera_label) in enumerate(zip(self.camera_frames, self.camera_labels)):
            # Read the YOLO output image for each camera
            camera_output_folder = os.path.join(self.yolo_output_folder, f'cam{i}')
            image_files = [f for f in os.listdir(camera_output_folder) if f.endswith('.jpg')]

            if image_files:
                latest_image = max(image_files, key=lambda x: os.path.getctime(os.path.join(camera_output_folder, x)))
                image_path = os.path.join(camera_output_folder, latest_image)

                # Load the image and display it in the camera frame
                img = Image.open(image_path)
                img = img.resize((320, 240), Image.ADAPTIVE)
                img = ImageTk.PhotoImage(img)

                # Update the image in the existing label for the camera frame
                camera_label.configure(image=img)
                camera_label.image = img
                camera_label.pack(fill=tk.BOTH, expand=True)

        # Schedule the function to run periodically (adjust the time interval as needed)
        self.after(100, self.update_camera_images)

def setup_gui(num_cams):
    root = tk.Tk()
    yolo_output_folder = 'live'  # Change this to the correct folder path

    dashboard = DashboardHome(root, yolo_output_folder, num_cams=num_cams)
    dashboard.pack(fill=tk.BOTH, expand=True)  # Allow the widget to fill the available space

    root.title('VenueguardAI Dashboard')  # Set the dashboard title
    root.geometry("800x600")
    root.mainloop()

def main(num_cams):
    '''    parser = argparse.ArgumentParser()
    parser.add_argument('--num_cams', type=int, default=1, help='Number of cameras using')
    args = parser.parse_args()
    num_cams = args.num_cams'''

    model_threads = []
    #give me an example of threading in python
    for cam_num in range (num_cams):
        model_thread = threading.Thread(target=detect_live_camera, args=(cam_num,), daemon=True)
        model_thread.start()
        model_threads.append(model_thread)

    time.sleep(2)

    gui_thread = threading.Thread(target=setup_gui, args=(num_cams,))
    gui_thread.start()

    gui_thread.join()


#if __name__ == "__main__":
#    main()
