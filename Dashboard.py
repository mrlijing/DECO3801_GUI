import tkinter as tk

class DashboardHome(tk.Frame):
    def __init__(self, parent: tk.Frame):
        super().__init__(parent, bg='#333333')
        self.create_dashboard_widgets()

    def create_dashboard_widgets(self):
        label = tk.Label(self, text='Dashboard Page', font=('Helvetica', 16))
        label.pack(padx=20, pady=20)

        # Create a container frame for the camera placeholders
        camera_container = tk.Frame(self, bg='blue')
        camera_container.pack(padx=20, pady=20)

        # Create placeholder frames for two cameras with a black background
        camera_frame1 = tk.Frame(camera_container, bg='black', width=320, height=240)
        camera_frame1.pack(side=tk.LEFT, padx=10, pady=10)

        camera_frame2 = tk.Frame(camera_container, bg='black', width=320, height=240)
        camera_frame2.pack(side=tk.LEFT, padx=10, pady=10)

        # You can add more widgets or customize the camera frames as needed
