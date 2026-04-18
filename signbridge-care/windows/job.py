import tkinter as tk
from tkinter import messagebox


class JobWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("💼 Работа")
        self.window.geometry("600x450")
        self.window.configure(bg="#0f0f1a")

        tk.Label(
            self.window, text="💼 Трудоустройство", font=("Segoe UI", 20, "bold"),
            bg="#0f0f1a", fg="#f39c12"
        ).pack(pady=20)

        jobs = [
            ("IT-специалист (удаленно)", "от 80 000 ₽"),
            ("Менеджер по работе с клиентами", "от 60 000 ₽"),
            ("Водитель", "от 70 000 ₽"),
            ("Сборщик заказов (удаленно)", "от 45 000 ₽")
        ]

        for title, salary in jobs:
            frame = tk.Frame(self.window, bg="#1a1a2e", relief=tk.RIDGE, bd=1)
            frame.pack(fill=tk.X, padx=20, pady=5)
            tk.Label(frame, text=title, font=("Segoe UI", 12, "bold"), bg="#1a1a2e", fg="#cdd6f4").pack(anchor=tk.W,
                                                                                                        padx=10, pady=2)
            tk.Label(frame, text=salary, bg="#1a1a2e", fg="#a8b2d1").pack(anchor=tk.W, padx=10, pady=2)
            tk.Button(frame, text="Откликнуться", bg="#4a90e2", fg="white", relief=tk.FLAT,
                      command=lambda t=title: messagebox.showinfo("Отклик", f"Вы откликнулись на: {t}")).pack(
                anchor=tk.E, padx=10, pady=5)

        tk.Label(self.window, text="📚 Бесплатные курсы", font=("Segoe UI", 14, "bold"), bg="#0f0f1a",
                 fg="#2ecc71").pack(pady=(20, 10))

        courses = ["Программирование Python", "Веб-дизайн", "1С Предприятие"]
        for c in courses:
            tk.Button(self.window, text=c, bg="#16213e", fg="#cdd6f4", relief=tk.FLAT,
                      command=lambda t=c: messagebox.showinfo("Курс", f"Вы записаны на курс: {t}")).pack(pady=3)