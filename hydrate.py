import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import pygame

class WaterReminderTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Hydration Timer")
        self.root.geometry("500x850")  
        self.root.resizable(True, True) 
        self.root.configure(bg="#0d1b2a")
        # Timer settings (10 minutes = 600 seconds for testing)
        self.total_time = 10  # 10 minutes in seconds
        self.remaining_time = self.total_time
        self.is_running = False
        self.water_count = 0

        # Initialize pygame mixer for sound
        pygame.mixer.init()
        self.alarm_path = os.path.join(os.path.dirname(__file__), "alarm.mp3")

        # Load water glass images
        self.load_images()

        # UI Elements
        self.create_widgets()

    def load_images(self):
        """Load all water glass images"""
        self.images = []
        image_dir = os.path.join(os.path.dirname(__file__), "images")

        # Load images from full (full glass) to full6 (empty glass)
        for i in range(7):
            if i == 0:
                img_path = os.path.join(image_dir, "full.png")
            else:
                img_path = os.path.join(image_dir, f"full{i}.png")

            img = Image.open(img_path)
            img = img.resize((150, 200), Image.Resampling.NEAREST)
            photo = ImageTk.PhotoImage(img)
            self.images.append(photo)

    def get_current_image_index(self):
        """Get the image index based on remaining time"""
        # Calculate progress (0 to 1)
        progress = (self.total_time - self.remaining_time) / self.total_time
        # Map to image index (0=full, 6=empty)
        index = int(progress * 6)
        return min(index, 6)

    def create_widgets(self):
        # Main container with enhanced padding
        main_frame = tk.Frame(self.root, bg="#0d1b2a")
        main_frame.pack(expand=True, fill="both", padx=35, pady=35)

        # Title with icon - Enhanced styling
        title_frame = tk.Frame(main_frame, bg="#0d1b2a")
        title_frame.pack(pady=(0, 25))

        title_label = tk.Label(
            title_frame,
            text="Hydration Timer",
            font=("Arima Madurai", 40, "bold"),
            fg="#4dd0e1",
            bg="#0d1b2a"
        )
        title_label.pack()

        subtitle_label = tk.Label(
            title_frame,
            text="Stay healthy, drink water every 10 min",
            font=("TkDefaultFont", 12),
            fg="#90a4ae",
            bg="#0d1b2a"
        )
        subtitle_label.pack(pady=(8, 0))

        # Water glass image display - No border
        image_frame = tk.Frame(main_frame, bg="#0d1b2a")
        image_frame.pack(pady=25)

        self.glass_label = tk.Label(
            image_frame,
            image=self.images[0],
            bg="#0d1b2a"
        )
        self.glass_label.pack()

        # Timer display below glass - Enhanced
        self.timer_label = tk.Label(
            main_frame,
            text=self.format_time(self.remaining_time),
            font=("TkDefaultFont", 56, "bold"),
            fg="#4dd0e1",
            bg="#0d1b2a"
        )
        self.timer_label.pack(pady=15)

        # Water count card - Enhanced with border
        water_card = tk.Frame(main_frame, bg="#1a2f45", bd=0, highlightbackground="#2a4a6f", highlightthickness=2)
        water_card.pack(pady=25, fill="x", padx=10)

        water_icon_label = tk.Label(
            water_card,
            text="💧",
            font=("TkDefaultFont", 40),
            bg="#1a2f45"
        )
        water_icon_label.pack(side="left", padx=25, pady=18)

        water_info_frame = tk.Frame(water_card, bg="#1a2f45")
        water_info_frame.pack(side="left", pady=18)

        self.water_count_label = tk.Label(
            water_info_frame,
            text=str(self.water_count),
            font=("TkDefaultFont", 40, "bold"),
            fg="#4dd0e1",
            bg="#1a2f45"
        )
        self.water_count_label.pack(anchor="w")

        water_text_label = tk.Label(
            water_info_frame,
            text="glasses today",
            font=("TkDefaultFont", 13),
            fg="#90a4ae",
            bg="#1a2f45"
        )
        water_text_label.pack(anchor="w")

        # Button Frame
        button_frame = tk.Frame(main_frame, bg="#0d1b2a")
        button_frame.pack(pady=25)

        # Start/Pause Button - Rounded with black text
        self.start_pause_btn = tk.Button(
            button_frame,
            text="START",
            command=self.toggle_timer,
            font=("Arial", 14, "bold"),
            bg="#4dd0e1",
            fg="#000000",  # Black text
            width=18,
            height=2,
            cursor="hand2",
            bd=0,
            relief="solid",
            activebackground="#26c6da",
            activeforeground="#000000",
            highlightthickness=2,
            highlightbackground="#4dd0e1",
            borderwidth=0
        )
        self.start_pause_btn.pack(side="left", padx=10)
        # Make button rounded
        self.start_pause_btn.config(highlightthickness=0, borderwidth=0)

        # Reset Button - Rounded
        self.reset_btn = tk.Button(
            button_frame,
            text="RESET",
            command=self.reset_timer,
            font=("Arial", 14, "bold"),
            bg="#ffa726",
            fg="#0d1b2a",
            width=10,
            height=2,
            cursor="hand2",
            bd=0,
            relief="solid",
            activebackground="#ff9800",
            activeforeground="#0d1b2a",
            highlightthickness=0,
            borderwidth=0
        )
        self.reset_btn.pack(side="left", padx=10)

        # Status Label - Enhanced
        self.status_label = tk.Label(
            main_frame,
            text="Ready to start",
            font=("TkDefaultFont", 12),
            fg="#90a4ae",
            bg="#0d1b2a"
        )
        self.status_label.pack(pady=12)

    def update_glass_image(self):
        """Update the water glass image based on time remaining"""
        index = self.get_current_image_index()
        self.glass_label.config(image=self.images[index])

    def format_time(self, seconds):
        """Convert seconds to MM:SS format"""
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"

    def toggle_timer(self):
        """Start or pause the timer"""
        if self.is_running:
            self.is_running = False
            self.start_pause_btn.config(text="RESUME", bg="#4dd0e1", fg="#000000")
            self.status_label.config(text="Paused", fg="#ffa726")
        else:
            self.is_running = True
            self.start_pause_btn.config(text="PAUSE", bg="#4dd0e1", fg="#000000")  # Black text
            self.status_label.config(text="Timer active!", fg="#4dd0e1")
            self.update_timer()

    def update_timer(self):
        """Update the timer every second"""
        if self.is_running and self.remaining_time > 0:
            self.remaining_time -= 1
            self.timer_label.config(text=self.format_time(self.remaining_time))
            self.update_glass_image()
            self.root.after(1000, self.update_timer)
        elif self.remaining_time == 0:
            self.timer_complete()

    def timer_complete(self):
        """Handle timer completion"""
        self.is_running = False
        self.water_count += 1
        self.water_count_label.config(text=str(self.water_count))

        # Play alarm sound for 10 seconds
        self.play_alarm()

        # Show notification (blocks until OK is clicked)
        messagebox.showinfo(
            "Time to Hydrate!",
            "10 minutes have passed!\n\nDrink a glass of water now!\n\nYour body will thank you!"
        )

        # Stop alarm when OK is clicked
        pygame.mixer.music.stop()

        # Reset timer for next round
        self.remaining_time = self.total_time
        self.timer_label.config(text=self.format_time(self.remaining_time))
        self.update_glass_image()
        self.start_pause_btn.config(text="START", bg="#1a2f45", fg="white")
        self.status_label.config(text="Great job!", fg="#4caf50")

    def play_alarm(self):
        """Play alarm sound (will loop until stopped)"""
        try:
            if os.path.exists(self.alarm_path):
                pygame.mixer.music.load(self.alarm_path)
                pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        except Exception as e:
            print(f"Could not play alarm: {e}")

    def reset_timer(self):
        """Reset the timer to initial state"""
        self.is_running = False
        self.remaining_time = self.total_time
        self.timer_label.config(text=self.format_time(self.remaining_time))
        self.update_glass_image()
        self.start_pause_btn.config(text="START", bg="#1a2f45", fg="white")
        self.status_label.config(text="Timer reset", fg="#90a4ae")


def main():
    root = tk.Tk()
    app = WaterReminderTimer(root)
    root.mainloop()


if __name__ == "__main__":
    main()