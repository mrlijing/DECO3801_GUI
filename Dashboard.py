import tkinter as tk
from PIL import Image, ImageTk
import os

class DashboardHome(tk.Frame):
    def __init__(self, parent: tk.Frame, yolo_output_folder):
        super().__init__(parent, bg='#333333')
        self.yolo_output_folder = yolo_output_folder
        self.camera_frames = []
        self.camera_labels = []
        self.create_dashboard_widgets()

    def create_dashboard_widgets(self):
        self.configure(bg='#444444')  # Adjust background color for the main frame

        label = tk.Label(self, text='Dashboard Page', font=('Helvetica', 20), bg='#444444', fg='#FFFFFF')  # Improved label
        label.pack(padx=20, pady=20)

        # Create a container frame for the camera placeholders
        camera_container = tk.Frame(self, bg='#444444')  # Improved background color
        camera_container.pack(padx=20, pady=20)

        # Create placeholder frames for two cameras with a black background
        for i in range(2):
            camera_frame = tk.Frame(camera_container, bg='black', width=320, height=240)
            camera_frame.pack(side=tk.LEFT, padx=10, pady=10)
            self.camera_frames.append(camera_frame)
            self.camera_labels.append(tk.Label(camera_frame))

        # You can add more widgets or customize the camera frames as needed

        # Start a thread to update the camera images
        self.update_camera_images()

    def update_camera_images(self):
        for i, (camera_frame, camera_label) in enumerate(zip(self.camera_frames, self.camera_labels)):
            # Read the YOLO output image for each camera
            camera_output_folder = os.path.join(self.yolo_output_folder, f'F{i+1}')
            image_files = [f for f in os.listdir(camera_output_folder) if f.endswith('.png')]

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
        self.after(1000, self.update_camera_images)

def main():
    root = tk.Tk()
    yolo_output_folder = 'cctv_recordings'  # Change this to the correct folder path

    dashboard = DashboardHome(root, yolo_output_folder)
    dashboard.pack(fill=tk.BOTH, expand=True)  # Allow the widget to fill the available space

    root.title('VenueguardAI Dashboard')  # Set the dashboard title
    root.geometry("800x600")
    root.mainloop()

if __name__ == "__main__":
    main()
