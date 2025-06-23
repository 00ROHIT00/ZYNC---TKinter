import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk, ImageFont
import os

# Configure CustomTkinter color theme
BLACK = "#000000"
DARK_GRAY = "#1a1a1a"
LIGHT_GRAY = "#333333"
WHITE = "#ffffff"
ACCENT = "#007acc"  # A nice blue accent color

class ZyncApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("ZYNC")
        self.geometry("1000x600")

        # Set window icon
        icon_path = os.path.join("assets", "icon.png")
        try:
            icon_img = Image.open(icon_path)
            icon_photo = ImageTk.PhotoImage(icon_img)
            self.wm_iconphoto(True, icon_photo)
        except Exception as e:
            print(f"Failed to set window icon: {e}")
        
        # Set theme and colors
        ctk.set_appearance_mode("dark")
        self._set_appearance_mode("dark")
        
        # Configure window background
        self.configure(fg_color=BLACK)

        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color=DARK_GRAY)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        # Load and display logo
        logo_path = os.path.join("assets", "icon.png")
        logo_image = Image.open(logo_path)
        # Resize the image to fit nicely in the sidebar
        logo_image = logo_image.resize((160, 160), Image.Resampling.LANCZOS)
        self.logo_image = ctk.CTkImage(light_image=logo_image, dark_image=logo_image, size=(160, 160))
        
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            image=self.logo_image,
            text=""  # No text, only image
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Button style configuration
        button_config = {
            "fg_color": LIGHT_GRAY,
            "hover_color": ACCENT,
            "corner_radius": 6,
            "border_width": 0,
            "text_color": WHITE,
            "width": 160
        }

        # Sidebar buttons
        self.connect_button = ctk.CTkButton(
            self.sidebar_frame,
            text="Connect Device",
            command=self.connect_device,
            **button_config
        )
        self.connect_button.grid(row=1, column=0, padx=20, pady=10)

        self.live_scan_button = ctk.CTkButton(
            self.sidebar_frame,
            text="Live Scan",
            command=self.live_scan,
            **button_config
        )
        self.live_scan_button.grid(row=2, column=0, padx=20, pady=10)

        self.scan_logs_button = ctk.CTkButton(
            self.sidebar_frame,
            text="Scan Logs",
            command=self.scan_logs,
            **button_config
        )
        self.scan_logs_button.grid(row=3, column=0, padx=20, pady=10)

        self.export_logs_button = ctk.CTkButton(
            self.sidebar_frame,
            text="Export Logs",
            command=self.export_logs,
            **button_config
        )
        self.export_logs_button.grid(row=4, column=0, padx=20, pady=10)

        self.settings_button = ctk.CTkButton(
            self.sidebar_frame,
            text="Settings",
            command=self.open_settings,
            **button_config
        )
        self.settings_button.grid(row=5, column=0, padx=20, pady=10)

        # Main content frame
        self.main_frame = ctk.CTkFrame(self, fg_color=BLACK, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Load custom font
        try:
            font_path = os.path.join("assets", "Barlow-Black.ttf")
            custom_font = ctk.CTkFont(family="Barlow Black", size=48, weight="bold")
            if not os.path.exists(font_path):
                raise FileNotFoundError
        except:
            # Fallback to system font if custom font fails to load
            custom_font = ctk.CTkFont(size=48, weight="bold")

        # ZYNC title in main frame with custom font
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="ZYNC",
            font=custom_font,
            text_color=WHITE
        )
        self.title_label.pack(pady=20)

        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="Device Status: Not Connected",
            font=ctk.CTkFont(size=14),
            text_color=ACCENT
        )
        self.status_label.pack(pady=10)

    def connect_device(self):
        # Placeholder for connect device functionality
        self.status_label.configure(text="Device Status: Connecting...")

    def live_scan(self):
        # Placeholder for live scan functionality
        pass

    def scan_logs(self):
        # Placeholder for scan logs functionality
        pass

    def export_logs(self):
        # Placeholder for export logs functionality
        pass

    def open_settings(self):
        # Placeholder for settings functionality
        pass

if __name__ == "__main__":
    app = ZyncApp()
    app.mainloop() 