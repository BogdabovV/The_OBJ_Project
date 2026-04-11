import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random


class PsychologyWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("🧠 Психологическая помощь")
        self.window.geometry("800x600")
        self.window.configure(bg="#1a1a2e")
        self.window.transient(parent)

        self.build()

    def build(self):
        tk.Label(
            self.window,
            text="🧠 Психологическая помощь",
            font=("Segoe UI", 20, "bold"),
            bg="#1a1a2e",
            fg="#4a90e2"
        ).pack(pady=10)

        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Чат
        chat_frame = tk.Frame(notebook, bg="#16213e")
        notebook.add(chat_frame, text="💬 Чат с психологом")

        self.chat_area = scrolledtext.ScrolledText(
            chat_frame,
            height=15,
            bg="#0f172a",
            fg="white",
            font=("Segoe UI", 11)
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.chat_area.insert(tk.END,
                              "Психолог: Здравствуйте! Я здесь, чтобы помочь. Расскажите, что вас беспокоит?\n\n")
        self.chat_area.config(state=tk.DISABLED)

        input_frame = tk.Frame(chat_frame, bg="#16213e")
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        self.msg_entry = tk.Entry(
            input_frame,
            font=("Segoe UI", 11),
            bg="#0f172a",
            fg="white"
        )
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.msg_entry.bind("<Return>", self.send_message)

        tk.Button(
            input_frame,
            text="Отправить",
            bg="#4a90e2",
            fg="white",
            command=self.send_message
        ).pack(side=tk.RIGHT, padx=5)

        # Медитации
        meditation_frame = tk.Frame(notebook, bg="#16213e")
        notebook.add(meditation_frame, text="🧘 Медитации")

        meditations = [
            "🌊 Дыхание на счет 4-7-8",
            "🎵 Успокаивающая музыка",
            "🧘 Медитация на 5 минут",
            "🌿 Прогулка в лесу (аудио)"
        ]

        for m in meditations:
            btn = tk.Button(
                meditation_frame,
                text=m,
                font=("Segoe UI", 12),
                bg="#2c3e50",
                fg="white",
                width=30,
                height=2,
                command=lambda t=m: self.start_meditation(t)
            )
            btn.pack(pady=10)

        # Дневник
        mood_frame = tk.Frame(notebook, bg="#16213e")
        notebook.add(mood_frame, text="📔 Дневник")

        tk.Label(
            mood_frame,
            text="Как прошёл ваш день?",
            font=("Segoe UI", 14),
            bg="#16213e",
            fg="white"
        ).pack(pady=10)

        self.diary_text = scrolledtext.ScrolledText(
            mood_frame,
            height=8,
            bg="#0f172a",
            fg="white"
        )
        self.diary_text.pack(fill=tk.X, padx=20, pady=10)

        tk.Button(
            mood_frame,
            text="Сохранить запись",
            bg="#2ecc71",
            fg="white",
            command=self.save_diary
        ).pack(pady=5)

        # Тесты
        test_frame = tk.Frame(notebook, bg="#16213e")
        notebook.add(test_frame, text="📊 Тесты")

        tests = [
            ("Тест на ПТСР", self.test_ptsd),
            ("Тест на депрессию", self.test_depression),
            ("Тест на тревожность", self.test_anxiety)
        ]

        for name, cmd in tests:
            tk.Button(
                test_frame,
                text=name,
                font=("Segoe UI", 12),
                bg="#f39c12",
                fg="white",
                width=30,
                height=2,
                command=cmd
            ).pack(pady=10)

        # Группы
        group_frame = tk.Frame(notebook, bg="#16213e")
        notebook.add(group_frame, text="👥 Группы поддержки")

        groups = [
            "🗓️ Встреча ветеранов (вторник 19:00)",
            "🗓️ Группа для семей (среда 20:00)",
            "🗓️ Чат поддержки (ежедневно)",
            "🗓️ Клуб по интересам (суббота 15:00)"
        ]

        for g in groups:
            tk.Label(
                group_frame,
                text=g,
                font=("Segoe UI", 11),
                bg="#16213e",
                fg="#a8b2d1"
            ).pack(anchor=tk.W, padx=20, pady=5)

    def send_message(self, event=None):
        msg = self.msg_entry.get().strip()
        if msg:
            self.chat_area.config(state=tk.NORMAL)
            self.chat_area.insert(tk.END, f"Вы: {msg}\n")

            answers = [
                "Понимаю вас. Расскажите подробнее.",
                "Спасибо, что делитесь. Это важно.",
                "Как вы себя чувствуете сейчас?",
                "Что помогает вам справляться?",
                "Я с вами. Продолжайте."
            ]
            answer = random.choice(answers)
            self.chat_area.insert(tk.END, f"Психолог: {answer}\n\n")

            self.chat_area.see(tk.END)
            self.chat_area.config(state=tk.DISABLED)
            self.msg_entry.delete(0, tk.END)

    def start_meditation(self, name):
        messagebox.showinfo("Медитация", f"Начинаем: {name}\n\nСделайте глубокий вдох...")

    def save_diary(self):
        text = self.diary_text.get("1.0", tk.END).strip()
        if text:
            messagebox.showinfo("Сохранено", "Ваша запись сохранена")
            self.diary_text.delete("1.0", tk.END)

    def test_ptsd(self):
        self.run_test("Тест на ПТСР", [
            "Вам снятся кошмары о пережитом?",
            "Вы избегаете мест, напоминающих о прошлом?",
            "Вас легко напугать?",
            "Вы чувствуете себя оторванным от других?"
        ])

    def test_depression(self):
        self.run_test("Тест на депрессию", [
            "Вы чувствуете грусть большую часть дня?",
            "Вам неинтересны вещи, которые раньше нравились?",
            "У вас проблемы со сном?",
            "Вы чувствуете усталость и упадок сил?"
        ])

    def test_anxiety(self):
        self.run_test("Тест на тревожность", [
            "Вы часто нервничаете без причины?",
            "Вам трудно расслабиться?",
            "У вас бывает учащенное сердцебиение?",
            "Вы постоянно переживаете о будущем?"
        ])

    def run_test(self, name, questions):
        test_win = tk.Toplevel(self.window)
        test_win.title(name)
        test_win.geometry("500x400")
        test_win.configure(bg="#1a1a2e")

        tk.Label(
            test_win,
            text=name,
            font=("Segoe UI", 16, "bold"),
            bg="#1a1a2e",
            fg="#4a90e2"
        ).pack(pady=10)

        answers = []

        for q in questions:
            frame = tk.Frame(test_win, bg="#1a1a2e")
            frame.pack(fill=tk.X, padx=20, pady=5)

            tk.Label(
                frame,
                text=q,
                bg="#1a1a2e",
                fg="white",
                wraplength=400,
                justify=tk.LEFT
            ).pack(anchor=tk.W)

            var = tk.IntVar(value=0)
            frame.var = var

            for i, text in enumerate(["Нет", "Иногда", "Часто", "Постоянно"]):
                tk.Radiobutton(
                    frame,
                    text=text,
                    variable=var,
                    value=i,
                    bg="#1a1a2e",
                    fg="white",
                    selectcolor="#1a1a2e"
                ).pack(side=tk.LEFT, padx=5)

            answers.append(var)

        def calculate():
            score = sum(v.get() for v in answers)
            if score <= 4:
                result = "Низкий уровень. Вы в порядке!"
            elif score <= 8:
                result = "Средний уровень. Обратите внимание на своё состояние."
            else:
                result = "Высокий уровень. Рекомендуем обратиться к психологу."

            messagebox.showinfo("Результат", f"Ваш результат: {score} из 12\n\n{result}")
            test_win.destroy()

        tk.Button(
            test_win,
            text="Узнать результат",
            bg="#4a90e2",
            fg="white",
            command=calculate
        ).pack(pady=20)