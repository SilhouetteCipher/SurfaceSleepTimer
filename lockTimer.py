import customtkinter as ctk
import threading
import time
import ctypes
from pystray import MenuItem as item
import pystray
from PIL import Image
import sys

class ModernLockTimerApp:
    def __init__(self):
        self.is_running = True
        self.countdown_thread = None
        self.remaining_time = 0

        # Load custom icon
        icon_path = "timer.ico"
        menu = (item('Show', self.show_window), item('Exit', self.quit_app))
        self.icon = pystray.Icon("timer", Image.open(icon_path), "Lock Timer", menu)
        threading.Thread(target=self.icon.run, daemon=True).start()

        self.create_window()

    def create_window(self):
        self.root = ctk.CTk()
        self.root.title("Lock Timer")
        
        # Set window size
        window_width = 280
        window_height = 370  # Further reduced height
        
        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate position
        position_right = int(screen_width + window_width*2)
        position_down = int(screen_height - window_height/3)
        
        # Set the geometry of the window
        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")
        
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)
        
        # Set the taskbar icon
        self.root.iconbitmap("timer.ico")

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        frame = ctk.CTkFrame(master=self.root)
        frame.pack(pady=10, padx=10, fill="both", expand=True)

        label = ctk.CTkLabel(master=frame, text="Choose a timer duration:", font=("Arial", 16))
        label.pack(pady=(0, 5))

        button_style = {"font": ("Arial", 14), "width": 200, "height": 60}

        self.button_30min = ctk.CTkButton(master=frame, text="30 Minutes", command=lambda: self.start_timer(30), **button_style)
        self.button_30min.pack(pady=5)

        self.button_1hour = ctk.CTkButton(master=frame, text="1 Hour", command=lambda: self.start_timer(60), **button_style)
        self.button_1hour.pack(pady=5)

        self.timer_label = ctk.CTkLabel(master=frame, text="", font=("Arial", 16))
        self.timer_label.pack(pady=5)

        # Add screensaver button
        screensaver_button = ctk.CTkButton(master=frame, text="Start Screensaver", command=self.start_screensaver, **button_style)
        screensaver_button.pack(pady=5)

        # Create a frame for the bottom row buttons
        bottom_frame = ctk.CTkFrame(master=frame)
        bottom_frame.pack(pady=5)

        # Create a new style for bottom row buttons
        bottom_button_style = {"font": ("Arial", 14), "width": 97, "height": 60}

        # Add minimize and exit buttons inside the bottom frame
        minimize_button = ctk.CTkButton(master=bottom_frame, text="Minimize", command=self.hide_window, **bottom_button_style)
        minimize_button.pack(side="left", padx=(0, 3))

        exit_button = ctk.CTkButton(master=bottom_frame, text="Exit", command=self.quit_app, **bottom_button_style)
        exit_button.pack(side="left", padx=(3, 0))

    def start_timer(self, minutes):
        self.button_30min.configure(state="disabled")
        self.button_1hour.configure(state="disabled")
        
        self.remaining_time = minutes * 60
        if self.countdown_thread is None or not self.countdown_thread.is_alive():
            self.countdown_thread = threading.Thread(target=self.run_timer, daemon=True)
            self.countdown_thread.start()

    def run_timer(self):
        while self.remaining_time > 0 and self.is_running:
            mins, secs = divmod(self.remaining_time, 60)
            timeformat = f"{mins:02d}:{secs:02d}"
            self.timer_label.configure(text=f"Time remaining: {timeformat}")
            time.sleep(1)
            self.remaining_time -= 1

        if self.is_running:
            self.lock_pc()

    def lock_pc(self):
        try:
            ctypes.windll.user32.LockWorkStation()
        except:
            self.timer_label.configure(text="Failed to lock. Please lock manually.")

    def start_screensaver(self):
        try:
            ctypes.windll.user32.SendMessageW(0xFFFF, 0x112, 0xF140, 0)
        except:
            self.timer_label.configure(text="Failed to start screensaver. Please start manually.")

    def show_window(self):
        self.root.after(0, self._show_window)

    def _show_window(self):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def hide_window(self):
        self.root.withdraw()

    def quit_app(self):
        self.is_running = False
        self.icon.stop()
        self.root.quit()
        sys.exit()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ModernLockTimerApp()
    app.run()