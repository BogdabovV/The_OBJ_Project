import tkinter as tk
from tkinter import messagebox


class SocialWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("🏠 Социальная адаптация")
        self.window.geometry("600x450")
        self.window.configure(bg="#0f0f1a")

        tk.Label(
            self.window, text="🏠 Социальная адаптация", font=("Segoe UI", 20, "bold"),
            bg="#0f0f1a", fg="#4a90e2"
        ).pack(pady=20)

        events = ["🎯 Встреча ветеранов - 25 марта", "🏃 Спортивный день - 27 марта", "🎨 Мастер-класс - 30 марта"]
        for e in events:
            tk.Label(self.window, text=e, font=("Segoe UI", 12), bg="#0f0f1a", fg="#a8b2d1").pack(anchor=tk.W, padx=30,
                                                                                                  pady=5)

        tk.Label(self.window, text="🎯 Клубы по интересам", font=("Segoe UI", 14, "bold"), bg="#0f0f1a",
                 fg="#f39c12").pack(pady=(20, 10))

        clubs = ["🎮 Настольные игры", "📚 Литературный клуб", "🎬 Киноклуб"]
        for c in clubs:
            tk.Button(self.window, text=c, bg="#16213e", fg="#cdd6f4", relief=tk.FLAT,
                      command=lambda t=c: messagebox.showinfo("Клуб", f"Вы записаны в клуб: {t}")).pack(pady=3)