import tkinter as tk
import threading
import time
import ctypes
import win32gui
import win32con
import win32api
import queue

# Unique ID for our window class
WM_TASKBAR = win32con.WM_USER + 1

class LockTimerApp:
    def __init__(self):
        self.is_running = True
        self.countdown_thread = None
        self.remaining_time = 0
        self.queue = queue.Queue()

        print("Initializing LockTimerApp")
        self.create_window()
        self.create_tray()

    def create_window(self):
        print("Creating window")
        self.root = tk.Tk()
        self.root.title("Lock Timer")
        self.root.geometry("300x400")
        self.root.withdraw()  # Hide window initially

        frame = tk.Frame(self.root)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        label = tk.Label(frame, text="Choose a timer duration:", font=("Arial", 16))
        label.pack(pady=20)

        button_style = {"font": ("Arial", 14), "width": 20, "height": 2}

        self.button_1min = tk.Button(frame, text="1 Minute (Test)", command=lambda: self.start_timer(1), **button_style)
        self.button_1min.pack(pady=10)

        self.button_30min = tk.Button(frame, text="30 Minutes", command=lambda: self.start_timer(30), **button_style)
        self.button_30min.pack(pady=10)

        self.button_1hour = tk.Button(frame, text="1 Hour", command=lambda: self.start_timer(60), **button_style)
        self.button_1hour.pack(pady=10)

        self.timer_label = tk.Label(frame, text="", font=("Arial", 16))
        self.timer_label.pack(pady=20)

        close_button = tk.Button(frame, text="Close", command=self.hide_window, width=10)
        close_button.pack(pady=10)

        print("Window created successfully")

    def create_tray(self):
        print("Creating tray icon")
        wc = win32gui.WNDCLASS()
        hinst = wc.hInstance = win32api.GetModuleHandle(None)
        wc.lpszClassName = "LockTimerTray"
        wc.lpfnWndProc = self.wnd_proc
        classAtom = win32gui.RegisterClass(wc)
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(classAtom, "Lock Timer", style,
                                          0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                                          0, 0, hinst, None)
        win32gui.UpdateWindow(self.hwnd)

        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
        nid = (self.hwnd, 0, flags, WM_TASKBAR, win32gui.LoadIcon(0, win32con.IDI_APPLICATION), "Lock Timer")
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
        print("Tray icon created successfully")

    def wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == WM_TASKBAR:
            if lparam == win32con.WM_LBUTTONUP:
                print("Left click detected")
                self.queue.put("show_window")
            elif lparam == win32con.WM_RBUTTONUP:
                menu = win32gui.CreatePopupMenu()
                win32gui.AppendMenu(menu, win32con.MF_STRING, 1, "Exit")
                pos = win32gui.GetCursorPos()
                win32gui.SetForegroundWindow(self.hwnd)
                win32gui.TrackPopupMenu(menu, win32con.TPM_LEFTALIGN, pos[0], pos[1], 0, self.hwnd, None)
                win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)
        elif msg == win32con.WM_COMMAND:
            id = win32api.LOWORD(wparam)
            if id == 1:  # Exit option
                win32gui.DestroyWindow(self.hwnd)
        elif msg == win32con.WM_DESTROY:
            win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, (self.hwnd, 0))
            win32gui.PostQuitMessage(0)

        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

    def start_timer(self, minutes):
        self.button_1min.config(state="disabled")
        self.button_30min.config(state="disabled")
        self.button_1hour.config(state="disabled")
        
        self.remaining_time = minutes * 60
        if self.countdown_thread is None or not self.countdown_thread.is_alive():
            self.countdown_thread = threading.Thread(target=self.run_timer, daemon=True)
            self.countdown_thread.start()

    def run_timer(self):
        while self.remaining_time > 0 and self.is_running:
            mins, secs = divmod(self.remaining_time, 60)
            timeformat = f"{mins:02d}:{secs:02d}"
            self.queue.put(("update_timer", f"Time remaining: {timeformat}"))
            time.sleep(1)
            self.remaining_time -= 1

        if self.is_running:
            self.lock_pc()

    def lock_pc(self):
        try:
            ctypes.windll.user32.LockWorkStation()
        except:
            self.queue.put(("update_timer", "Failed to lock. Please lock manually."))

    def show_window(self):
        print("show_window method called")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        window_width = 300
        window_height = 400
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        print(f"Positioning window at: {x}, {y}")
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.deiconify()
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        self.root.focus_force()
        print("Window should now be visible")

    def hide_window(self):
        self.root.withdraw()

    def process_queue(self):
        try:
            while True:
                message = self.queue.get_nowait()
                if message == "show_window":
                    self.show_window()
                elif isinstance(message, tuple) and message[0] == "update_timer":
                    self.timer_label.config(text=message[1])
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.process_queue)

    def run(self):
        print("Starting main loop")
        self.root.after(100, self.process_queue)
        while self.is_running:
            win32gui.PumpWaitingMessages()
            self.root.update()
        print("Main loop ended")

if __name__ == "__main__":
    print("Starting application")
    app = LockTimerApp()
    try:
        app.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    print("Application ended")