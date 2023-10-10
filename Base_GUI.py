import tkinter as tk
from Dashboard import DashboardHome
from Report import Report


class TopNavBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='lightgray')
        self.parent = parent
        self.current_page = None
        self.pages = {
        'Dashboard': [DashboardHome(parent, 'cctv_recordings'), 'dashboard.png'],
        'Report': [Report(parent, 'cctv_screenshots', self), 'file.png'],
        'Settings': [create_content_frame(parent, 'Settings'), 'settings.png']
        }
        self.nav_items = {}
        self.create_nav_bar()  # Create the navigation bar

    def create_nav_bar(self):
        default_page = None

        for page_name, page_items in self.pages.items():
            nav_item = tk.Frame(self, bg='lightgray', 
                                highlightbackground='gray',
                                pady=1)
            
            image = tk.PhotoImage(file=page_items[1])
            image_label = tk.Label(nav_item, text=page_name, bg='lightgray', image=image)
            image_label.image = image
            image_label.bind("<Button 1>", lambda event, p=page_name:self.show_page(p))
            image_label.pack(padx=10, fill=tk.X)
            text_label = tk.Label(nav_item, text=page_name, font=('Arial', 12), bg='lightgray')
            text_label.bind("<Button 1>", lambda event, p=page_name:self.show_page(p))
            text_label.pack(padx=10, fill=tk.X)
            
            nav_item.bind("<Button 1>", lambda event, p=page_name:self.show_page(p))
            nav_item.bind("<Enter>", lambda event, item=nav_item: self.on_hover_enter(item))
            nav_item.bind("<Leave>", lambda event, item=nav_item: self.on_hover_leave(item))
            nav_item.pack(side=tk.LEFT)
            self.nav_items[page_name] = nav_item
            
            if default_page is None:
                default_page = page_name
            

    def show_page(self, page_name):
        if self.current_page:
            self.current_page.pack_forget()

            self.nav_items[self.current_page_name].configure(bg='lightgray')

        self.current_page = self.pages[page_name][0]
        self.current_page_name = page_name
        self.current_page.pack(fill=tk.BOTH, expand=True)

        self.nav_items[page_name].configure(bg='gray')

    def on_hover_enter(self, item: tk.Frame):
        item.configure(bg='gray')

    def on_hover_leave(self, item: tk.Frame):
        if self.current_page_name != item.winfo_children()[0].cget("text"):
            item.configure(bg='lightgray')

def create_content_frame(parent: tk, page_name):
    frame = tk.Frame(parent, bg='darkgrey')
    label = tk.Label(frame, text=f'Welcome to {page_name}', font=('Helvetica', 16))
    label.pack(padx=20, pady=20)
    return frame

def main():
    
    def on_closing():
        root.destroy()

    root = tk.Tk()
    root.title('Base GUI')
    root.protocol("WM_DELETE_WINDOW", on_closing)

    heading_frame = tk.Frame(bg='#444444', height=40)
    heading_frame.pack(fill=tk.X)

        # Add a label with the application name to the heading frame
    app_name_label = tk.Label(heading_frame, text='VenueguardAI', font=('Helvetica', 20), bg='#444444')
    app_name_label.pack(side=tk.LEFT, padx=10, pady=10)
    navbar = TopNavBar(root)
    navbar.pack(fill=tk.X)
    navbar.show_page('Dashboard')

    root.geometry("800x800")
    root.mainloop()

if __name__ == "__main__":
    main()