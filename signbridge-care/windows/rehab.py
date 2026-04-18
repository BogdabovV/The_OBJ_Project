import tkinter as tk
from tkinter import ttk, messagebox
import random


class RehabWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Реабилитация")
        self.window.geometry = "650x550"
        self.window.configure(bg="#0f0f1a")

        self.current_exercise = None
        self.score = 0

        self.colors = {
            "bg": "#0f0f1a", "surface": "#1a1a2e", "surface2": "#16213e",
            "primary": "#4a90e2", "success": "#2ecc71", "warning": "#f39c12",
            "danger": "#e74c3c", "text": "#cdd6f4", "text2": "#a8b2d1"
        }

        self.build()

    def build(self):
        tk.Label(self.window, text="Реабилитация", font=("Segoe UI", 20, "bold"),
                 bg=self.colors["bg"], fg=self.colors["success"]).pack(pady=10)

        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Вкладка с упражнениями
        ex_tab = tk.Frame(notebook, bg=self.colors["surface"])
        notebook.add(ex_tab, text="Упражнения")

        categories = [
            ("🦵 Для ног", self.leg_exercises),
            ("💪 Для рук", self.arm_exercises),
            ("🧘 Дыхательные", self.breathing_exercises),
            ("🚶 Ходьба и баланс", self.walking_exercises)
        ]

        for cat_name, cat_func in categories:
            frame = tk.Frame(ex_tab, bg=self.colors["surface2"], relief=tk.RIDGE, bd=1)
            frame.pack(fill=tk.X, padx=20, pady=5)

            tk.Label(frame, text=cat_name, font=("Segoe UI", 12, "bold"),
                     bg=self.colors["surface2"], fg=self.colors["primary"]).pack(anchor=tk.W, padx=10, pady=5)

            exercises = cat_func()
            for ex_name, ex_desc in exercises[:3]:
                ex_frame = tk.Frame(frame, bg=self.colors["surface2"])
                ex_frame.pack(fill=tk.X, padx=10, pady=2)
                tk.Label(ex_frame, text=f"• {ex_name}", bg=self.colors["surface2"], fg=self.colors["text"]).pack(
                    side=tk.LEFT)
                tk.Button(ex_frame, text="Выполнить", bg=self.colors["success"], fg="black",
                          relief=tk.FLAT, command=lambda d=ex_desc, n=ex_name: self.start_exercise(n, d)).pack(
                    side=tk.RIGHT, padx=5)

        # Вкладка с прогрессом
        prog_tab = tk.Frame(notebook, bg=self.colors["surface"])
        notebook.add(prog_tab, text="Мой прогресс")

        tk.Label(prog_tab, text="📊 Статистика тренировок", font=("Segoe UI", 14, "bold"),
                 bg=self.colors["surface"], fg=self.colors["primary"]).pack(pady=10)

        self.progress_text = tk.Text(prog_tab, height=10, bg=self.colors["surface2"],
                                     fg=self.colors["text"], relief=tk.FLAT, wrap=tk.WORD)
        self.progress_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.progress_text.insert(tk.END, "Начните выполнять упражнения, чтобы отслеживать прогресс!\n\n")
        self.progress_text.config(state=tk.DISABLED)

        tk.Button(prog_tab, text="Обновить", bg=self.colors["primary"], fg="white",
                  relief=tk.FLAT, command=self.update_progress).pack(pady=10)

        # Советы
        tips_tab = tk.Frame(notebook, bg=self.colors["surface"])
        notebook.add(tips_tab, text="Советы")

        tips = [
            "🌟 Начинайте с малого и постепенно увеличивайте нагрузку",
            "💧 Пейте воду до и после упражнений",
            "🛌 Отдыхайте между подходами 30-60 секунд",
            "🎯 Не сравнивайте себя с другими - важен ваш прогресс",
            "📅 Занимайтесь регулярно, лучше каждый день понемногу",
            "😊 Прислушивайтесь к своему телу и не делайте через боль"
        ]

        for tip in tips:
            tk.Label(tips_tab, text=tip, bg=self.colors["surface2"], fg=self.colors["text2"],
                     font=("Segoe UI", 11), wraplength=500, justify=tk.LEFT).pack(anchor=tk.W, padx=20, pady=5)

    def leg_exercises(self):
        return [
            ("Подъёмы на носки",
             "Встаньте прямо, медленно поднимитесь на носки, задержитесь на 2 секунды, опуститесь. 15 раз."),
            ("Махи ногой", "Держась за опору, делайте махи ногой вперёд-назад. 10 раз каждой ногой."),
            ("Приседания у стены", "Прислонитесь спиной к стене, медленно приседайте. 10 раз."),
            ("Сгибание ног лёжа", "Лёжа на спине, сгибайте ноги в коленях, скользя пятками по полу. 15 раз.")
        ]

    def arm_exercises(self):
        return [
            ("Сгибание рук", "Сидя, сгибайте руки в локтях (можно с лёгкими гантелями). 12 раз."),
            ("Разведение рук", "Разводите прямые руки в стороны и сводите перед собой. 10 раз."),
            ("Вращение кистями", "Вращайте кистями рук сначала в одну, потом в другую сторону. 20 раз."),
            ("Подъём рук вверх", "Поднимайте прямые руки вверх через стороны. 10 раз.")
        ]

    def breathing_exercises(self):
        return [
            ("Диафрагмальное дыхание",
             "Лягте, положите руку на живот. Медленно вдохните носом (живот поднимается), выдохните ртом. 5 минут."),
            ("Дыхание 4-7-8", "Вдох на 4 счёта, задержка на 7, выдох на 8. Повторить 5 раз."),
            ("Квадратное дыхание", "Вдох 4 с, задержка 4 с, выдох 4 с, задержка 4 с. Повторить 5 раз.")
        ]

    def walking_exercises(self):
        return [
            ("Ходьба на месте", "Маршируйте на месте, высоко поднимая колени. 1 минута."),
            ("Ходьба с пятки на носок", "Ходите, перекатываясь с пятки на носок. 2 минуты."),
            ("Баланс на одной ноге", "Встаньте на одну ногу, держитесь за опору. 30 секунд, затем смените ногу.")
        ]

    def start_exercise(self, name, desc):
        self.current_exercise = name

        win = tk.Toplevel(self.window)
        win.title(f"Упражнение: {name}")
        win.geometry = "500x400"
        win.configure(bg="#1a1a2e")
        win.transient(self.window)
        win.grab_set()

        tk.Label(win, text=name, font=("Segoe UI", 18, "bold"),
                 bg="#1a1a2e", fg="#2ecc71").pack(pady=20)

        tk.Label(win, text=desc, bg="#1a1a2e", fg="#cdd6f4",
                 wraplength=400, justify=tk.CENTER).pack(pady=10)

        tk.Label(win, text="Как выполнили?", font=("Segoe UI", 12, "bold"),
                 bg="#1a1a2e", fg="#cdd6f4").pack(pady=20)

        def rate(value):
            self.score += value
            messagebox.showinfo("Отлично!", f"Вы выполнили упражнение!\n\nПолучено +{value} баллов")
            win.destroy()
            self.save_progress(name, value)

        btn_frame = tk.Frame(win, bg="#1a1a2e")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="👍 Отлично", bg="#2ecc71", fg="black",
                  relief=tk.FLAT, command=lambda: rate(10)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="😐 Нормально", bg="#f39c12", fg="black",
                  relief=tk.FLAT, command=lambda: rate(5)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="👎 Сложно", bg="#e74c3c", fg="white",
                  relief=tk.FLAT, command=lambda: rate(2)).pack(side=tk.LEFT, padx=5)

    def save_progress(self, name, points):
        import json
        import os
        from datetime import datetime

        progress_file = "data/progress.json"
        if os.path.exists(progress_file):
            with open(progress_file, "r", encoding="utf-8") as f:
                progress = json.load(f)
        else:
            progress = {"total": 0, "exercises": [], "history": []}

        progress["total"] += points
        progress["exercises"].append(
            {"name": name, "points": points, "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
        progress["history"].append(f"{datetime.now().strftime('%d.%m %H:%M')} - {name} +{points} баллов")

        if len(progress["history"]) > 20:
            progress["history"] = progress["history"][-20:]

        with open(progress_file, "w", encoding="utf-8") as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)

    def update_progress(self):
        import json
        import os

        self.progress_text.config(state=tk.NORMAL)
        self.progress_text.delete("1.0", tk.END)

        if os.path.exists("data/progress.json"):
            with open("data/progress.json", "r", encoding="utf-8") as f:
                progress = json.load(f)

            self.progress_text.insert(tk.END, f"🏆 Всего баллов: {progress.get('total', 0)}\n\n")
            self.progress_text.insert(tk.END, "📋 Последние тренировки:\n")
            for h in progress.get("history", [])[-10:]:
                self.progress_text.insert(tk.END, f"  • {h}\n")
        else:
            self.progress_text.insert(tk.END, "Начните выполнять упражнения, чтобы отслеживать прогресс!\n\n")

        self.progress_text.config(state=tk.DISABLED)