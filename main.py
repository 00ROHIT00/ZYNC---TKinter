import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk, ImageFont, ImageDraw
import os
import sys
import webbrowser

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Minimalist Color Scheme
BG = "#111111"        # Almost black
SURFACE = "#181818"   # Slightly lighter black
ACCENT = "#32E6E2"    # Cyan
GRAY = "#808080"      # Medium gray for better readability
WHITE = "#ffffff"     # Pure white
HOVER = "#222222"     # Hover state

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

        # Configure window
        self.title("ZYNC")
        self.geometry("1100x750")
        
        # Set window icon
        icon_ico_path = resource_path(os.path.join("assets", "icon.ico"))
        if sys.platform.startswith("win") and os.path.exists(icon_ico_path):
            try:
                self.iconbitmap(icon_ico_path)
            except Exception as e:
                print(f"Failed to set .ico icon: {e}")

        # Set theme
        ctk.set_appearance_mode("dark")
        self._set_appearance_mode("dark")
        self.configure(fg_color=BG)

        # Create main layout
        self.setup_layout()

    def setup_layout(self):
        # Main container
        self.container = ctk.CTkFrame(self, fg_color=BG)
        self.container.pack(expand=True, fill="both", padx=40, pady=30)

        # Top bar with logo and status
        self.create_top_bar()
        
        # Content frame that will switch between views
        self.content_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.content_frame.pack(expand=True, fill="both")
        
        # Initially show the action grid
        self.show_action_grid()
        
        # Bottom bar with utilities
        self.create_bottom_bar()

    def create_top_bar(self):
        # Top bar container
        top_bar = ctk.CTkFrame(self.container, fg_color="transparent", height=80)
        top_bar.pack(fill="x", pady=(0, 40))
        top_bar.pack_propagate(False)

        # Left side - Logo and title
        logo_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        logo_frame.pack(side="left", fill="y")

        # Load logo
        logo_path = resource_path(os.path.join("assets", "icon.png"))
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((40, 40), Image.Resampling.LANCZOS)
        self.logo_image = ctk.CTkImage(light_image=logo_image, dark_image=logo_image, size=(40, 40))
        
        logo_label = ctk.CTkLabel(logo_frame, image=self.logo_image, text="")
        logo_label.pack(side="left")

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

    def show_action_grid(self):
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
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

    def connect_device(self):
        self.status_label.configure(text="●  Connecting...", text_color=ACCENT)

    def live_scan(self):
        pass

    def scan_logs(self):
        pass

    def export_logs(self):
        pass

    def open_settings(self):
        pass

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
        logo_label = ctk.CTkLabel(logo_frame, image=self.logo_image, text="")
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
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Main container with some padding
        main_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        main_container.pack(expand=True, fill="both", padx=40, pady=30)
        
        # Header
        header_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 30))
        
        header_title = ctk.CTkLabel(
            header_frame,
            text="Device Information",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=WHITE
        )
        header_title.pack(side="left")
        
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
        
        # Content area with sections
        content_frame = ctk.CTkFrame(main_container, fg_color=SURFACE, corner_radius=15)
        content_frame.pack(expand=True, fill="both")
        
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

if __name__ == "__main__":
    app = ZyncApp()
    app.mainloop() 