import tkinter as tk
from tkinter import ttk, messagebox

class RehabWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Реабилитация")
        self.window.geometry("600x500")
        self.window.configure(bg="#0f0f1a")

        self.colors = {
            "bg": "#0f0f1a", "surface": "#1a1a2e", "surface2": "#16213e",
            "primary": "#4a90e2", "success": "#2ecc71", "danger": "#e74c3c",
            "text": "#cdd6f4", "text2": "#a8b2d1"
        }

        self.build()

    def build(self):
        tk.Label(self.window, text="Реабилитация", font=("Segoe UI", 20, "bold"),
                 bg=self.colors["bg"], fg=self.colors["success"]).pack(pady=10)

        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Упражнения
        ex_tab = tk.Frame(notebook, bg=self.colors["surface"])
        notebook.add(ex_tab, text="Упражнения")

        categories = [
            ("Ноги", ["Подъёмы на носки (15 раз)", "Махи ногой (10 раз)", "Приседания у стены (10 раз)"]),
            ("Руки", ["Сгибание рук (12 раз)", "Разведение рук (10 раз)", "Вращение кистями (20 раз)"]),
            ("Дыхание", ["Диафрагмальное дыхание (5 мин)", "Дыхание 4-7-8", "Квадратное дыхание"]),
            ("Ходьба", ["Ходьба на месте (1 мин)", "Ходьба с пятки на носок (2 мин)", "Баланс на одной ноге (30 сек)"])
        ]

        for cat, exs in categories:
            frame = tk.Frame(ex_tab, bg=self.colors["surface2"], relief=tk.RIDGE, bd=1)
            frame.pack(fill=tk.X, padx=20, pady=5)
            tk.Label(frame, text=cat, font=("Segoe UI", 12, "bold"),
                     bg=self.colors["surface2"], fg=self.colors["primary"]).pack(anchor=tk.W, padx=10, pady=5)
            for ex in exs:
                row = tk.Frame(frame, bg=self.colors["surface2"])
                row.pack(fill=tk.X, padx=10, pady=2)
                tk.Label(row, text=f"• {ex}", bg=self.colors["surface2"], fg=self.colors["text"]).pack(side=tk.LEFT)
                tk.Button(row, text="Выполнить", bg=self.colors["success"], fg="black", relief=tk.FLAT,
                          command=lambda e=ex: messagebox.showinfo("Упражнение", e)).pack(side=tk.RIGHT, padx=5)

        # Советы
        tips_tab = tk.Frame(notebook, bg=self.colors["surface"])
        notebook.add(tips_tab, text="Советы")
        tips = [
            "Начинайте с малого и постепенно увеличивайте нагрузку",
            "Пейте воду до и после упражнений",
            "Отдыхайте между подходами 30-60 секунд",
            "Не сравнивайте себя с другими — важен ваш прогресс",
            "Занимайтесь регулярно, лучше каждый день понемногу",
            "Прислушивайтесь к своему телу и не делайте через боль"
        ]
        for tip in tips:
            tk.Label(tips_tab, text=tip, bg=self.colors["surface2"], fg=self.colors["text2"],
                     font=("Segoe UI", 10), wraplength=500, justify=tk.LEFT).pack(anchor=tk.W, padx=20, pady=5)