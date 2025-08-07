import tkinter as tk
from PIL import Image, ImageTk
import sys
import os
from pygame import mixer

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

mixer.init()
mixer.music.load(resource_path("assets/music_twilighttown.mp3"))
mixer.music.play(-1)

WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15
CYCLES_BEFORE_LONG_BREAK = 4

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Hearts - Twilight Town")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.remaining_seconds = WORK_MIN * 60

        self.original_bg = Image.open(resource_path("assets/bg_twilighttown.png"))
        self.bg = ImageTk.PhotoImage(self.original_bg.resize((800, 600)))

        self.canvas = tk.Canvas(self.root, width=800, height=600, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.bg_image_id = self.canvas.create_image(0, 0, image=self.bg, anchor="nw")
        self.timer_text = self.canvas.create_text(400, 300, text="25:00", fill="white", font=("Arial", 48, "bold"))
        self.session_label = self.canvas.create_text(400, 250, text="Work Time", fill="dark orange", font=("Arial", 24, "bold"))

        # Estilo uniforme para todos los botones
        button_style = {
            "bg": "gray20",
            "fg": "white",
            "relief": tk.FLAT,
            "padx": 10,
            "pady": 5,
            "font": ("Arial", 10, "bold")
        }

        self.start_button = tk.Button(self.root, text="Start", command=self.start_timer, **button_style)
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_timer, **button_style)
        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_timer, **button_style)
        self.mute_button = tk.Button(self.root, text="Mute", command=self.toggle_mute, **button_style)

        self.volume_slider = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL,
                                      command=self.change_volume, length=150,
                                      bg="gray20", fg="white", troughcolor="gray50", highlightthickness=0)
        self.volume_slider.set(50)
        mixer.music.set_volume(0.5)

        # Posicionamiento de botones
        self.start_button_window = self.canvas.create_window(300, 400, window=self.start_button)
        self.reset_button_window = self.canvas.create_window(500, 400, window=self.reset_button)
        self.pause_button_window = self.canvas.create_window(400, 460, window=self.pause_button)
        self.mute_button_window = self.canvas.create_window(400, 520, window=self.mute_button)
        self.volume_slider_window = self.canvas.create_window(400, 560, window=self.volume_slider)

        self.root.bind("<Configure>", self.on_resize)

        self.cycle_count = 0
        self.running = False
        self.muted = False

    def on_resize(self, event):
        if event.widget != self.root:
            return

        width = self.root.winfo_width()
        height = self.root.winfo_height()

        resized_image = self.original_bg.resize((width, height), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(resized_image)
        self.canvas.itemconfig(self.bg_image_id, image=self.bg)
        self.canvas.config(width=width, height=height)

        self.canvas.coords(self.timer_text, width // 2, height // 2)
        self.canvas.coords(self.session_label, width // 2, height // 2 - 60)
        self.canvas.coords(self.start_button_window, width // 2 - 120, height // 2 + 100)
        self.canvas.coords(self.reset_button_window, width // 2 + 120, height // 2 + 100)
        self.canvas.coords(self.pause_button_window, width // 2, height // 2 + 160)
        self.canvas.coords(self.mute_button_window, width // 2, height // 2 + 220)
        self.canvas.coords(self.volume_slider_window, width // 2, height // 2 + 260)

    def start_timer(self):
        if not self.running:
            self.running = True
            self._countdown(self.remaining_seconds)

    def _start_countdown(self, seconds, label_text="Work Time"):
        self.canvas.itemconfig(self.session_label, text=label_text)
        self._countdown(seconds)

    def _countdown(self, seconds):
        if not self.running:
            self.remaining_seconds = seconds
            return

        mins, secs = divmod(seconds, 60)
        self.canvas.itemconfig(self.timer_text, text=f"{mins:02d}:{secs:02d}")
        self.remaining_seconds = seconds

        if seconds > 0:
            self.root.after(1000, lambda: self._countdown(seconds - 1))
        else:
            self._next_session()

    def _next_session(self):
        self.cycle_count += 1
        if self.cycle_count % CYCLES_BEFORE_LONG_BREAK == 0:
            self._start_countdown(LONG_BREAK_MIN * 60, "Long Break")
        else:
            self._start_countdown(SHORT_BREAK_MIN * 60, "Short Break")

    def reset_timer(self):
        self.running = False
        self.remaining_seconds = WORK_MIN * 60
        self.canvas.itemconfig(self.timer_text, text="25:00")
        self.canvas.itemconfig(self.session_label, text="Work Time")
        self.cycle_count = 0

    def pause_timer(self):
        self.running = False

    def toggle_mute(self):
        if self.muted:
            volume = self.volume_slider.get() / 100
            mixer.music.set_volume(volume)
            self.mute_button.config(text="Mute")
            self.muted = False
        else:
            mixer.music.set_volume(0)
            self.mute_button.config(text="Unmute")
            self.muted = True

    def change_volume(self, value):
        if not self.muted:
            volume = int(value) / 100
            mixer.music.set_volume(volume)

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
