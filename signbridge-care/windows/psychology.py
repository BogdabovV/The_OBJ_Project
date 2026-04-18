import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random


class PsychologyWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Психологическая помощь")
        self.window.geometry("750x600")
        self.window.configure(bg="#0f0f1a")

        self.colors = {
            "bg": "#0f0f1a", "surface": "#1a1a2e", "surface2": "#16213e",
            "primary": "#4a90e2", "success": "#2ecc71", "danger": "#e74c3c",
            "text": "#cdd6f4", "text2": "#a8b2d1"
        }

        self.build()

    def check_crisis(self, text):
        crisis_words = ["спрыгнуть", "окна", "выброшусь", "прыгну", "покончить",
                        "убить себя", "не хочу жить", "смерть", "умереть", "покончу",
                        "жизнь не имеет смысла", "нет смысла жить", "зачем жить"]
        for w in crisis_words:
            if w in text.lower():
                return True
        return False

    def build(self):
        tk.Label(self.window, text="Психологическая помощь", font=("Segoe UI", 20, "bold"),
                 bg=self.colors["bg"], fg=self.colors["primary"]).pack(pady=10)

        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Чат
        chat_tab = tk.Frame(notebook, bg=self.colors["surface"])
        notebook.add(chat_tab, text="Чат с психологом")

        self.chat = scrolledtext.ScrolledText(chat_tab, height=15, bg=self.colors["surface2"],
                                              fg=self.colors["text"], wrap=tk.WORD, font=("Segoe UI", 11))
        self.chat.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.chat.insert(tk.END, "👨‍⚕️ Психолог: Здравствуйте! Я здесь, чтобы помочь.\n\n")
        self.chat.insert(tk.END, "Расскажите, что вас беспокоит. Я внимательно слушаю.\n\n")
        self.chat.config(state=tk.DISABLED)

        # Быстрые ответы
        mood_frame = tk.Frame(chat_tab, bg=self.colors["surface"])
        mood_frame.pack(fill=tk.X, padx=10, pady=5)

        moods = [("Отлично", self.colors["success"]), ("Нормально", self.colors["primary"]),
                 ("Плохо", self.colors["danger"]), ("Нужна помощь", self.colors["danger"])]
        for mood, color in moods:
            btn = tk.Button(mood_frame, text=mood, bg=color, fg="white", relief=tk.FLAT,
                            command=lambda m=mood: self.send_message(m))
            btn.pack(side=tk.LEFT, padx=5)

        # Поле ввода
        input_frame = tk.Frame(chat_tab, bg=self.colors["surface"])
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        self.entry = tk.Entry(input_frame, bg=self.colors["surface2"], fg=self.colors["text"],
                              font=("Segoe UI", 11), relief=tk.FLAT)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.entry.bind("<Return>", lambda e: self.send_message())

        send_btn = tk.Button(input_frame, text="Отправить", bg=self.colors["primary"], fg="white",
                             relief=tk.FLAT, command=self.send_message)
        send_btn.pack(side=tk.RIGHT, padx=5)

        # Медитации
        med_tab = tk.Frame(notebook, bg=self.colors["surface"])
        notebook.add(med_tab, text="Медитации")

        meditations = [
            ("Дыхание 4-7-8", "Вдох на 4 секунды\nЗадержка на 7 секунд\nВыдох на 8 секунд\nПовторить 5 раз"),
            ("Снятие напряжения", "Напрягите все мышцы на 5 секунд\nЗатем резко расслабьтесь\nПовторить 3 раза"),
            ("Успокаивающая музыка", "Включите спокойную музыку\nЗакройте глаза\nСлушайте 10 минут"),
            ("Прогулка в лесу", "Представьте, что вы в лесу\nСлышите пение птиц\nЧувствуете свежий воздух"),
            ("Медитация на 5 минут", "Сядьте удобно\nЗакройте глаза\nСосредоточьтесь на дыхании")
        ]

        for name, desc in meditations:
            frame = tk.Frame(med_tab, bg=self.colors["surface2"], relief=tk.RIDGE, bd=1)
            frame.pack(fill=tk.X, padx=20, pady=5)
            tk.Label(frame, text=name, font=("Segoe UI", 12, "bold"),
                     bg=self.colors["surface2"], fg=self.colors["primary"]).pack(anchor=tk.W, padx=10, pady=5)
            tk.Label(frame, text=desc, bg=self.colors["surface2"], fg=self.colors["text2"],
                     justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=5)
            tk.Button(frame, text="Начать", bg=self.colors["success"], fg="black",
                      relief=tk.FLAT, command=lambda d=desc: messagebox.showinfo("Медитация", d)).pack(anchor=tk.E,
                                                                                                       padx=10, pady=5)

        # Тесты
        test_tab = tk.Frame(notebook, bg=self.colors["surface"])
        notebook.add(test_tab, text="Тесты")

        tests = [
            ("Тест на ПТСР", self.test_ptsd),
            ("Тест на депрессию", self.test_depression),
            ("Тест на тревожность", self.test_anxiety)
        ]

        for name, cmd in tests:
            btn = tk.Button(test_tab, text=name, bg=self.colors["primary"], fg="white",
                            relief=tk.FLAT, height=2, width=30, command=cmd)
            btn.pack(pady=10)

    def send_message(self, msg=None):
        if msg is None:
            msg = self.entry.get().strip()
        if not msg:
            return

        self.chat.config(state=tk.NORMAL)
        self.chat.insert(tk.END, f"Вы: {msg}\n")

        if self.check_crisis(msg):
            response = """❗ Я слышу, что вам очень тяжело. Пожалуйста, НЕ ПРИНИМАЙТЕ поспешных решений.

💛 ВЫ НЕ ОДИН. Ваша жизнь ценна.

НЕМЕДЛЕННО позвоните на кризисную линию: 8-800-XXX-XX-XX
Специалисты готовы помочь вам 24/7.

Давайте сделаем глубокий вдох вместе. Я здесь, я слушаю вас."""
            self.chat.insert(tk.END, f"👨‍⚕️ Психолог: {response}\n\n")
            self.show_crisis_warning()
        else:
            responses = [
                "Понимаю вас. Расскажите подробнее.",
                "Спасибо, что делитесь. Это очень важно.",
                "Как вы себя чувствуете сейчас?",
                "Что помогает вам справляться?",
                "Я здесь, чтобы поддержать вас.",
                "Расскажите, что произошло.",
                "Ваши чувства абсолютно нормальны."
            ]
            self.chat.insert(tk.END, f"👨‍⚕️ Психолог: {random.choice(responses)}\n\n")

        self.chat.see(tk.END)
        self.chat.config(state=tk.DISABLED)
        self.entry.delete(0, tk.END)

    def show_crisis_warning(self):
        win = tk.Toplevel(self.window)
        win.title("❗ Кризисное предупреждение")
        win.geometry("450x350")
        win.configure(bg="#1a1a2e")
        win.transient(self.window)
        win.grab_set()

        tk.Label(win, text="🆘 ВАЖНОЕ ПРЕДУПРЕЖДЕНИЕ", font=("Segoe UI", 16, "bold"),
                 bg="#1a1a2e", fg="#e74c3c").pack(pady=20)

        tk.Label(win, text="Пожалуйста, немедленно позвоните на кризисную линию:\n\n"
                           "📞 8-800-XXX-XX-XX\n\n"
                           "Круглосуточно, анонимно, бесплатно\n\n"
                           "Вы не один. Помощь рядом.",
                 bg="#1a1a2e", fg="#cdd6f4", justify=tk.CENTER).pack(pady=10)

        tk.Button(win, text="Я понял, спасибо", bg="#4a90e2", fg="white",
                  relief=tk.FLAT, command=win.destroy).pack(pady=20)

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
        win = tk.Toplevel(self.window)
        win.title(name)
        win.geometry("500x450")
        win.configure(bg="#1a1a2e")

        tk.Label(win, text=name, font=("Segoe UI", 16, "bold"),
                 bg="#1a1a2e", fg="#4a90e2").pack(pady=10)

        answers = []
        for q in questions:
            frame = tk.Frame(win, bg="#1a1a2e")
            frame.pack(fill=tk.X, padx=20, pady=5)
            tk.Label(frame, text=q, bg="#1a1a2e", fg="#cdd6f4", wraplength=400).pack(anchor=tk.W)

            var = tk.IntVar(value=0)
            for i, text in enumerate(["Нет", "Иногда", "Часто", "Постоянно"]):
                rb = tk.Radiobutton(frame, text=text, variable=var, value=i,
                                    bg="#1a1a2e", fg="#cdd6f4", selectcolor="#1a1a2e")
                rb.pack(side=tk.LEFT, padx=5)
            answers.append(var)

        def calculate():
            score = sum(v.get() for v in answers)
            max_score = len(questions) * 3
            if score <= max_score * 0.3:
                result = "Низкий уровень. Вы в порядке!"
                color = "#2ecc71"
            elif score <= max_score * 0.6:
                result = "Средний уровень. Обратите внимание на своё состояние."
                color = "#f39c12"
            else:
                result = "Высокий уровень. Рекомендуем обратиться к психологу."
                color = "#e74c3c"

            messagebox.showinfo("Результат", f"Ваш результат: {score} из {max_score}\n\n{result}")
            win.destroy()

        tk.Button(win, text="Узнать результат", bg="#4a90e2", fg="white",
                  relief=tk.FLAT, command=calculate).pack(pady=20)