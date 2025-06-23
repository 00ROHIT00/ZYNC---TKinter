import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk, ImageFont
import os
import webbrowser
import sys

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

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

        # Set window icon for Windows using .ico file
        icon_ico_path = resource_path(os.path.join("assets", "icon.ico"))
        if sys.platform.startswith("win") and os.path.exists(icon_ico_path):
            try:
                self.iconbitmap(icon_ico_path)
            except Exception as e:
                print(f"Failed to set .ico icon: {e}")

        # (Optional) Set iconphoto for cross-platform support (uses PNG)
        icon_png_path = resource_path(os.path.join("assets", "icon.png"))
        if os.path.exists(icon_png_path):
            try:
                icon_img = Image.open(icon_png_path)
                icon_photo = ImageTk.PhotoImage(icon_img)
                self.wm_iconphoto(True, icon_photo)
            except Exception as e:
                print(f"Failed to set iconphoto: {e}")
        
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
        self.sidebar_frame.grid_rowconfigure(0, weight=1)
        self.sidebar_frame.grid_columnconfigure(0, weight=1)

        # Sidebar inner frame for logo and main nav buttons
        self.sidebar_inner = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.sidebar_inner.pack(side="top", fill="x", pady=(20, 0))

        # Logo
        logo_path = resource_path(os.path.join("assets", "icon.png"))
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((80, 80), Image.Resampling.LANCZOS)
        self.logo_image = ctk.CTkImage(light_image=logo_image, dark_image=logo_image, size=(80, 80))
        self.logo_label = ctk.CTkLabel(self.sidebar_inner, image=self.logo_image, text="")
        self.logo_label.pack(pady=(0, 20))

        # Button style configuration
        button_config = {
            "fg_color": LIGHT_GRAY,
            "hover_color": ACCENT,
            "corner_radius": 6,
            "border_width": 0,
            "text_color": WHITE,
            "width": 160
        }

        # Main navigation buttons in sidebar_inner
        self.connect_button = ctk.CTkButton(self.sidebar_inner, text="Connect Device", command=self.connect_device, **button_config)
        self.connect_button.pack(pady=5)
        self.live_scan_button = ctk.CTkButton(self.sidebar_inner, text="Live Scan", command=self.live_scan, **button_config)
        self.live_scan_button.pack(pady=5)
        self.scan_logs_button = ctk.CTkButton(self.sidebar_inner, text="Scan Logs", command=self.scan_logs, **button_config)
        self.scan_logs_button.pack(pady=5)
        self.export_logs_button = ctk.CTkButton(self.sidebar_inner, text="Export Logs", command=self.export_logs, **button_config)
        self.export_logs_button.pack(pady=5)
        self.settings_button = ctk.CTkButton(self.sidebar_inner, text="Settings", command=self.open_settings, **button_config)
        self.settings_button.pack(pady=5)
        self.device_info_button = ctk.CTkButton(self.sidebar_inner, text="Device Info", command=self.open_device_info, **button_config)
        self.device_info_button.pack(pady=5)
        self.terms_button = ctk.CTkButton(self.sidebar_inner, text="Terms and Conditions", command=self.open_terms, **button_config)
        self.terms_button.pack(pady=5)

        # Spacer frame to push bottom buttons down
        self.spacer = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent", height=20)
        self.spacer.pack(expand=True, fill="both")

        # Bottom buttons
        self.about_button = ctk.CTkButton(self.sidebar_frame, text="About Us", command=self.open_about, **button_config)
        self.about_button.pack(pady=5, padx=20)
        self.github_button = ctk.CTkButton(self.sidebar_frame, text="GitHub Repo", command=self.open_github, **button_config)
        self.github_button.pack(pady=(5, 20), padx=20)

        # Main content frame
        self.main_frame = ctk.CTkFrame(self, fg_color=BLACK, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Load custom font
        try:
            font_path = resource_path(os.path.join("assets", "Barlow-Black.ttf"))
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

    def open_device_info(self):
        # Placeholder for Device Info functionality
        pass

    def open_terms(self):
        # Placeholder for Terms and Conditions functionality
        pass

    def open_about(self):
        # Placeholder for About Us functionality
        pass

    def open_github(self):
        webbrowser.open_new_tab("https://github.com/yourusername/your-repo")

if __name__ == "__main__":
    app = ZyncApp()
    app.mainloop() 