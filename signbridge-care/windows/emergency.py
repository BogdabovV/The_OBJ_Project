import tkinter as tk
from tkinter import messagebox


class EmergencyWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("🆘 Экстренная помощь")
        self.window.geometry("500x400")
        self.window.configure(bg="#1a1a2e")
        self.window.transient(parent)

        self.build()

    def build(self):
        # Красная кнопка
        self.emergency_btn = tk.Button(
            self.window,
            text="🆘 МНЕ ПЛОХО",
            font=("Segoe UI", 20, "bold"),
            bg="#e74c3c",
            fg="white",
            height=3,
            width=20,
            command=self.emergency
        )
        self.emergency_btn.pack(pady=30)

        # Горячие линии
        hotlines_frame = tk.Frame(self.window, bg="#16213e", relief=tk.RIDGE)
        hotlines_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            hotlines_frame,
            text="📞 Горячие линии",
            font=("Segoe UI", 14, "bold"),
            bg="#16213e",
            fg="white"
        ).pack(anchor=tk.W, padx=10, pady=5)

        hotlines = [
            ("Психологическая помощь", "8-800-XXX-XX-XX"),
            ("Скорая помощь", "103"),
            ("Горячая линия Минобороны", "8-800-XXX-XX-XX"),
            ("Фонд Защитники Отечества", "8-800-XXX-XX-XX")
        ]

        for name, phone in hotlines:
            frame = tk.Frame(hotlines_frame, bg="#16213e")
            frame.pack(fill=tk.X, padx=10, pady=3)

            tk.Label(
                frame,
                text=f"{name}:",
                font=("Segoe UI", 11),
                bg="#16213e",
                fg="#a8b2d1"
            ).pack(side=tk.LEFT)

            tk.Label(
                frame,
                text=phone,
                font=("Segoe UI", 11, "bold"),
                bg="#16213e",
                fg="#4a90e2"
            ).pack(side=tk.RIGHT)

        # Ближайшие центры
        centers_frame = tk.Frame(self.window, bg="#16213e", relief=tk.RIDGE)
        centers_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            centers_frame,
            text="🏥 Ближайшие центры",
            font=("Segoe UI", 14, "bold"),
            bg="#16213e",
            fg="white"
        ).pack(anchor=tk.W, padx=10, pady=5)

        centers = [
            "Центр реабилитации ветеранов - Москва, ул. Ленина, 10",
            "Психологический центр - Москва, ул. Мира, 5"
        ]

        for c in centers:
            tk.Label(
                centers_frame,
                text=c,
                font=("Segoe UI", 10),
                bg="#16213e",
                fg="#a8b2d1"
            ).pack(anchor=tk.W, padx=10, pady=3)

        # Кнопка геолокации
        tk.Button(
            centers_frame,
            text="📍 Найти рядом",
            bg="#f39c12",
            fg="white",
            command=self.find_nearby
        ).pack(pady=10)

    def emergency(self):
        result = messagebox.askyesno(
            "Экстренная помощь",
            "Вы действительно хотите вызвать помощь?\n\nВам позвонят в ближайшее время"
        )
        if result:
            messagebox.showinfo("Помощь", "Специалист свяжется с вами в течение 5 минут. Вы не один!")

    def find_nearby(self):
        messagebox.showinfo("Геолокация", "Ближайшие центры помощи загружаются...")