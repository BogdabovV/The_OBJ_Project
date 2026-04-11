import tkinter as tk
from tkinter import ttk, messagebox


class SocialWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("🏠 Социальная адаптация")
        self.window.geometry("700x500")
        self.window.configure(bg="#1a1a2e")
        self.window.transient(parent)

        self.build()

    def build(self):
        tk.Label(
            self.window,
            text="🏠 Социальная адаптация",
            font=("Segoe UI", 20, "bold"),
            bg="#1a1a2e",
            fg="#e74c3c"
        ).pack(pady=10)

        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Мероприятия
        events_frame = tk.Frame(notebook, bg="#16213e")
        notebook.add(events_frame, text="🗓️ Мероприятия")

        events = [
            "🎯 Встреча ветеранов - 25 марта, 18:00",
            "🏃 Спортивный день - 27 марта, 10:00",
            "🎨 Мастер-класс по рисованию - 30 марта, 15:00",
            "🎵 Концерт - 1 апреля, 17:00"
        ]

        for e in events:
            tk.Label(
                events_frame,
                text=e,
                font=("Segoe UI", 12),
                bg="#16213e",
                fg="#a8b2d1"
            ).pack(anchor=tk.W, padx=20, pady=5)

        # Клубы по интересам
        clubs_frame = tk.Frame(notebook, bg="#16213e")
        notebook.add(clubs_frame, text="🎯 Клубы")

        clubs = [
            "🎮 Клуб настольных игр",
            "📚 Литературный клуб",
            "🎬 Киноклуб",
            "🎵 Музыкальный клуб"
        ]

        for c in clubs:
            btn = tk.Button(
                clubs_frame,
                text=c,
                font=("Segoe UI", 11),
                bg="#2c3e50",
                fg="white",
                width=30,
                command=lambda t=c: self.join_club(t)
            )
            btn.pack(pady=5)

        # Семейный раздел
        family_frame = tk.Frame(notebook, bg="#16213e")
        notebook.add(family_frame, text="👨‍👩‍👧 Семье")

        tips = [
            "Как поддержать близкого после травмы",
            "Советы психолога для семьи",
            "Группа поддержки для родственников",
            "Истории семей, которые прошли через это"
        ]

        for t in tips:
            tk.Label(
                family_frame,
                text=f"📖 {t}",
                font=("Segoe UI", 11),
                bg="#16213e",
                fg="#a8b2d1"
            ).pack(anchor=tk.W, padx=20, pady=5)

    def join_club(self, club):
        messagebox.showinfo("Запись", f"Вы записаны в клуб: {club}\n\nС вами свяжутся организаторы")