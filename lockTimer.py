import customtkinter as ctk
import threading
import time
import ctypes
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageDraw
import os
import tempfile
import sys

class ModernLockTimerApp:
    def __init__(self):
        self.is_running = True
        self.countdown_thread = None
        self.remaining_time = 0

        # Create custom icon
        self.icon_path = self.create_clock_icon()
        menu = (item('Show', self.show_window), item('Exit', self.quit_app))
        self.icon = pystray.Icon("lock_timer", Image.open(self.icon_path), "Lock Timer", menu)
        threading.Thread(target=self.icon.run, daemon=True).start()

        self.create_window()

    def create_clock_icon(self, size=64, bg_color=(0, 150, 255), fg_color=(255, 255, 255)):
        image = Image.new('RGBA', (size, size), color=bg_color+(255,))
        draw = ImageDraw.Draw(image)
        
        # Draw clock circle
        draw.ellipse([2, 2, size-2, size-2], outline=fg_color, width=2)
        
        # Draw clock hands
        center = size // 2
        draw.line([center, center, center, 10], fill=fg_color, width=2)  # Hour hand
        draw.line([center, center, size-10, center], fill=fg_color, width=2)  # Minute hand
        
        # Save as .ico file
        ico_output = tempfile.NamedTemporaryFile(suffix='.ico', delete=False)
        image.save(ico_output, format='ICO', sizes=[(64, 64)])
        ico_output.close()
        
        return ico_output.name

    def create_window(self):
        self.root = ctk.CTk()
        self.root.title("Lock Timer")
        
        # Set window size
        window_width = 300
        window_height = 450
        
        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate position
        position_right = int(screen_width + window_width*2)
        position_down = int(screen_height - window_height/2)
        
        # Set the geometry of the window
        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")
        
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)
        
        # Set the taskbar icon
        if sys.platform.startswith('win'):
            self.root.iconbitmap(default=self.icon_path)
        else:
            icon_image = Image.open(self.icon_path)
            self.root.iconphoto(True, ctk.CTkImage(light_image=icon_image, dark_image=icon_image))

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        frame = ctk.CTkFrame(master=self.root)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        label = ctk.CTkLabel(master=frame, text="Choose a timer duration:", font=("Arial", 16))
        label.pack(pady=20)

        button_style = {"font": ("Arial", 14), "width": 300, "height": 80}

        self.button_30min = ctk.CTkButton(master=frame, text="30 Minutes", command=lambda: self.start_timer(30), **button_style)
        self.button_30min.pack(pady=10)

        self.button_1hour = ctk.CTkButton(master=frame, text="1 Hour", command=lambda: self.start_timer(60), **button_style)
        self.button_1hour.pack(pady=10)

        self.timer_label = ctk.CTkLabel(master=frame, text="", font=("Arial", 16))
        self.timer_label.pack(pady=20)

        # Add exit button with matching style
        exit_button = ctk.CTkButton(master=frame, text="Exit", command=self.quit_app, **button_style)
        exit_button.pack(pady=10)

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
        os.remove(self.icon_path)  # Clean up the temporary icon file
        sys.exit()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ModernLockTimerApp()
    app.run()