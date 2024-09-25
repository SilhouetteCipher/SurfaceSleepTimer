## Perfect for Surface Tablets and YouTube Users

This application is ideal for Surface tablet users who enjoy watching YouTube videos before sleep. The screensaver button enables a blank screen, which is particularly useful as Windows YouTube does not support audio playback while the device is locked. By using this timer, you ensure that your device locks when the timer ends, preventing unnecessary battery drain throughout the night.

![Surface Sleep Timer Screenshot](images/screenshot.png | width=300)

# Surface Sleep Timer

This is a modern, customizable lock timer application built with Python and CustomTkinter. It allows users to set a timer for 30 minutes or 1 hour, after which it will lock the computer. It also includes a system tray icon for easy access and a screensaver activation feature.

## Features

- Set a timer for 30 minutes or 1 hour
- Lock computer automatically when timer expires
- Start screensaver on demand which lets you turn the screen off when using the Blank Screen Screensaver
- System tray icon for quick access
- Minimize to system tray

## Requirements

- Python 3.7+
- CustomTkinter
- Pystray
- Pillow (PIL)

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/SilhouetteCipher/SurfaceSleepTimer.git
   cd SurfaceSleepTimer
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, use the following command in the project directory:

```
python lockTimer.py
```

## Building an Executable with PyInstaller

To create a standalone executable that doesn't require Python to be installed, you can use PyInstaller. Follow these steps:

1. Install PyInstaller if you haven't already:

   ```
   pip install pyinstaller
   ```

2. Create the executable:

   ```
   pyinstaller --windowed --add-data "timer.ico;." --icon=timer.ico lockTimer.py
   ```

   This command does the following:

   - `--windowed`: Creates a windowed application without a console
   - `--add-data "timer.ico;."`: Includes the timer.ico file in the executable
   - `--icon=timer.ico`: Sets the application icon

3. The executable will be created in the `dist/lockTimer` directory.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)
