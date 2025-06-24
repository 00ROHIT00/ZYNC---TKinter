import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk, ImageFont, ImageDraw
import os
import sys
import webbrowser
import json

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Settings file path
SETTINGS_FILE = resource_path("settings.json")

# Minimalist Color Scheme - Dark Theme
COLORS = {
    "dark": {
        "BG": "#111111",        # Almost black
        "SURFACE": "#181818",   # Slightly lighter black
        "ACCENT": "#32E6E2",    # Cyan
        "GRAY": "#808080",      # Medium gray
        "WHITE": "#ffffff",     # Pure white
        "HOVER": "#222222",     # Hover state
        "TEXT": "#ffffff",      # Text color
        "TEXT_SECONDARY": "#808080"  # Secondary text
    },
    "light": {
        "BG": "#F5F5F7",        # Very light gray
        "SURFACE": "#FFFFFF",   # White
        "ACCENT": "#2BA8A5",    # Darker cyan (for better contrast)
        "GRAY": "#6E6E73",      # Medium gray
        "WHITE": "#000000",     # Used for main text in light mode
        "HOVER": "#E8E8E8",     # Light gray hover
        "TEXT": "#000000",      # Text color
        "TEXT_SECONDARY": "#6E6E73"  # Secondary text
    }
}

# Initialize with dark theme
BG = COLORS["dark"]["BG"]
SURFACE = COLORS["dark"]["SURFACE"]
ACCENT = COLORS["dark"]["ACCENT"]
GRAY = COLORS["dark"]["GRAY"]
WHITE = COLORS["dark"]["WHITE"]
HOVER = COLORS["dark"]["HOVER"]

def create_icon(icon_type):
    """Create a simple icon using PIL drawing."""
    size = (32, 32)
    image = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    if icon_type == "connect":
        # Draw a circle with a dot in the center
        draw.ellipse([4, 4, 28, 28], outline=ACCENT, width=2)
        draw.ellipse([12, 12, 20, 20], fill=ACCENT)
    elif icon_type == "scan":
        # Draw a document with scan lines
        draw.rectangle([6, 4, 26, 28], outline=ACCENT, width=2)
        draw.line([10, 12, 22, 12], fill=ACCENT, width=2)
        draw.line([10, 16, 22, 16], fill=ACCENT, width=2)
        draw.line([10, 20, 22, 20], fill=ACCENT, width=2)
    elif icon_type == "logs":
        # Draw a document with text lines
        draw.rectangle([6, 4, 26, 28], outline=ACCENT, width=2)
        draw.line([10, 12, 22, 12], fill=ACCENT, width=2)
        draw.line([10, 16, 22, 16], fill=ACCENT, width=2)
        draw.line([10, 20, 18, 20], fill=ACCENT, width=2)
    elif icon_type == "export":
        # Draw an up arrow
        draw.rectangle([6, 4, 26, 28], outline=ACCENT, width=2)
        points = [(16, 8), (10, 16), (22, 16)]  # Arrow head
        draw.polygon(points, fill=ACCENT)
        draw.line([16, 14, 16, 24], fill=ACCENT, width=2)  # Arrow stem
    
    return image

class ZyncApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Load saved settings or use defaults
        self.settings = self.load_settings()
        
        # Initialize settings with saved values
        self.current_theme = self.settings.get("theme", "Dark")
        self.current_font_size = self.settings.get("font_size", "Medium")
        self.font_sizes = {
            "Small": {
                "title": 20,
                "header": 16,
                "normal": 12,
                "small": 11
            },
            "Medium": {
                "title": 24,
                "header": 18,
                "normal": 14,
                "small": 13
            },
            "Large": {
                "title": 28,
                "header": 20,
                "normal": 16,
                "small": 15
            }
        }

        # Load both light and dark logos
        self.load_logos()

        # Set theme before creating any widgets
        self.apply_theme(self.current_theme, save_settings=False)

        # Configure window
        self.title("ZYNC")
        self.geometry("1920x1080")
        
        # Center the window on screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 1920
        window_height = 1080
        
        # Calculate position x and y coordinates
        x = (screen_width/2) - (window_width/2)
        y = (screen_height/2) - (window_height/2)
        self.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")
        
        # Set window icon based on theme
        self.update_window_icon()

        # Create main layout
        self.setup_layout()

    def load_settings(self):
        """Load settings from file"""
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading settings: {e}")
        return {}  # Return empty dict if no settings or error

    def save_settings(self):
        """Save current settings to file"""
        settings = {
            "theme": self.current_theme,
            "font_size": self.current_font_size
        }
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def load_logos(self):
        """Load both light and dark versions of the logo"""
        # Load dark logo (white)
        dark_logo_path = resource_path(os.path.join("assets", "icon.png"))
        dark_logo_image = Image.open(dark_logo_path)
        dark_logo_image = dark_logo_image.resize((40, 40), Image.Resampling.LANCZOS)
        self.dark_logo = ctk.CTkImage(light_image=dark_logo_image, dark_image=dark_logo_image, size=(40, 40))

        # Load light logo (black)
        light_logo_path = resource_path(os.path.join("assets", "black.png"))
        light_logo_image = Image.open(light_logo_path)
        light_logo_image = light_logo_image.resize((40, 40), Image.Resampling.LANCZOS)
        self.light_logo = ctk.CTkImage(light_image=light_logo_image, dark_image=light_logo_image, size=(40, 40))

    def update_window_icon(self):
        """Update the window icon based on current theme"""
        icon_path = resource_path(os.path.join("assets", 
            "black.ico" if self.current_theme == "Light" else "icon.ico"))
        if sys.platform.startswith("win") and os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception as e:
                print(f"Failed to set .ico icon: {e}")

    def apply_theme(self, theme, save_settings=True):
        """Apply the selected theme and optionally save settings"""
        self.current_theme = theme
        if theme == "System":
            # Try to detect system theme
            try:
                import darkdetect
                theme = "Dark" if darkdetect.isDark() else "Light"
            except ImportError:
                theme = "Dark"  # Default to Dark if can't detect

        # Update global color variables
        theme_lower = theme.lower()
        global BG, SURFACE, ACCENT, GRAY, WHITE, HOVER
        BG = COLORS[theme_lower]["BG"]
        SURFACE = COLORS[theme_lower]["SURFACE"]
        ACCENT = COLORS[theme_lower]["ACCENT"]
        GRAY = COLORS[theme_lower]["GRAY"]
        WHITE = COLORS[theme_lower]["WHITE"]
        HOVER = COLORS[theme_lower]["HOVER"]
        
        # Apply theme to CustomTkinter
        if theme == "Light":
            ctk.set_appearance_mode("light")
            self._set_appearance_mode("light")
        else:  # Dark theme
            ctk.set_appearance_mode("dark")
            self._set_appearance_mode("dark")
            
        # Update the colors of existing widgets
        self.configure(fg_color=BG)
        if hasattr(self, 'container'):
            self.container.configure(fg_color=BG)
            self._update_widget_colors(self.container)
            
        # Update logo if it exists
        if hasattr(self, 'logo_label'):
            self.logo_label.configure(
                image=self.light_logo if theme == "Light" else self.dark_logo
            )
            
        # Update window icon
        self.update_window_icon()
            
        # Save settings if requested
        if save_settings:
            self.save_settings()

    def _update_widget_colors(self, widget):
        """Recursively update colors of all widgets"""
        theme_lower = self.current_theme.lower()
        
        try:
            if isinstance(widget, ctk.CTkFrame):
                current_color = widget.cget("fg_color")
                if current_color in [COLORS["dark"]["SURFACE"], COLORS["light"]["SURFACE"]]:
                    widget.configure(fg_color=SURFACE)
                elif current_color in [COLORS["dark"]["BG"], COLORS["light"]["BG"], "transparent"]:
                    widget.configure(fg_color=BG if current_color != "transparent" else "transparent")
                    
            elif isinstance(widget, ctk.CTkLabel):
                current_color = widget.cget("text_color")
                if current_color in [COLORS["dark"]["WHITE"], COLORS["light"]["WHITE"]]:
                    widget.configure(text_color=WHITE)
                elif current_color in [COLORS["dark"]["GRAY"], COLORS["light"]["GRAY"]]:
                    widget.configure(text_color=GRAY)
                elif current_color in [COLORS["dark"]["ACCENT"], COLORS["light"]["ACCENT"]]:
                    widget.configure(text_color=ACCENT)
                    
            elif isinstance(widget, ctk.CTkButton):
                current_color = widget.cget("fg_color")
                if current_color in [COLORS["dark"]["SURFACE"], COLORS["light"]["SURFACE"]]:
                    widget.configure(
                        fg_color=SURFACE,
                        hover_color=HOVER,
                        text_color=WHITE
                    )
                elif current_color == ACCENT:
                    widget.configure(
                        hover_color="#2BC4C1" if theme_lower == "dark" else "#248F8C"
                    )
                    
            elif isinstance(widget, ctk.CTkOptionMenu):
                widget.configure(
                    fg_color=SURFACE,
                    button_color=ACCENT,
                    button_hover_color=HOVER,
                    text_color=WHITE
                )
                
            elif isinstance(widget, ctk.CTkSwitch):
                widget.configure(
                    progress_color=ACCENT,
                    button_color=WHITE,
                    button_hover_color=GRAY,
                    fg_color=SURFACE
                )
                
            elif isinstance(widget, ctk.CTkScrollableFrame):
                widget.configure(fg_color="transparent")
                
        except Exception as e:
            print(f"Error updating widget colors: {e}")
            
        # Recursively update child widgets
        for child in widget.winfo_children():
            self._update_widget_colors(child)

    def apply_font_size(self, size, save_settings=True):
        """Apply the selected font size and optionally save settings"""
        self.current_font_size = size
        sizes = self.font_sizes[size]
        
        # Update all text elements that exist
        if hasattr(self, 'content_frame'):
            # Recursively update all labels and buttons
            self._update_widget_fonts(self)
            
        # Store the size for new elements
        self.current_font_sizes = sizes
        
        # Save settings if requested
        if save_settings:
            self.save_settings()

    def _update_widget_fonts(self, widget):
        """Recursively update fonts of all widgets"""
        sizes = self.font_sizes[self.current_font_size]
        
        if isinstance(widget, ctk.CTkLabel):
            # Determine the font size based on the widget's role
            if widget.cget("text") == "ZYNC":  # Main title
                widget.configure(font=ctk.CTkFont(size=sizes["title"], weight="bold"))
            elif widget.cget("text") == "SETTINGS":  # Page header
                widget.configure(font=ctk.CTkFont(size=sizes["title"], weight="bold"))
            elif widget.cget("text") in ["General", "Scan Settings", "Export Settings", "Developer Options (ADVANCED)"]:  # Section headers
                widget.configure(font=ctk.CTkFont(size=sizes["header"], weight="bold"))
            else:  # Normal text
                current_font = widget.cget("font")
                is_bold = current_font.weight == "bold" if hasattr(current_font, 'weight') else False
                widget.configure(font=ctk.CTkFont(size=sizes["normal"], weight="bold" if is_bold else "normal"))
        
        elif isinstance(widget, ctk.CTkButton):
            widget.configure(font=ctk.CTkFont(size=sizes["normal"]))
        
        elif isinstance(widget, ctk.CTkOptionMenu):
            widget.configure(font=ctk.CTkFont(size=sizes["normal"]))
        
        # Recursively update child widgets
        for child in widget.winfo_children():
            self._update_widget_fonts(child)

    def setup_layout(self):
        # Main container
        self.container = ctk.CTkFrame(self, fg_color=BG)
        self.container.pack(expand=True, fill="both", padx=40, pady=30)

        # Top bar with logo and status
        self.top_bar = self.create_top_bar()
        
        # Content frame that will switch between views
        self.content_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.content_frame.pack(expand=True, fill="both")
        
        # Bottom bar with utilities
        self.bottom_bar = self.create_bottom_bar()
        
        # Initially show the action grid
        self.show_action_grid()

    def create_top_bar(self):
        # Top bar container
        top_bar = ctk.CTkFrame(self.container, fg_color="transparent", height=80)
        top_bar.pack(fill="x", pady=(0, 40))
        top_bar.pack_propagate(False)

        # Left side - Logo and title
        logo_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        logo_frame.pack(side="left", fill="y")

        # Logo label (will be updated with theme changes)
        self.logo_label = ctk.CTkLabel(
            logo_frame,
            image=self.dark_logo if self.current_theme == "Dark" else self.light_logo,
            text=""
        )
        self.logo_label.pack(side="left")

        # Title with custom font
        try:
            font_path = resource_path(os.path.join("assets", "Barlow-Black.ttf"))
            title_font = ctk.CTkFont(family="Barlow Black", size=24, weight="bold")
        except:
            title_font = ctk.CTkFont(size=24, weight="bold")

        title_label = ctk.CTkLabel(
            logo_frame,
            text="ZYNC",
            font=title_font,
            text_color=WHITE
        )
        title_label.pack(side="left", padx=15)

        # Right side - Status
        self.status_label = ctk.CTkLabel(
            top_bar,
            text="●  Not Connected",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=GRAY
        )
        self.status_label.pack(side="right", padx=10)

        return top_bar

    def create_bottom_bar(self):
        # Bottom utilities bar
        bottom_frame = ctk.CTkFrame(self.container, fg_color="transparent", height=50)
        bottom_frame.pack(fill="x", pady=(20, 0))
        bottom_frame.pack_propagate(False)

        # Utility buttons configuration
        button_config = {
            "fg_color": "transparent",
            "hover_color": "#1A1A1A",  # Very subtle dark hover color
            "text_color": GRAY,
            "font": ctk.CTkFont(size=14, weight="bold"),
            "height": 32,
            "corner_radius": 6
        }

        # Left side buttons
        left_frame = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        left_frame.pack(side="left")

        utilities = [
            ("Settings", self.open_settings),
            ("Device Info", self.open_device_info),
            ("Terms & Conditions", self.open_terms)
        ]

        for text, command in utilities:
            btn = ctk.CTkButton(left_frame, text=text, command=command, **button_config)
            btn.pack(side="left", padx=5)
            # Add hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.configure(text_color=WHITE))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(text_color=GRAY))

        # Right side buttons
        right_frame = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        right_frame.pack(side="right")

        about_btn = ctk.CTkButton(right_frame, text="About", command=self.open_about, **button_config)
        about_btn.pack(side="left", padx=5)
        about_btn.bind("<Enter>", lambda e: about_btn.configure(text_color=WHITE))
        about_btn.bind("<Leave>", lambda e: about_btn.configure(text_color=GRAY))

        github_btn = ctk.CTkButton(right_frame, text="GitHub", command=self.open_github, **button_config)
        github_btn.pack(side="left", padx=5)
        github_btn.bind("<Enter>", lambda e: github_btn.configure(text_color=WHITE))
        github_btn.bind("<Leave>", lambda e: github_btn.configure(text_color=GRAY))

        return bottom_frame

    def show_action_grid(self):
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Show dashboard bars in correct order
        self.top_bar.pack(in_=self.container, fill="x", pady=(0, 40), after=None)
        self.content_frame.pack(in_=self.container, expand=True, fill="both", after=self.top_bar)
        self.bottom_bar.pack(in_=self.container, fill="x", pady=(20, 0), after=self.content_frame)
        
        # Main actions grid
        actions_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        actions_frame.pack(expand=True, fill="both", pady=20)

        # Configure grid weights
        actions_frame.grid_columnconfigure((0, 1), weight=1, uniform="column")
        actions_frame.grid_rowconfigure((0, 1), weight=1, uniform="row")

        # Action buttons with icons
        actions = [
            ("Connect Device", "Connect to your device", "connect", 0, 0),
            ("Live Scan", "Real-time scanning", "scan", 0, 1),
            ("Scan Logs", "View scan history", "logs", 1, 0),
            ("Export Logs", "Export data", "export", 1, 1)
        ]

        # Create icons
        self.icons = {}
        for _, _, icon_name, _, _ in actions:
            icon_image = create_icon(icon_name)
            self.icons[icon_name] = ctk.CTkImage(light_image=icon_image, dark_image=icon_image, size=(32, 32))

        for text, desc, icon_name, row, col in actions:
            self.create_action_button(actions_frame, text, desc, icon_name, row, col)

    def create_action_button(self, parent, text, description, icon_name, row, col):
        # Button frame with hover effect
        frame = ctk.CTkFrame(parent, fg_color=SURFACE, corner_radius=15)
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        # Bind click and hover events to the frame
        command_map = {
            "Connect Device": self.connect_device,
            "Live Scan": self.live_scan,
            "Scan Logs": self.scan_logs,
            "Export Logs": self.export_logs
        }
        
        command = command_map.get(text, lambda: None)
        
        frame.bind("<Button-1>", lambda e: command())
        frame.bind("<Enter>", lambda e: frame.configure(fg_color=HOVER))
        frame.bind("<Leave>", lambda e: frame.configure(fg_color=SURFACE))

        # Make frame clickable by changing cursor
        frame.configure(cursor="hand2")

        # Center content
        content = ctk.CTkFrame(frame, fg_color="transparent")
        content.place(relx=0.5, rely=0.5, anchor="center")

        # Make content clickable too
        content.bind("<Button-1>", lambda e: command())
        content.configure(cursor="hand2")

        # Icon
        if icon_name in self.icons:
            icon_label = ctk.CTkLabel(content, image=self.icons[icon_name], text="")
            icon_label.pack(pady=(0, 10))
            icon_label.bind("<Button-1>", lambda e: command())
            icon_label.configure(cursor="hand2")

        # Title
        title = ctk.CTkLabel(
            content,
            text=text,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=WHITE
        )
        title.pack()
        title.bind("<Button-1>", lambda e: command())
        title.configure(cursor="hand2")

        # Description
        desc = ctk.CTkLabel(
            content,
            text=description,
            font=ctk.CTkFont(size=14),
            text_color=GRAY
        )
        desc.pack(pady=(5, 0))
        desc.bind("<Button-1>", lambda e: command())
        desc.configure(cursor="hand2")

    def connect_device(self):
        self.status_label.configure(text="●  Connecting...", text_color=ACCENT)

    def live_scan(self):
        pass

    def scan_logs(self):
        pass

    def export_logs(self):
        pass

    def open_settings(self):
        self.show_settings()

    def open_device_info(self):
        self.show_device_info()

    def open_terms(self):
        terms_window = ctk.CTkToplevel(self)
        terms_window.title("Terms and Conditions")
        terms_window.geometry("700x600")
        terms_window.resizable(False, False)
        terms_window.configure(fg_color=BG)
        
        # Set window icon
        icon_ico_path = resource_path(os.path.join("assets", "icon.ico"))
        if sys.platform.startswith("win") and os.path.exists(icon_ico_path):
            try:
                terms_window.iconbitmap(icon_ico_path)
            except Exception as e:
                print(f"Failed to set .ico icon for Terms window: {e}")
        
        # Make the window modal
        terms_window.transient(self)
        terms_window.grab_set()
        
        # Center the window relative to the main window
        x = self.winfo_x() + (self.winfo_width() - 700) // 2
        y = self.winfo_y() + (self.winfo_height() - 600) // 2
        terms_window.geometry(f"+{x}+{y}")
        
        # Main container
        container = ctk.CTkFrame(terms_window, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=30, pady=30)
        
        # Title
        title = ctk.CTkLabel(
            container,
            text="Terms and Conditions",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=WHITE
        )
        title.pack(pady=(0, 5))
        
        # Last updated
        last_updated = ctk.CTkLabel(
            container,
            text="Last updated: June, 2025",
            font=ctk.CTkFont(size=12),
            text_color=GRAY
        )
        last_updated.pack(pady=(0, 20))
        
        # Create scrollable frame
        scrollable_frame = ctk.CTkScrollableFrame(
            container,
            fg_color=SURFACE,
            corner_radius=10
        )
        scrollable_frame.pack(expand=True, fill="both")
        
        # Terms content
        terms_text = """Welcome to ZYNC — your personal portable WiFi security scanner.

By using the ZYNC mobile application and hardware device (collectively referred to as the "Service"), you agree to the following Terms and Conditions. Please read them carefully.

1. Acceptance of Terms

By accessing or using ZYNC, you confirm that you have read, understood, and agree to be bound by these Terms. If you do not agree, do not use the app or device.

2. Description of Service

ZYNC allows users to:

    • Scan nearby WiFi networks using a portable device.
    • Display details such as SSID, encryption type, and potential risks.
    • Connect the device to the mobile app via Bluetooth to view live scan data.
    • Store and view scan logs through the mobile app.

The app and device are intended to inform and assist users in identifying potentially insecure WiFi connections. It does not interfere, tamper with, or access any network content.

3. User Responsibility

You agree to use ZYNC only for lawful purposes. You shall not:

    • Attempt unauthorized access to networks.
    • Use the device/app for hacking, eavesdropping, or packet sniffing.
    • Share inaccurate or misleading scan data.

ZYNC is a passive scanner — it does not connect to any network without user consent.

4. Data Collection and Privacy

ZYNC may collect:

    • Scan metadata (SSID, signal strength, encryption type).
    • Device information (non-personally identifiable).
    • App usage statistics (for performance improvements).

All data remains local to the user's device unless manually exported. ZYNC does not share your data with third parties.

5. No Warranty

ZYNC is provided on an "as-is" basis. We do not guarantee:

    • The accuracy or completeness of scan results.
    • That all security threats will be detected.
    • Uninterrupted or error-free operation.

You are solely responsible for how you act based on scan data.

6. Limitation of Liability

In no event shall ZYNC, its developers, or affiliates be liable for:

    • Any damage caused by reliance on scan results.
    • Loss of data, network issues, or unauthorized access.
    • Any indirect or consequential losses.

7. Modifications to Terms

We reserve the right to update these Terms at any time. Continued use of the app or device after changes means you accept the updated terms.

8. Contact Us

For questions or support, please contact:
📧 zync@example.com
🌐 zync.com"""

        terms_label = ctk.CTkLabel(
            scrollable_frame,
            text=terms_text,
            font=ctk.CTkFont(size=14),
            text_color=WHITE,
            justify="left",
            wraplength=600
        )
        terms_label.pack(padx=20, pady=20)
        
        # Close button
        close_button = ctk.CTkButton(
            container,
            text="Close",
            command=terms_window.destroy,
            fg_color=SURFACE,
            hover_color=HOVER,
            text_color=WHITE,
            height=32,
            width=100
        )
        close_button.pack(pady=(20, 0))

    def open_about(self):
        about_window = ctk.CTkToplevel(self)
        about_window.title("About ZYNC")
        about_window.geometry("500x450")
        about_window.resizable(False, False)
        about_window.configure(fg_color=BG)
        
        # Set window icon
        icon_ico_path = resource_path(os.path.join("assets", "icon.ico"))
        if sys.platform.startswith("win") and os.path.exists(icon_ico_path):
            try:
                about_window.iconbitmap(icon_ico_path)
            except Exception as e:
                print(f"Failed to set .ico icon for About window: {e}")
        
        # Make the window modal
        about_window.transient(self)
        about_window.grab_set()
        
        # Center the window relative to the main window
        x = self.winfo_x() + (self.winfo_width() - 500) // 2
        y = self.winfo_y() + (self.winfo_height() - 450) // 2
        about_window.geometry(f"+{x}+{y}")
        
        # Content frame
        content_frame = ctk.CTkFrame(about_window, fg_color="transparent")
        content_frame.pack(expand=True, fill="both", padx=30, pady=30)
        
        # Logo and title frame
        logo_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        logo_frame.pack(fill="x", pady=(0, 20))
        
        # Logo
        logo_label = ctk.CTkLabel(logo_frame, image=self.logo_label, text="")
        logo_label.pack(side="left")
        
        # Title with custom font
        try:
            title_font = ctk.CTkFont(family="Barlow Black", size=24, weight="bold")
        except:
            title_font = ctk.CTkFont(size=24, weight="bold")
            
        title_label = ctk.CTkLabel(
            logo_frame,
            text="ZYNC",
            font=title_font,
            text_color=WHITE
        )
        title_label.pack(side="left", padx=15)
        
        # Description
        description = ctk.CTkLabel(
            content_frame,
            text="ZYNC is your personal portable WiFi security scanner, designed to help you identify "
                 "and assess the security of wireless networks around you. Our mission is to make network "
                 "security accessible and understandable for everyone.",
            font=ctk.CTkFont(size=14),
            text_color=WHITE,
            wraplength=440,
            justify="left"
        )
        description.pack(pady=(0, 20))
        
        # Features title
        features_title = ctk.CTkLabel(
            content_frame,
            text="Features:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=WHITE
        )
        features_title.pack(anchor="w", pady=(0, 10))
        
        # Features list
        features = [
            "Real-time WiFi network scanning",
            "Detailed Security Analysis",
            "User-friendly Interface",
            "Portable Hardware Device",
            "Comprehensive Scan Logs"
        ]
        
        for feature in features:
            feature_label = ctk.CTkLabel(
                content_frame,
                text=f"• {feature}",
                font=ctk.CTkFont(size=14),
                text_color=GRAY,
                justify="left"
            )
            feature_label.pack(anchor="w", pady=2)
        
        # Close button
        close_button = ctk.CTkButton(
            content_frame,
            text="Close",
            command=about_window.destroy,
            fg_color=SURFACE,
            hover_color=HOVER,
            text_color=WHITE,
            height=32,
            width=100
        )
        close_button.pack(pady=(20, 0))

    def open_github(self):
        # Create warning dialog
        warning_window = ctk.CTkToplevel(self)
        warning_window.title("External Link")
        warning_window.geometry("450x250")
        warning_window.resizable(False, False)
        warning_window.configure(fg_color=BG)
        
        # Set window icon
        icon_ico_path = resource_path(os.path.join("assets", "icon.ico"))
        if sys.platform.startswith("win") and os.path.exists(icon_ico_path):
            try:
                warning_window.iconbitmap(icon_ico_path)
            except Exception as e:
                print(f"Failed to set .ico icon for warning window: {e}")
        
        # Make the window modal
        warning_window.transient(self)
        warning_window.grab_set()
        
        # Center the window relative to the main window
        x = self.winfo_x() + (self.winfo_width() - 450) // 2
        y = self.winfo_y() + (self.winfo_height() - 250) // 2
        warning_window.geometry(f"+{x}+{y}")
        
        # Container
        container = ctk.CTkFrame(warning_window, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=30, pady=30)
        
        # Warning icon (⚠️) and title
        title = ctk.CTkLabel(
            container,
            text="⚠️ External Website",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=ACCENT
        )
        title.pack(pady=(0, 15))
        
        # Warning message
        message = ctk.CTkLabel(
            container,
            text="You are about to be redirected to an external website:\n\nhttps://github.com/00ROHIT00/ZYNC---TKinter\n\nExternal websites are not operated by ZYNC.\nProceed with caution.",
            font=ctk.CTkFont(size=14),
            text_color=WHITE,
            justify="center",
            wraplength=350
        )
        message.pack(pady=(0, 20))
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(container, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        # Cancel button
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            command=warning_window.destroy,
            fg_color=SURFACE,
            hover_color=HOVER,
            text_color=WHITE,
            height=32,
            width=100
        )
        cancel_button.pack(side="left", padx=5)
        
        # Continue button
        def on_continue():
            warning_window.destroy()
            webbrowser.open("https://github.com/00ROHIT00/ZYNC---TKinter")
            
        continue_button = ctk.CTkButton(
            buttons_frame,
            text="Continue",
            command=on_continue,
            fg_color=ACCENT,
            hover_color="#2BC4C1",  # Slightly darker shade of ACCENT
            text_color=BG,
            height=32,
            width=100
        )
        continue_button.pack(side="right", padx=5)

    def show_device_info(self):
        # Hide dashboard bars
        self.top_bar.pack_forget()
        self.bottom_bar.pack_forget()
        
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Main container without padding to use full space
        main_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        main_container.pack(expand=True, fill="both")
        
        # Header
        header_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=30)

        # Back button
        back_button = ctk.CTkButton(
            header_frame,
            text="← Back",
            command=self.show_action_grid,
            fg_color=SURFACE,
            hover_color=HOVER,
            text_color=WHITE,
            height=32,
            width=100
        )
        back_button.pack(side="left")
        
        header_title = ctk.CTkLabel(
            header_frame,
            text="Device Information",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=WHITE
        )
        header_title.pack(side="left", padx=20)
        
        # Status indicator
        status_frame = ctk.CTkFrame(header_frame, fg_color=SURFACE, corner_radius=10)
        status_frame.pack(side="right")
        
        status_dot = ctk.CTkLabel(
            status_frame,
            text="●",
            font=ctk.CTkFont(size=20),
            text_color=ACCENT
        )
        status_dot.pack(side="left", padx=(15, 5), pady=8)
        
        status_text = ctk.CTkLabel(
            status_frame,
            text="Connected",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=WHITE
        )
        status_text.pack(side="left", padx=(0, 15), pady=8)
        
        # Content area with sections - now using full width
        content_frame = ctk.CTkFrame(main_container, fg_color=SURFACE, corner_radius=15)
        content_frame.pack(expand=True, fill="both", padx=40, pady=(0, 30))
        
        # Left column (60% width)
        left_col = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_col.pack(side="left", fill="both", expand=True, padx=25, pady=25)
        
        # Device basics section
        self.create_info_section(left_col, "Device Details", [
            ("Device Name", "ZYNC-001"),
            ("Board Model", "ZYNC-V2"),
            ("Firmware Version", "v1.2.3"),
            ("Screen Type", "OLED 128x64")
        ])
        
        # Connection section
        self.create_info_section(left_col, "Connection", [
            ("Connection Type", "Bluetooth"),
            ("Bluetooth MAC", "00:11:22:33:44:55"),
            ("Last Connected", "2024-03-15 14:30")
        ])
        
        # Vertical separator
        separator = ctk.CTkFrame(content_frame, fg_color=GRAY, width=1)
        separator.pack(side="left", fill="y", padx=0, pady=35)
        
        # Right column (40% width)
        right_col = ctk.CTkFrame(content_frame, fg_color="transparent")
        right_col.pack(side="left", fill="both", padx=25, pady=25)
        
        # Power section
        self.create_info_section(right_col, "Power Status", [
            ("Battery Level", "85%"),
            ("Charging Status", "Not Charging"),
            ("Voltage", "3.7V")
        ])
        
        # Statistics section
        self.create_info_section(right_col, "Statistics", [
            ("Uptime", "5h 23m"),
            ("Last Scan", "2024-03-15 14:25"),
            ("Total Scans Done", "127")
        ])

    def create_info_section(self, parent, title, items):
        # Section container
        section = ctk.CTkFrame(parent, fg_color="transparent")
        section.pack(fill="x", pady=(0, 25))
        
        # Section title
        title_label = ctk.CTkLabel(
            section,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=ACCENT
        )
        title_label.pack(anchor="w", pady=(0, 15))
        
        # Items
        for key, value in items:
            item_frame = ctk.CTkFrame(section, fg_color=BG, corner_radius=8, height=36)
            item_frame.pack(fill="x", pady=4)
            item_frame.pack_propagate(False)
            
            key_label = ctk.CTkLabel(
                item_frame,
                text=key,
                font=ctk.CTkFont(size=13),
                text_color=GRAY,
                anchor="w"
            )
            key_label.pack(side="left", padx=15)
            
            value_label = ctk.CTkLabel(
                item_frame,
                text=value,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=WHITE,
                anchor="e"
            )
            value_label.pack(side="right", padx=15)

    def show_settings(self):
        # Hide dashboard bars
        self.top_bar.pack_forget()
        self.bottom_bar.pack_forget()
        
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Main container without padding to use full space
        main_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        main_container.pack(expand=True, fill="both")
        
        # Header
        header_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=30)

        # Back button
        back_button = ctk.CTkButton(
            header_frame,
            text="← Back",
            command=self.show_action_grid,
            fg_color=SURFACE,
            hover_color=HOVER,
            text_color=WHITE,
            height=32,
            width=100
        )
        back_button.pack(side="left")
        
        # Title (centered)
        header_title = ctk.CTkLabel(
            header_frame,
            text="SETTINGS",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=WHITE
        )
        header_title.pack(expand=True, pady=(0, 0))
        
        # Settings content
        content_frame = ctk.CTkFrame(main_container, fg_color=SURFACE, corner_radius=15)
        content_frame.pack(expand=True, fill="both", padx=40, pady=(0, 30))
        
        # Settings sections container with scrolling
        settings_container = ctk.CTkScrollableFrame(
            content_frame,
            fg_color="transparent",
            corner_radius=0
        )
        settings_container.pack(expand=True, fill="both", padx=25, pady=25)

        # General Settings
        self.create_settings_section(settings_container, "General", [
            ("App Theme", "dropdown", ["Dark", "Light", "System"]),
            ("Font Size", "dropdown", ["Small", "Medium", "Large"]),
            ("Default Save Path", "path", "Browse...")
        ])
        
        # Scan Settings
        self.create_settings_section(settings_container, "Scan Settings", [
            ("Scan Interval", "dropdown", ["5s", "10s", "30s", "1m", "5m"]),
            ("Scan Depth", "dropdown", ["Basic", "Standard", "Deep"]),
            ("Ignore Duplicate SSIDs", "switch", None),
            ("Alert for Insecure WiFi", "switch", None)
        ])
        
        # Export Settings
        self.create_settings_section(settings_container, "Export Settings", [
            ("Log Format", "dropdown", ["TXT", "CSV", "JSON"]),
            ("Include Device Info in Logs", "switch", None)
        ])
        
        # Developer Options
        self.create_settings_section(settings_container, "Developer Options (ADVANCED)", [
            ("Verbose Scan Output", "switch", None),
            ("Test Bluetooth Connection", "button", "Test")
        ])

    def create_settings_section(self, parent, title, settings):
        # Section container
        section = ctk.CTkFrame(parent, fg_color="transparent")
        section.pack(fill="x", pady=(0, 25))
        
        # Section title
        title_label = ctk.CTkLabel(
            section,
            text=title,
            font=ctk.CTkFont(size=self.font_sizes[self.current_font_size]["header"], weight="bold"),
            text_color=ACCENT
        )
        title_label.pack(anchor="w", pady=(0, 15))
        
        # Settings items
        for setting_name, setting_type, setting_options in settings:
            item_frame = ctk.CTkFrame(section, fg_color=BG, corner_radius=8, height=45)
            item_frame.pack(fill="x", pady=4)
            item_frame.pack_propagate(False)
            
            # Setting name
            name_label = ctk.CTkLabel(
                item_frame,
                text=setting_name,
                font=ctk.CTkFont(size=self.font_sizes[self.current_font_size]["normal"]),
                text_color=WHITE,
                anchor="w"
            )
            name_label.pack(side="left", padx=15, fill="x", expand=True)
            
            # Setting control
            if setting_type == "dropdown":
                if setting_name == "App Theme":
                    control = ctk.CTkOptionMenu(
                        item_frame,
                        values=setting_options,
                        fg_color=SURFACE,
                        button_color=ACCENT,
                        button_hover_color="#2BC4C1",
                        text_color=WHITE,
                        width=120,
                        command=self.apply_theme,
                        font=ctk.CTkFont(size=self.font_sizes[self.current_font_size]["normal"])
                    )
                    control.set(self.current_theme)
                elif setting_name == "Font Size":
                    control = ctk.CTkOptionMenu(
                        item_frame,
                        values=setting_options,
                        fg_color=SURFACE,
                        button_color=ACCENT,
                        button_hover_color="#2BC4C1",
                        text_color=WHITE,
                        width=120,
                        command=self.apply_font_size,
                        font=ctk.CTkFont(size=self.font_sizes[self.current_font_size]["normal"])
                    )
                    control.set(self.current_font_size)
                else:
                    control = ctk.CTkOptionMenu(
                        item_frame,
                        values=setting_options,
                        fg_color=SURFACE,
                        button_color=ACCENT,
                        button_hover_color="#2BC4C1",
                        text_color=WHITE,
                        width=120,
                        font=ctk.CTkFont(size=self.font_sizes[self.current_font_size]["normal"])
                    )
                    control.set(setting_options[0])
                control.pack(side="right", padx=15)
            
            elif setting_type == "switch":
                control = ctk.CTkSwitch(
                    item_frame,
                    text="",
                    progress_color=ACCENT,
                    button_color=WHITE,
                    button_hover_color="#CCCCCC",
                    width=46
                )
                control.pack(side="right", padx=15)
            
            elif setting_type == "path":
                def browse_path():
                    # This is a placeholder for the file dialog functionality
                    pass
                
                control = ctk.CTkButton(
                    item_frame,
                    text=setting_options,
                    command=browse_path,
                    fg_color=SURFACE,
                    hover_color=HOVER,
                    text_color=WHITE,
                    width=100,
                    height=28
                )
                control.pack(side="right", padx=15)
            
            elif setting_type == "button":
                control = ctk.CTkButton(
                    item_frame,
                    text=setting_options,
                    fg_color=SURFACE,
                    hover_color=HOVER,
                    text_color=WHITE,
                    width=100,
                    height=28
                )
                control.pack(side="right", padx=15)

if __name__ == "__main__":
    app = ZyncApp()
    app.mainloop() 