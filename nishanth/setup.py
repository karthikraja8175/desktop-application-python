from cx_Freeze import setup, Executable

# Define the executable
executables = [
    Executable(
        "main.py",                # Main script
        base="Win32GUI",          # Hides the console window for GUI apps
        target_name="AMV2.exe",   # Name of the generated .exe
        icon="images/logo.ico",   # Application icon
    )
]

# Build options
build_options = {
    "packages": [],  # Add Python packages required by your app
    "include_files": [  # Include additional files and folders
        "images/",       # Folder with .ico and .png files
        "am.db",   # Database file
    ],
}

# Setup configuration
setup(
    name="AMV2",
    version="1.0",
    description="Billing application",
    options={"build_exe": build_options},
    executables=executables,
)