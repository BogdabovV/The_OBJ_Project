import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random

# Список фраз, требующих внимания
CRISIS_PHRASES = [
    "спрыгнуть", "окна", "выброшусь", "прыгну", "покончить", "убить себя",
    "не хочу жить", "смерть", "умереть", "нет смысла", "зачем жить",
    "жизнь кончена", "ненавижу себя"
]

def crisis_detected(text):
    t = text.lower()
    return any(p in t for p in CRISIS_PHRASES)

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

    def build(self):
        tk.Label(self.window, text="Психологическая помощь", font=("Segoe UI", 20, "bold"),
                 bg=self.colors["bg"], fg=self.colors["primary"]).pack(pady=10)

        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Вкладка чата
        chat_tab = tk.Frame(notebook, bg=self.colors["surface"])
        notebook.add(chat_tab, text="Чат с психологом")

        self.chat = scrolledtext.ScrolledText(chat_tab, height=15, bg=self.colors["surface2"],
                                              fg=self.colors["text"], wrap=tk.WORD, font=("Segoe UI", 11))
        self.chat.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.chat.insert(tk.END, "Психолог: Здравствуйте! Расскажите, что вас беспокоит.\n\n")
        self.chat.config(state=tk.DISABLED)

        # Быстрые кнопки
        mood_frame = tk.Frame(chat_tab, bg=self.colors["surface"])
        mood_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(mood_frame, text="Быстрый ответ:", bg=self.colors["surface"], fg=self.colors["text"]).pack(side=tk.LEFT)
        for mood, color in [("Отлично", self.colors["success"]), ("Нормально", self.colors["primary"]),
                            ("Плохо", self.colors["danger"]), ("Нужна помощь", self.colors["danger"])]:
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
        tk.Button(input_frame, text="Отправить", bg=self.colors["primary"], fg="white",
                  relief=tk.FLAT, command=self.send_message).pack(side=tk.RIGHT, padx=5)

        # Вкладка медитаций
        med_tab = tk.Frame(notebook, bg=self.colors["surface"])
        notebook.add(med_tab, text="Медитации")
        meditations = [
            ("Дыхание 4-7-8", "Вдох 4с, задержка 7с, выдох 8с"),
            ("Снятие напряжения", "Напрячь всё тело на 5с → расслабиться. 3 раза"),
            ("Успокаивающая музыка", "Включите спокойную музыку на 10 минут")
        ]
        for name, desc in meditations:
            frame = tk.Frame(med_tab, bg=self.colors["surface2"], relief=tk.RIDGE, bd=1)
            frame.pack(fill=tk.X, padx=20, pady=5)
            tk.Label(frame, text=name, font=("Segoe UI", 12, "bold"),
                     bg=self.colors["surface2"], fg=self.colors["primary"]).pack(anchor=tk.W, padx=10, pady=5)
            tk.Label(frame, text=desc, bg=self.colors["surface2"], fg=self.colors["text2"], justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=5)
            tk.Button(frame, text="Начать", bg=self.colors["success"], fg="black", relief=tk.FLAT,
                      command=lambda d=desc: messagebox.showinfo("Медитация", d)).pack(anchor=tk.E, padx=10, pady=5)

        # Вкладка тестов
        test_tab = tk.Frame(notebook, bg=self.colors["surface"])
        notebook.add(test_tab, text="Тесты")
        tests = [("Тест на ПТСР", self.test_ptsd), ("Тест на депрессию", self.test_depression),
                 ("Тест на тревожность", self.test_anxiety)]
        for name, cmd in tests:
            tk.Button(test_tab, text=name, bg=self.colors["primary"], fg="white", relief=tk.FLAT,
                      height=2, width=30, command=cmd).pack(pady=10)

    def send_message(self, msg=None):
        if msg is None:
            msg = self.entry.get().strip()
        if not msg:
            return

        self.chat.config(state=tk.NORMAL)
        self.chat.insert(tk.END, f"Вы: {msg}\n")

        if crisis_detected(msg):
            response = ("Пожалуйста, не принимайте поспешных решений. Вы не один.\n\n"
                        "📞 Позвоните на кризисную линию: 8-800-XXX-XX-XX\n"
                        "Круглосуточно, анонимно, бесплатно.\n\n"
                        "Я рядом, расскажите, что случилось.")
            self.chat.insert(tk.END, f"Психолог: {response}\n\n")
            self.show_crisis_warning()
        else:
            answers = [
                "Понимаю. Расскажите подробнее.",
                "Спасибо, что делитесь.",
                "Как вы себя чувствуете сейчас?",
                "Я здесь, чтобы поддержать вас.",
                "Что вас беспокоит?"
            ]
            self.chat.insert(tk.END, f"Психолог: {random.choice(answers)}\n\n")

        self.chat.see(tk.END)
        self.chat.config(state=tk.DISABLED)
        self.entry.delete(0, tk.END)

    def show_crisis_warning(self):
        win = tk.Toplevel(self.window)
        win.title("Поддержка")
        win.geometry("450x350")
        win.configure(bg="#1a1a2e")
        win.transient(self.window)
        win.grab_set()
        tk.Label(win, text="Вам нужна помощь", font=("Segoe UI", 16, "bold"),
                 bg="#1a1a2e", fg="#e74c3c").pack(pady=20)
        tk.Label(win, text="Позвоните на кризисную линию:\n\n"
                           "📞 8-800-XXX-XX-XX\n\n"
                           "Круглосуточно, анонимно, бесплатно\n\n"
                           "Вы не один.",
                 bg="#1a1a2e", fg="#cdd6f4", justify=tk.CENTER).pack(pady=10)
        tk.Button(win, text="Закрыть", bg="#4a90e2", fg="white",
                  relief=tk.FLAT, command=win.destroy).pack(pady=20)

    # Тесты
    def test_ptsd(self): self.run_test("ПТСР", ["Кошмары?", "Избегаете мест?", "Легко напугать?"])
    def test_depression(self): self.run_test("Депрессия", ["Грусть?", "Потеря интереса?", "Проблемы со сном?"])
    def test_anxiety(self): self.run_test("Тревога", ["Нервозность?", "Трудно расслабиться?", "Учащённое сердцебиение?"])

    def run_test(self, name, questions):
        win = tk.Toplevel(self.window)
        win.title(name)
        win.geometry("500x450")
        win.configure(bg="#1a1a2e")
        tk.Label(win, text=name, font=("Segoe UI", 16, "bold"), bg="#1a1a2e", fg="#4a90e2").pack(pady=10)
        answers = []
        for q in questions:
            f = tk.Frame(win, bg="#1a1a2e")
            f.pack(fill=tk.X, padx=20, pady=5)
            tk.Label(f, text=q, bg="#1a1a2e", fg="#cdd6f4", wraplength=400).pack(anchor=tk.W)
            var = tk.IntVar(value=0)
            for i, t in enumerate(["Нет", "Иногда", "Часто", "Постоянно"]):
                rb = tk.Radiobutton(f, text=t, variable=var, value=i, bg="#1a1a2e", fg="#cdd6f4", selectcolor="#1a1a2e")
                rb.pack(side=tk.LEFT, padx=5)
            answers.append(var)
        def calc():
            score = sum(v.get() for v in answers)
            maxs = len(questions) * 3
            if score <= maxs * 0.3:
                res = "Низкий уровень. Всё в порядке."
            elif score <= maxs * 0.6:
                res = "Средний уровень. Обратите внимание."
            else:
                res = "Высокий уровень. Рекомендуем обратиться к психологу."
            messagebox.showinfo("Результат", f"Результат: {score} из {maxs}\n\n{res}")
            win.destroy()
        tk.Button(win, text="Узнать результат", bg="#4a90e2", fg="white", relief=tk.FLAT, command=calc).pack(pady=20)