# ZYNC Application

A modern Tkinter-based application for device connectivity and log management.

## Features

- Connect to devices
- Live scanning functionality
- View and manage scan logs
- Export logs
- Application settings

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Requirements

- Python 3.7+
- CustomTkinter 5.2.2
- Pillow 10.2.0

## Development

The application uses CustomTkinter for a modern, dark-themed UI. The main components are:
- Sidebar with navigation buttons
- Main content area
- Status display
- Modern dark theme 