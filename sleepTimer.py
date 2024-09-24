import tkinter as tk
import threading
import time
import subprocess

class SleepTimerApp:
    def __init__(self, master):
        self.master = master
        master.title("Sleep Timer")
        master.geometry("400x400")

        self.label = tk.Label(master, text="Choose a timer duration:", font=("Arial", 16))
        self.label.pack(pady=20)

        button_style = {"font": ("Arial", 14), "width": 15, "height": 2}

        self.button_1min = tk.Button(master, text="1 Minute (Test)", command=lambda: self.start_timer(1), **button_style)
        self.button_1min.pack(pady=10)

        self.button_30min = tk.Button(master, text="30 Minutes", command=lambda: self.start_timer(30), **button_style)
        self.button_30min.pack(pady=10)

        self.button_1hour = tk.Button(master, text="1 Hour", command=lambda: self.start_timer(60), **button_style)
        self.button_1hour.pack(pady=10)

        self.timer_label = tk.Label(master, text="", font=("Arial", 16))
        self.timer_label.pack(pady=20)

    def start_timer(self, minutes):
        self.button_1min.config(state=tk.DISABLED)
        self.button_30min.config(state=tk.DISABLED)
        self.button_1hour.config(state=tk.DISABLED)
        
        threading.Thread(target=self.run_timer, args=(minutes,), daemon=True).start()

    def run_timer(self, minutes):
        seconds = minutes * 60
        while seconds > 0:
            mins, secs = divmod(seconds, 60)
            timeformat = f"{mins:02d}:{secs:02d}"
            self.timer_label.config(text=f"Time remaining: {timeformat}")
            time.sleep(1)
            seconds -= 1

        self.sleep_device()

    def sleep_device(self):
        try:
            subprocess.run(["powershell", "-Command", "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Application]::SetSuspendState('Suspend', $false, $true)"], check=True)
        except subprocess.CalledProcessError:
            self.timer_label.config(text="Failed to sleep. Please sleep manually.")

root = tk.Tk()
app = SleepTimerApp(root)
root.mainloop()