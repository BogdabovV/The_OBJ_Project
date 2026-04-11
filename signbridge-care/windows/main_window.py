import tkinter as tk
from tkinter import messagebox


class MainWindow:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller  # это SignBridgeCare
        self.frame = tk.Frame(parent, bg="#1a1a2e")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.build()

    def build(self):
        # Шапка
        header = tk.Frame(self.frame, bg="#16213e", height=80)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="🤝 SignBridge Care",
            font=("Segoe UI", 24, "bold"),
            bg="#16213e",
            fg="#4a90e2"
        ).pack(side=tk.LEFT, padx=20, pady=15)

        tk.Label(
            header,
            text="Помощь ветеранам и их семьям",
            font=("Segoe UI", 12),
            bg="#16213e",
            fg="#a8b2d1"
        ).pack(side=tk.LEFT, padx=10)

        # Меню
        menu_frame = tk.Frame(self.frame, bg="#1a1a2e")
        menu_frame.pack(fill=tk.X, padx=20, pady=10)

        modules = [
            ("🧠 Психология", self.controller.open_psychology, "#4a90e2"),
            ("🏋️ Реабилитация", self.controller.open_rehab, "#2ecc71"),
            ("⚖️ Юрист", self.controller.open_law, "#9b59b6"),
            ("🏠 Социум", self.controller.open_social, "#e74c3c"),
            ("🆘 Экстренная", self.controller.open_emergency, "#e67e22")
        ]

        for i, (text, cmd, color) in enumerate(modules):
            btn = tk.Button(
                menu_frame,
                text=text,
                font=("Segoe UI", 12, "bold"),
                bg=color,
                fg="white",
                width=16,
                height=2,
                command=cmd
            )
            btn.grid(row=0, column=i, padx=5, pady=10)

        # Статус дня
        mood_frame = tk.Frame(self.frame, bg="#16213e", relief=tk.RIDGE, bd=1)
        mood_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            mood_frame,
            text="😊 Как вы сегодня?",
            font=("Segoe UI", 14, "bold"),
            bg="#16213e",
            fg="white"
        ).pack(side=tk.LEFT, padx=20, pady=10)

        moods = [
            ("😊 Отлично", "#2ecc71"),
            ("😐 Нормально", "#f39c12"),
            ("😔 Плохо", "#e74c3c"),
            ("😢 Нужна помощь", "#e67e22")
        ]

        for text, color in moods:
            btn = tk.Button(
                mood_frame,
                text=text,
                font=("Segoe UI", 11),
                bg=color,
                fg="white",
                command=lambda t=text: self.controller.set_mood(t)
            )
            btn.pack(side=tk.LEFT, padx=5, pady=10)

        # Голосовой помощник
        voice_frame = tk.Frame(self.frame, bg="#1a1a2e")
        voice_frame.pack(fill=tk.X, padx=20, pady=10)

        self.voice_btn = tk.Button(
            voice_frame,
            text="🎤 Спросить как дела",
            font=("Segoe UI", 11),
            bg="#4a90e2",
            fg="white",
            height=2,
            command=self.controller.voice_check
        )
        self.voice_btn.pack(pady=5)

        # История успеха
        story_frame = tk.Frame(self.frame, bg="#2c3e50", relief=tk.RIDGE)
        story_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            story_frame,
            text="🌟 История успеха",
            font=("Segoe UI", 12, "bold"),
            bg="#2c3e50",
            fg="#f1c40f"
        ).pack(anchor=tk.W, padx=10, pady=5)

        tk.Label(
            story_frame,
            text='"После ранения я думал, что жизнь закончилась. SignBridge Care помог найти психолога, пройти реабилитацию. Теперь я помогаю другим!"',
            font=("Segoe UI", 10),
            bg="#2c3e50",
            fg="white",
            wraplength=800
        ).pack(anchor=tk.W, padx=10, pady=5)

        tk.Label(
            story_frame,
            text="— Алексей, ветеран",
            font=("Segoe UI", 9, "italic"),
            bg="#2c3e50",
            fg="#a8b2d1"
        ).pack(anchor=tk.W, padx=10, pady=5)