import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import math
import time
import random
from datetime import datetime

class AdvancedPrayerAnimation(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Simulasi Doa Kristen Advanced")
        self.geometry("800x600")
        
        # Setup frame utama
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)
        
        # Canvas untuk animasi
        self.canvas = tk.Canvas(self.main_frame, width=800, height=500, bg='#1a1a2e')
        self.canvas.pack(fill="both", expand=True)
        
        # Frame untuk kontrol
        self.control_frame = tk.Frame(self.main_frame, bg='#162447')
        self.control_frame.pack(fill="x", pady=5)
        
        # Inisialisasi variabel
        self.animation_speed = 0.05
        self.light_intensity = 0
        self.prayer_particles = []
        self.stars = []
        self.is_praying = False
        self.prayer_count = 0
        self.prayer_time = 0
        self.start_time = None
        self.current_prayer_index = 0
        
        # List doa-doa
        self.prayers = [
            "Bapa Kami yang di surga,",
            "Dikuduskanlah nama-Mu,",
            "Datanglah Kerajaan-Mu,",
            "Jadilah kehendak-Mu,",
            "Di bumi seperti di surga.",
            "Berilah kami pada hari ini makanan kami yang secukupnya,",
            "Dan ampunilah kami akan kesalahan kami,",
            "Seperti kami juga mengampuni orang yang bersalah kepada kami,",
            "Dan janganlah membawa kami ke dalam pencobaan,",
            "Tetapi lepaskanlah kami dari yang jahat.",
            "Amin."
        ]
        
        # Setup UI
        self.setup_ui()
        self.create_environment()
        self.create_person()
        self.create_stats_display()
        
        # Mulai animasi
        self.animate_stars()
        self.animate_particles()
        self.create_sound_effects()
        
    def setup_ui(self):
        # Tombol kontrol
        self.start_button = tk.Button(
            self.control_frame, 
            text="Mulai Berdoa", 
            command=self.toggle_prayer,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 10, 'bold')
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        # Slider kecepatan animasi
        tk.Label(
            self.control_frame, 
            text="Kecepatan:", 
            bg='#162447',
            fg='white'
        ).pack(side=tk.LEFT, padx=5)
        
        self.speed_scale = tk.Scale(
            self.control_frame,
            from_=0.01,
            to=0.1,
            resolution=0.01,
            orient=tk.HORIZONTAL,
            command=self.update_speed,
            bg='#162447',
            fg='white'
        )
        self.speed_scale.set(0.05)
        self.speed_scale.pack(side=tk.LEFT, padx=5)
        
        # Mode siang/malam
        self.time_var = tk.StringVar(value="malam")
        self.time_button = tk.Button(
            self.control_frame,
            text="🌙 Mode Malam",
            command=self.toggle_time,
            bg='#2d3436',
            fg='white'
        )
        self.time_button.pack(side=tk.LEFT, padx=5)
        
    def create_environment(self):
        self.create_church()
        self.create_stars()
        self.create_light_effect()
        
    def interpolate_color(self, color1, color2, factor):
        r1 = int(color1[1:3], 16)
        g1 = int(color1[3:5], 16)
        b1 = int(color1[5:7], 16)
        
        r2 = int(color2[1:3], 16)
        g2 = int(color2[3:5], 16)
        b2 = int(color2[5:7], 16)
        
        r = int(r1 + factor * (r2 - r1))
        g = int(g1 + factor * (g2 - g1))
        b = int(b1 + factor * (b2 - b1))
        
        return f"#{r:02x}{g:02x}{b:02x}"

    def create_church(self):
        gradient_steps = 100
        for i in range(gradient_steps):
            y = 150 + i
            factor = i / gradient_steps
            color = self.interpolate_color("#4a4e69", "#22223b", factor)
            self.canvas.create_line(200, y, 600, y, fill=color)
        
        self.create_church_window(300, 200)
        self.create_church_window(500, 200)
        self.create_cross(400, 100, 40, 60, color="gold", width=5)
        self.create_ornaments()
        
    def create_stars(self):
        for _ in range(50):
            x = random.randint(0, 800)
            y = random.randint(0, 300)
            size = random.randint(1, 3)
            self.stars.append({
                'id': self.canvas.create_oval(
                    x, y, x+size, y+size,
                    fill='white',
                    outline='white'
                ),
                'twinkle': random.random()
            })
            
    def animate_stars(self):
        if self.time_var.get() == "malam":
            for star in self.stars:
                star['twinkle'] += random.random() * 0.1
                opacity = abs(math.sin(star['twinkle']))
                hex_value = format(int(opacity * 255), '02x')
                color = f"#{hex_value}{hex_value}{hex_value}"
                self.canvas.itemconfig(
                    star['id'],
                    fill=color,
                    outline=color
                )
        self.after(50, self.animate_stars)
        
    def create_cross(self, x, y, cross_width, height, **kwargs):
        color = kwargs.get('color', 'white')
        line_width = kwargs.get('width', 2)
        
        # Vertical line
        self.canvas.create_line(
            x, y-height/2,
            x, y+height/2,
            fill=color,
            width=line_width
        )
        
        # Horizontal line
        self.canvas.create_line(
            x-cross_width/2, y,
            x+cross_width/2, y,
            fill=color,
            width=line_width
        )
        
    def create_church_window(self, x, y):
        self.canvas.create_arc(
            x-30, y-60, x+30, y+60,
            start=0, extent=180,
            fill="#ffd700",
            outline="#c9b037",
            width=2
        )
        
        for i in range(3):
            self.canvas.create_line(
                x-20+i*20, y-40,
                x-20+i*20, y+20,
                fill="#c9b037",
                width=2
            )
            
    def create_person(self):
        self.head = self.canvas.create_oval(
            380, 300, 420, 340,
            fill="#ffe0bd",
            outline="black"
        )
        
        self.face_details = [
            self.canvas.create_oval(390, 315, 395, 320, fill="black"),
            self.canvas.create_oval(405, 315, 410, 320, fill="black"),
            self.canvas.create_arc(
                390, 320, 410, 335,
                start=0, extent=-180,
                fill="",
                outline="black"
            )
        ]
        
        self.body = self.canvas.create_polygon(
            390, 340, 410, 340, 420, 400, 380, 400,
            fill="#4a4e69",
            outline="black",
            smooth=True
        )
        
        self.arms = [
            self.canvas.create_line(
                390, 350, 370, 380,
                fill="#ffe0bd",
                width=3,
                smooth=True
            ),
            self.canvas.create_line(
                410, 350, 430, 380,
                fill="#ffe0bd",
                width=3,
                smooth=True
            )
        ]
        
        self.legs = [
            self.canvas.create_line(
                390, 400, 385, 440,
                fill="black",
                width=3
            ),
            self.canvas.create_line(
                410, 400, 415, 440,
                fill="black",
                width=3
            )
        ]
        
    def create_light_effect(self):
        self.light_effect = self.canvas.create_oval(
            350, 50, 450, 150,
            fill="",
            outline="#ffd700",
            width=20
        )
        
    def create_stats_display(self):
        self.stats_frame = tk.Frame(self.main_frame, bg="#162447")
        self.stats_frame.pack(fill="x", pady=5)
        
        self.prayer_count_label = tk.Label(
            self.stats_frame,
            text="Jumlah Doa: 0",
            bg="#162447",
            fg="white",
            font=('Arial', 10)
        )
        self.prayer_count_label.pack(side=tk.LEFT, padx=5)
        
        self.prayer_time_label = tk.Label(
            self.stats_frame,
            text="Waktu Berdoa: 0:00",
            bg="#162447",
            fg="white",
            font=('Arial', 10)
        )
        self.prayer_time_label.pack(side=tk.LEFT, padx=5)
        
    def animate_person(self):
        if self.is_praying:
            angle = math.sin(time.time() * 2) * 10
            
            self.canvas.coords(
                self.head,
                380 + angle, 300 + abs(angle),
                420 + angle, 340 + abs(angle)
            )
            
            hand_angle = math.sin(time.time() * 2) * 5
            self.canvas.coords(
                self.arms[0],
                390 + angle, 350 + abs(angle),
                395 + hand_angle, 370 + abs(angle)
            )
            self.canvas.coords(
                self.arms[1],
                410 + angle, 350 + abs(angle),
                405 - hand_angle, 370 + abs(angle)
            )
            
            self.light_intensity = (math.sin(time.time() * 2) + 1) / 2
            gold_colors = ["#FFD700", "#DAA520", "#B8860B"]
            color_index = int(self.light_intensity * (len(gold_colors) - 1))
            self.canvas.itemconfig(
                self.light_effect,
                outline=gold_colors[color_index]
            )
            
            if time.time() - self.last_prayer_update > 3:
                self.update_prayer_text()
                self.last_prayer_update = time.time()
            
            self.update_stats()
            self.after(int(self.animation_speed * 1000), self.animate_person)
            
    def update_prayer_text(self):
        for item in self.canvas.find_withtag("prayer_text"):
            self.canvas.delete(item)
            
        self.canvas.create_text(
            400, 250,
            text=self.prayers[self.current_prayer_index],
            font=('Arial', 12, 'bold'),
            fill='white',
            tags="prayer_text"
        )
        
        self.current_prayer_index = (self.current_prayer_index + 1) % len(self.prayers)
        
    def update_stats(self):
        if self.start_time:
            current_time = time.time()
            elapsed_time = int(current_time - self.start_time)
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            self.prayer_time_label.config(
                text=f"Waktu Berdoa: {minutes}:{seconds:02d}"
            )
            
    def toggle_prayer(self):
        self.is_praying = not self.is_praying
        if self.is_praying:
            self.start_button.config(text="Selesai Berdoa", bg='#f44336')
            self.start_time = time.time()
            self.last_prayer_update = time.time()
            self.animate_person()
        else:
            self.start_button.config(text="Mulai Berdoa", bg='#4CAF50')
            self.prayer_count += 1
            self.prayer_count_label.config(text=f"Jumlah Doa: {self.prayer_count}")
            self.start_time = None
            self.create_person()
            
    def toggle_time(self):
        if self.time_var.get() == "malam":
            self.time_var.set("siang")
            self.canvas.config(bg='#87CEEB')
            self.time_button.config(text="☀️ Mode Siang")
        else:
            self.time_var.set("malam")
            self.canvas.config(bg='#1a1a2e')
            self.time_button.config(text="🌙 Mode Malam")
            
    def update_speed(self, value):
        self.animation_speed = float(value)
        
    def create_ornaments(self):
        for x in [250, 550]:
            self.create_pillar(x, 150, 40, 300)
        self.create_window_decorations()
        self.create_altar()
        
    def create_pillar(self, x, y, width, height):
        self.canvas.create_rectangle(
            x-width/2, y,
            x+width/2, y+height,
            fill="#6b705c",
            outline="#4a4e69"
        )
        
        for i in range(0, height, 30):
            self.canvas.create_rectangle(
                x-width/2-5, y+i,
                x+width/2+5, y+i+10,
                fill="#4a4e69",
                outline=""
            )
            
        self.canvas.create_arc(
            x-width/2-10, y-20,
            x+width/2+10, y+20,
            start=0, extent=180,
            fill="#4a4e69"
        )

    def create_window_decorations(self):
        for x in [300, 500]:
            self.canvas.create_arc(
                x-40, 160, x+40, 240,
                start=0, extent=180,
                fill="",
                outline="#c9b037",
                width=3
            )
            
            for i in range(-30, 31, 15):
                self.canvas.create_line(
                    x+i, 180,
                    x+i, 220,
                    fill="#c9b037",
                    width=2
                )
                
    def create_altar(self):
        self.canvas.create_rectangle(
            350, 380, 450, 400,
            fill="#8b7355",
            outline="#6b5b3f"
        )
        
        self.canvas.create_polygon(
            350, 380,
            450, 380,
            470, 440,
            330, 440,
            fill="#f5f5f5",
            outline="#e0e0e0"
        )
        
        self.create_candle(370, 370)
        self.create_candle(430, 370)
        
    def create_candle(self, x, y):
        self.canvas.create_rectangle(
            x-5, y,
            x+5, y+20,
            fill="white",
            outline="#e0e0e0"
        )
        
        flame = self.canvas.create_oval(
            x-3, y-10,
            x+3, y,
            fill="#ffd700",
            outline="#ff8c00",
            tags="flame"
        )
        
        self.animate_flame(flame)
        
    def animate_flame(self, flame):
        if self.is_praying:
            current_coords = self.canvas.coords(flame)
            offset_x = math.sin(time.time() * 10) * 2
            offset_y = math.sin(time.time() * 5) * 2
            
            self.canvas.coords(
                flame,
                current_coords[0] + offset_x,
                current_coords[1] + offset_y,
                current_coords[2] + offset_x,
                current_coords[3] + offset_y
            )
            
        self.after(50, lambda: self.animate_flame(flame))
        
    def create_particles(self):
        if self.is_praying and random.random() < 0.1:
            x = random.randint(350, 450)
            y = 150
            particle = self.canvas.create_oval(
                x, y, x+2, y+2,
                fill="#FFD700",
                outline=""
            )
            self.prayer_particles.append({
                'id': particle,
                'x': x,
                'y': y,
                'dx': random.uniform(-1, 1),
                'dy': random.uniform(-2, -1),
                'life': 1.0
            })
            
    def animate_particles(self):
        to_delete = []
        gold_shades = [
            "#FFD700",  # Bright gold
            "#DAA520",  # Goldenrod
            "#B8860B",  # Dark goldenrod
            "#CD853F",  # Peru
            "#8B4513"   # Saddle brown
        ]
        
        for particle in self.prayer_particles:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 0.02
            
            if particle['life'] > 0:
                self.canvas.coords(
                    particle['id'],
                    particle['x'],
                    particle['y'],
                    particle['x'] + 2,
                    particle['y'] + 2
                )
                
                color_index = min(
                    int((1 - particle['life']) * len(gold_shades)),
                    len(gold_shades) - 1
                )
                self.canvas.itemconfig(
                    particle['id'],
                    fill=gold_shades[color_index]
                )
            else:
                to_delete.append(particle)
                
        for particle in to_delete:
            self.canvas.delete(particle['id'])
            self.prayer_particles.remove(particle)
            
        if self.is_praying:
            self.create_particles()
        self.after(50, self.animate_particles)
        
    def create_sound_effects(self):
        try:
            import winsound
            def play_sound():
                if self.is_praying:
                    winsound.PlaySound(
                        "SystemAsterisk",
                        winsound.SND_ALIAS | winsound.SND_ASYNC
                    )
                    self.after(5000, play_sound)
            play_sound()
        except:
            pass
        
    def save_prayer_stats(self):
        if hasattr(self, 'start_time') and self.start_time:
            prayer_duration = time.time() - self.start_time
            with open("prayer_stats.txt", "a") as f:
                f.write(f"Date: {datetime.now()}, Duration: {int(prayer_duration)} seconds\n")
                
    def show_prayer_history(self):
        try:
            with open("prayer_stats.txt", "r") as f:
                history = f.readlines()
            
            history_window = tk.Toplevel(self)
            history_window.title("Riwayat Doa")
            history_window.geometry("400x300")
            
            text_widget = tk.Text(history_window, wrap=tk.WORD)
            text_widget.pack(fill="both", expand=True)
            
            for line in history:
                text_widget.insert(tk.END, line)
                
        except FileNotFoundError:
            messagebox.showinfo("Info", "Belum ada riwayat doa.")
            
    def add_keyboard_shortcuts(self):
        self.bind('<space>', lambda e: self.toggle_prayer())
        self.bind('<Escape>', lambda e: self.quit())
        self.bind('h', lambda e: self.show_prayer_history())
        
    def add_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Riwayat Doa", command=self.show_prayer_history)
        file_menu.add_separator()
        file_menu.add_command(label="Keluar", command=self.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Bantuan", menu=help_menu)
        help_menu.add_command(
            label="Tentang",
            command=lambda: messagebox.showinfo(
                "Tentang",
                "Simulasi Doa Kristen\nVersi 2.0\n\nDibuat dengan ❤️ dan Python"
            )
        )

if __name__ == "__main__":
    app = AdvancedPrayerAnimation()
    app.add_keyboard_shortcuts()
    app.add_menu()
    app.mainloop()