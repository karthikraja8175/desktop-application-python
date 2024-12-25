import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  
from package.sticker import Sticker
from package.flex import Flex
from package.frame import Frame
from package.others import Others
from package.admin import Admin


class SplashScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Splash Screen")
        self.geometry("600x400")
        self.configure(bg="#474E93")
        self.overrideredirect(True)  # Remove window decorations

        # Center the splash screen on the screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (600 // 2)
        y = (screen_height // 2) - (400 // 2)
        self.geometry(f"600x400+{x}+{y}")

        # Add logo animation
        self.logo_frames = [ImageTk.PhotoImage(Image.open(f"images\\loop.png").resize((200, 200))) for i in range(1, 6)]  # Replace with your logo animation frames
        self.logo_label = tk.Label(self, bg="#474E93")
        self.logo_label.pack(pady=20)  # Add padding to position it vertically

        self.current_frame = 0
        self.animate_logo()

        # Add application name animation below the logo
        self.text_var = tk.StringVar()  # Dynamic variable for animating text
        self.app_name = "AMV2"
        self.text_index = 0  # Index to track animation progress

        self.app_name_label = tk.Label(
            self, textvariable=self.text_var,  # Bind the dynamic text variable
            font=("Arial", 24, "bold"), bg="#474E93", fg="#FFFFFF"
        )
        self.app_name_label.pack(pady=10)  # Add some spacing between logo and name
        self.animate_text()  # Start animating the app name

    def animate_logo(self):
        # Cycle through the logo frames
        self.logo_label.config(image=self.logo_frames[self.current_frame])
        self.current_frame += 1
        if self.current_frame == len(self.logo_frames):
            self.current_frame = 0
        self.after(200, self.animate_logo)  # Adjust the delay for frame speed

    def animate_text(self):
        # Animate the application name character by character
        if self.text_index < len(self.app_name):
            self.text_var.set(self.app_name[:self.text_index + 1])  # Update displayed text
            self.text_index += 1
            self.after(400, self.animate_text)  # Call again after a delay
        else:
            self.after(1900, start_main_app)  # Proceed to main app after animation ends


def start_main_app():
    """Close the splash screen and show the main app."""
    app.splash_screen.destroy()
    app.deiconify()  # Show the main application
    app.show_frame("Home")  # Show the Home frame by default


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AMV2")
        self.iconbitmap('C:\\Users\\karth\\Desktop\\nishanth\\images\\loop.ico')
        self.geometry("1500x750")
        self.configure(bg="#474E93")
        self.frames = {}  # Dictionary to store initialized frames

        # Hide the main application initially
        self.withdraw()

        # Show splash screen
        self.splash_screen = SplashScreen(self)

    def show_frame(self, name):
        """Bring the frame with the given name to the front, creating it if necessary."""
        if name not in self.frames:
            # Lazy load the frame if it hasn't been initialized
            frame_class = {
                "Home": Home,
                "Sticker": Sticker,
                "Flex": Flex,
                "Frame": Frame,
                "Others": Others,
                "Admin": Admin,
            }.get(name)

            if frame_class:
                frame = frame_class(parent=self, controller=self)
                self.frames[name] = frame
                frame.place(relwidth=1, relheight=1)

        frame = self.frames[name]
        frame.tkraise()



class CustomLabel(tk.Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Home(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#A294F9")
        self.controller = controller

        # Navigation labels
        labels = [
            ("Sticker", "Sticker"),
            ("Flex", "Flex"),
            ("Frame", "Frame"),
            ("Others", "Others"),
            ("Admin", "Admin"),
        ]

        for i, (text, frame_name) in enumerate(labels):
            label = tk.Label(
                self, text=text, font=("Arial", 35), fg="#1B1833",
                cursor="hand2", bg="#A294F9", anchor="w"
            )

            # Set label position using place
            label.place(x=100, y=150 + (i * 100))  # Adjust the x, y coordinates as needed

            # Bind the label to switch frames on click
            label.bind("<Button-1>", lambda event, name=frame_name: controller.show_frame(name))
        
        # Add the logo above the shop name
        self.logo_image = Image.open("C:\\Users\\karth\\Desktop\\nishanth\\images\\loop.png")  # Replace with your logo path
        self.logo_image = self.logo_image.resize((450, 450), Image.LANCZOS)  # Use Image.LANCZOS for resizing
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        logo_label = tk.Label(self, image=self.logo_photo, bg="#A294F9")
        logo_label.place(x=650, y=60) 

        shop_name = CustomLabel(self, text="SRI ALAGU MURUGAN \n STICKER & FLEX", bg="#A294F9", fg="#1B1833", cursor="hand2", font=("Arial", 55))
        shop_name.pack(pady=10, padx=10)
        shop_name.place(x=500, y=450)


if __name__ == "__main__":
    app = MainApp()
    app.withdraw()  # Hide the main application during the splash screen
    
    # Show splash screen
    splash_screen = SplashScreen(app)
    app.mainloop()
