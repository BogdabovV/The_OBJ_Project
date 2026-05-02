import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random
import hashlib
import os
import json
import threading
import time
import cv2
import mediapipe as mp
from PIL import Image, ImageTk
from cryptography.fernet import Fernet


# ==================== БЕЗОПАСНОЕ ХРАНЕНИЕ ====================
class SecureStorage:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        key_path = "data/key.key"
        if os.path.exists(key_path):
            with open(key_path, "rb") as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open(key_path, "wb") as f:
                f.write(self.key)
        self.cipher = Fernet(self.key)

    def encrypt(self, data):
        if isinstance(data, dict):
            data = json.dumps(data, ensure_ascii=False)
        if isinstance(data, str):
            data = data.encode()
        return self.cipher.encrypt(data).decode()

    def decrypt(self, data):
        dec = self.cipher.decrypt(data.encode())
        try:
            return json.loads(dec)
        except:
            return dec.decode()

    def save(self, data, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.encrypt(data))

    def load(self, path):
        if not os.path.exists(path):
            return {}
        with open(path, "r", encoding="utf-8") as f:
            enc = f.read()
        return self.decrypt(enc)


# ==================== АВТОРИЗАЦИЯ ====================
class AuthManager:
    def __init__(self):
        self.storage = SecureStorage()
        self.users = self.load_users()
        self.current_user = None

    def load_users(self):
        if os.path.exists("data/users.dat"):
            return self.storage.load("data/users.dat")
        return {}

    def save_users(self):
        self.storage.save(self.users, "data/users.dat")

    def hash_pass(self, pwd):
        return hashlib.sha256(pwd.encode()).hexdigest()

    def register(self, login, pwd):
        if login in self.users:
            return False, "Пользователь уже существует"
        self.users[login] = {"pwd": self.hash_pass(pwd)}
        self.save_users()
        return True, "Регистрация успешна"

    def login(self, login, pwd):
        if login in self.users and self.users[login]["pwd"] == self.hash_pass(pwd):
            self.current_user = login
            return True, login
        return False, "Неверный логин или пароль"


# ==================== КРИЗИСНЫЕ ФРАЗЫ ====================
CRISIS_PHRASES = [
    "спрыгнуть", "окна", "выброшусь", "прыгну", "покончить", "убить себя",
    "не хочу жить", "смерть", "умереть", "нет смысла", "зачем жить",
    "жизнь кончена", "ненавижу себя"
]


def crisis_detected(text):
    t = text.lower()
    return any(p in t for p in CRISIS_PHRASES)


# ==================== ОСНОВНОЕ ПРИЛОЖЕНИЕ ====================
class SignBridgeApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SignBridge Care")
        self.root.geometry("950x700")
        self.root.configure(bg="#0f0f1a")

        self.auth = AuthManager()
        self.current_frame = None
        self.colors = {
            "bg": "#0f0f1a", "surface": "#1a1a2e", "surface2": "#16213e",
            "primary": "#4a90e2", "success": "#2ecc71", "danger": "#e74c3c",
            "text": "#cdd6f4", "text2": "#a8b2d1"
        }

        self.show_login()

    def switch_to(self, frame_class, **kwargs):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame_class(self.root, self, **kwargs)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def go_back(self):
        if self.auth.current_user:
            self.switch_to(MainMenu)
        else:
            self.show_login()

    def show_login(self):
        self.switch_to(LoginScreen)

    def open_psychology(self):
        self.switch_to(PsychologyScreen)

    def open_rehab(self):
        self.switch_to(RehabScreen)

    def open_gesture(self):
        self.switch_to(GestureScreen)

    def run(self):
        self.root.mainloop()


# ==================== ЭКРАН ВХОДА ====================
class LoginScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=app.colors["bg"])
        self.app = app
        self.pack(fill=tk.BOTH, expand=True)

        box = tk.Frame(self, bg=app.colors["surface"], relief=tk.RIDGE, bd=1)
        box.place(relx=0.5, rely=0.5, anchor="center", width=380, height=480)

        tk.Label(box, text="SignBridge Care", font=("Segoe UI", 20, "bold"),
                 bg=app.colors["surface"], fg=app.colors["primary"]).pack(pady=25)

        tk.Label(box, text="Логин", bg=app.colors["surface"], fg=app.colors["text"]).pack(anchor=tk.W, padx=30)
        self.login_entry = tk.Entry(box, bg=app.colors["surface2"], fg=app.colors["text"], relief=tk.FLAT)
        self.login_entry.pack(padx=30, pady=5, fill=tk.X)

        tk.Label(box, text="Пароль", bg=app.colors["surface"], fg=app.colors["text"]).pack(anchor=tk.W, padx=30,
                                                                                           pady=(10, 0))
        pf = tk.Frame(box, bg=app.colors["surface"])
        pf.pack(padx=30, pady=5, fill=tk.X)
        self.pass_entry = tk.Entry(pf, show="*", bg=app.colors["surface2"], fg=app.colors["text"], relief=tk.FLAT)
        self.pass_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.pass_btn = tk.Button(pf, text="👁️", bg=app.colors["surface2"], fg=app.colors["text"],
                                  relief=tk.FLAT, width=3, command=self.toggle_pass)
        self.pass_btn.pack(side=tk.RIGHT, padx=(5, 0))

        tk.Button(box, text="Войти", bg=app.colors["primary"], fg="white",
                  relief=tk.FLAT, height=2, command=self.do_login).pack(fill=tk.X, padx=30, pady=20)

        tk.Frame(box, bg=app.colors["text2"], height=1).pack(fill=tk.X, padx=30, pady=10)
        tk.Label(box, text="Нет аккаунта?", bg=app.colors["surface"], fg=app.colors["text2"]).pack()
        tk.Button(box, text="Регистрация", bg=app.colors["success"], fg="black",
                  relief=tk.FLAT, height=2, command=self.show_register).pack(fill=tk.X, padx=30, pady=10)

    def toggle_pass(self):
        if self.pass_entry.cget('show') == '*':
            self.pass_entry.configure(show='')
            self.pass_btn.configure(text="🔒")
        else:
            self.pass_entry.configure(show='*')
            self.pass_btn.configure(text="👁️")

    def do_login(self):
        login = self.login_entry.get().strip()
        pwd = self.pass_entry.get().strip()
        ok, res = self.app.auth.login(login, pwd)
        if ok:
            self.app.switch_to(MainMenu)
        else:
            messagebox.showerror("Ошибка", res)

    def show_register(self):
        win = tk.Toplevel(self)
        win.title("Регистрация")
        win.geometry("380x480")
        win.configure(bg=self.app.colors["surface"])
        win.transient(self)
        win.grab_set()

        tk.Label(win, text="Регистрация", font=("Segoe UI", 20, "bold"),
                 bg=self.app.colors["surface"], fg=self.app.colors["primary"]).pack(pady=20)

        tk.Label(win, text="Логин", bg=self.app.colors["surface"], fg=self.app.colors["text"]).pack(anchor=tk.W,
                                                                                                    padx=30)
        r_login = tk.Entry(win, bg=self.app.colors["surface2"], fg=self.app.colors["text"], relief=tk.FLAT)
        r_login.pack(padx=30, pady=5, fill=tk.X)

        tk.Label(win, text="Пароль", bg=self.app.colors["surface"], fg=self.app.colors["text"]).pack(anchor=tk.W,
                                                                                                     padx=30)
        pf = tk.Frame(win, bg=self.app.colors["surface"])
        pf.pack(padx=30, pady=5, fill=tk.X)
        r_pass = tk.Entry(pf, show="*", bg=self.app.colors["surface2"], fg=self.app.colors["text"], relief=tk.FLAT)
        r_pass.pack(side=tk.LEFT, fill=tk.X, expand=True)
        pb = tk.Button(pf, text="👁️", bg=self.app.colors["surface2"], fg=self.app.colors["text"],
                       relief=tk.FLAT, width=3, command=lambda: self.toggle_pass_register(r_pass, pb))
        pb.pack(side=tk.RIGHT, padx=(5, 0))

        tk.Label(win, text="Повтор пароля", bg=self.app.colors["surface"], fg=self.app.colors["text"]).pack(anchor=tk.W,
                                                                                                            padx=30)
        pf2 = tk.Frame(win, bg=self.app.colors["surface"])
        pf2.pack(padx=30, pady=5, fill=tk.X)
        r_pass2 = tk.Entry(pf2, show="*", bg=self.app.colors["surface2"], fg=self.app.colors["text"], relief=tk.FLAT)
        r_pass2.pack(side=tk.LEFT, fill=tk.X, expand=True)
        pb2 = tk.Button(pf2, text="👁️", bg=self.app.colors["surface2"], fg=self.app.colors["text"],
                        relief=tk.FLAT, width=3, command=lambda: self.toggle_pass_register(r_pass2, pb2))
        pb2.pack(side=tk.RIGHT, padx=(5, 0))

        def reg():
            login = r_login.get().strip()
            pwd = r_pass.get().strip()
            pwd2 = r_pass2.get().strip()
            if not login or not pwd:
                messagebox.showerror("Ошибка", "Заполните поля")
                return
            if pwd != pwd2:
                messagebox.showerror("Ошибка", "Пароли не совпадают")
                return
            ok, msg = self.app.auth.register(login, pwd)
            if ok:
                messagebox.showinfo("Успех", msg)
                win.destroy()
                self.login_entry.delete(0, tk.END)
                self.login_entry.insert(0, login)
            else:
                messagebox.showerror("Ошибка", msg)

        tk.Button(win, text="Зарегистрироваться", bg=self.app.colors["success"], fg="black",
                  relief=tk.FLAT, height=2, command=reg).pack(fill=tk.X, padx=30, pady=20)

    def toggle_pass_register(self, entry, btn):
        if entry.cget('show') == '*':
            entry.configure(show='')
            btn.configure(text="🔒")
        else:
            entry.configure(show='*')
            btn.configure(text="👁️")


# ==================== ГЛАВНОЕ МЕНЮ ====================
class MainMenu(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=app.colors["bg"])
        self.app = app
        self.pack(fill=tk.BOTH, expand=True)

        header = tk.Frame(self, bg=app.colors["surface2"], height=60)
        header.pack(fill=tk.X)
        tk.Label(header, text="SignBridge Care", font=("Segoe UI", 20, "bold"),
                 bg=app.colors["surface2"], fg=app.colors["primary"]).pack(side=tk.LEFT, padx=20)
        tk.Label(header, text=app.auth.current_user, bg=app.colors["surface2"], fg=app.colors["text2"]).pack(
            side=tk.RIGHT, padx=20)
        tk.Button(header, text="Выйти", bg=app.colors["danger"], fg="white",
                  relief=tk.FLAT, command=self.logout).pack(side=tk.RIGHT, padx=10)

        main = tk.Frame(self, bg=app.colors["bg"])
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        menu = tk.Frame(main, bg=app.colors["surface"], relief=tk.RIDGE, bd=1)
        menu.pack(fill=tk.X, pady=10)
        tk.Label(menu, text="Модули", font=("Segoe UI", 14, "bold"),
                 bg=app.colors["surface"], fg=app.colors["primary"]).pack(anchor=tk.W, padx=15, pady=10)

        btns = tk.Frame(menu, bg=app.colors["surface"])
        btns.pack(padx=15, pady=10)

        modules = [
            ("🧠 Психология", self.app.open_psychology, app.colors["primary"]),
            ("💪 Реабилитация", self.app.open_rehab, app.colors["success"]),
            ("🤟 Жесты", self.app.open_gesture, app.colors["danger"])
        ]

        for i, (text, cmd, color) in enumerate(modules):
            btn = tk.Button(btns, text=text, bg=color, fg="white",
                            font=("Segoe UI", 11), relief=tk.FLAT, height=2, command=cmd)
            btn.grid(row=i, column=0, padx=5, pady=5, sticky="ew")
        btns.grid_columnconfigure(0, weight=1)

        info = tk.Frame(main, bg=app.colors["surface2"], relief=tk.RIDGE, bd=1)
        info.pack(fill=tk.X, pady=10)
        tk.Label(info, text="💡 Совет дня", font=("Segoe UI", 12, "bold"),
                 bg=app.colors["surface2"], fg=app.colors["primary"]).pack(anchor=tk.W, padx=15, pady=5)
        tk.Label(info, text="Сделайте глубокий вдох — вы справитесь! 🌟",
                 bg=app.colors["surface2"], fg=app.colors["text2"]).pack(anchor=tk.W, padx=15, pady=5)

    def logout(self):
        self.app.auth.current_user = None
        self.app.show_login()


# ==================== ПСИХОЛОГИЯ ====================
class PsychologyScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=app.colors["bg"])
        self.app = app
        self.pack(fill=tk.BOTH, expand=True)

        header = tk.Frame(self, bg=app.colors["surface2"], height=50)
        header.pack(fill=tk.X)
        tk.Button(header, text="← Назад", bg=app.colors["primary"], fg="white",
                  relief=tk.FLAT, command=self.app.go_back).pack(side=tk.LEFT, padx=10, pady=5)
        tk.Label(header, text="🧠 Психологическая помощь", font=("Segoe UI", 16, "bold"),
                 bg=app.colors["surface2"], fg=app.colors["primary"]).pack(side=tk.LEFT, padx=10)

        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # === ЧАТ ===
        chat_tab = tk.Frame(notebook, bg=app.colors["surface"])
        notebook.add(chat_tab, text="💬 Чат")

        self.chat = scrolledtext.ScrolledText(chat_tab, height=15, bg=app.colors["surface2"],
                                              fg=app.colors["text"], wrap=tk.WORD, font=("Segoe UI", 11))
        self.chat.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.chat.insert(tk.END, "🤖 Психолог: Здравствуйте! Расскажите, что вас беспокоит.\n\n")
        self.chat.config(state=tk.DISABLED)

        mood_frame = tk.Frame(chat_tab, bg=app.colors["surface"])
        mood_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(mood_frame, text="Быстрый ответ:", bg=app.colors["surface"], fg=app.colors["text"]).pack(side=tk.LEFT)
        for mood, color in [("Отлично 😊", app.colors["success"]), ("Нормально 🙂", app.colors["primary"]),
                            ("Плохо 😔", app.colors["danger"]), ("Нужна помощь 🆘", app.colors["danger"])]:
            btn = tk.Button(mood_frame, text=mood, bg=color, fg="white", relief=tk.FLAT,
                            command=lambda m=mood: self.send_message(m))
            btn.pack(side=tk.LEFT, padx=3)

        input_frame = tk.Frame(chat_tab, bg=app.colors["surface"])
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        self.entry = tk.Entry(input_frame, bg=app.colors["surface2"], fg=app.colors["text"],
                              font=("Segoe UI", 11), relief=tk.FLAT)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.entry.bind("<Return>", lambda e: self.send_message())
        tk.Button(input_frame, text="Отправить ➤", bg=app.colors["primary"], fg="white",
                  relief=tk.FLAT, command=self.send_message).pack(side=tk.RIGHT, padx=5)

        # === МЕДИТАЦИИ ===
        med_tab = tk.Frame(notebook, bg=app.colors["surface"])
        notebook.add(med_tab, text="🧘 Медитации")
        meditations = [
            ("🌬️ Дыхание 4-7-8", "Вдох 4с → Задержка 7с → Выдох 8с. Повторить 4 раза."),
            ("💆 Снятие напряжения", "Напрячь всё тело на 5с → Расслабиться. Повторить 3 раза."),
            ("🎵 Успокаивающая музыка", "Включите спокойную музыку и закройте глаза на 10 минут.")
        ]
        for name, desc in meditations:
            frame = tk.Frame(med_tab, bg=app.colors["surface2"], relief=tk.RIDGE, bd=1)
            frame.pack(fill=tk.X, padx=20, pady=5)
            tk.Label(frame, text=name, font=("Segoe UI", 12, "bold"),
                     bg=app.colors["surface2"], fg=app.colors["primary"]).pack(anchor=tk.W, padx=10, pady=5)
            tk.Label(frame, text=desc, bg=app.colors["surface2"], fg=app.colors["text2"], justify=tk.LEFT).pack(
                anchor=tk.W, padx=10, pady=5)
            tk.Button(frame, text="▶ Начать", bg=app.colors["success"], fg="black", relief=tk.FLAT,
                      command=lambda d=desc: messagebox.showinfo("Медитация", d)).pack(anchor=tk.E, padx=10, pady=5)

        # === ТЕСТЫ ===
        test_tab = tk.Frame(notebook, bg=app.colors["surface"])
        notebook.add(test_tab, text="📋 Тесты")
        tests = [("🧠 Тест на ПТСР", self.test_ptsd), ("😔 Тест на депрессию", self.test_depression),
                 ("😰 Тест на тревожность", self.test_anxiety)]
        for name, cmd in tests:
            tk.Button(test_tab, text=name, bg=app.colors["primary"], fg="white", relief=tk.FLAT,
                      height=2, width=35, command=cmd).pack(pady=8)

    def send_message(self, msg=None):
        if msg is None:
            msg = self.entry.get().strip()
        if not msg:
            return

        self.chat.config(state=tk.NORMAL)
        self.chat.insert(tk.END, f"👤 Вы: {msg}\n")

        if crisis_detected(msg):
            response = ("⚠️ Пожалуйста, не принимайте поспешных решений. Вы не один.\n\n"
                        "📞 Кризисная линия: 8-800-2000-122 (Россия, бесплатно)\n"
                        "🌐 Международная помощь: findahelpline.com\n\n"
                        "🤖 Я рядом. Расскажите, что случилось?")
            self.chat.insert(tk.END, f"🤖 Психолог: {response}\n\n")
            self.show_crisis_warning()
        else:
            answers = [
                "Понимаю вас. Расскажите подробнее, что вы чувствуете?",
                "Спасибо, что поделились. Это важный шаг.",
                "Как вы себя чувствуете прямо сейчас?",
                "Я здесь, чтобы поддержать вас. Что вас беспокоит больше всего?",
                "Это нормально — чувствовать так. Давайте разберёмся вместе."
            ]
            self.chat.insert(tk.END, f"🤖 Психолог: {random.choice(answers)}\n\n")

        self.chat.see(tk.END)
        self.chat.config(state=tk.DISABLED)
        self.entry.delete(0, tk.END)

    def show_crisis_warning(self):
        win = tk.Toplevel(self)
        win.title("🆘 Срочная помощь")
        win.geometry("450x380")
        win.configure(bg="#1a1a2e")
        win.transient(self)
        win.grab_set()

        tk.Label(win, text="⚠️ Вам нужна помощь", font=("Segoe UI", 16, "bold"),
                 bg="#1a1a2e", fg="#e74c3c").pack(pady=20)
        tk.Label(win, text="📞 Позвоните на кризисную линию:\n\n"
                           "🇷🇺 Россия: 8-800-2000-122 (детский телефон доверия)\n"
                           "🇷🇺 Экстренная психологическая: 8-499-173-09-09\n"
                           "🌍 Международный поиск: findahelpline.com\n\n"
                           "✅ Круглосуточно • Анонимно • Бесплатно\n\n"
                           "💙 Вы не один. Помощь рядом.",
                 bg="#1a1a2e", fg="#cdd6f4", justify=tk.CENTER, font=("Segoe UI", 10)).pack(pady=10)
        tk.Button(win, text="Закрыть", bg="#4a90e2", fg="white",
                  relief=tk.FLAT, command=win.destroy).pack(pady=20)

    def test_ptsd(self):
        self.run_test("🧠 ПТСР",
                      ["Бывают ли кошмары о травмирующем событии?", "Избегаете ли мест, напоминающих о событии?",
                       "Легко ли вас напугать?"])

    def test_depression(self):
        self.run_test("😔 Депрессия", ["Чувствуете ли грусть большую часть дня?", "Потеряли ли интерес к любимым делам?",
                                      "Есть ли проблемы со сном или аппетитом?"])

    def test_anxiety(self):
        self.run_test("😰 Тревожность", ["Часто ли чувствуете нервозность?", "Трудно ли расслабиться?",
                                        "Бывает ли учащённое сердцебиение без причины?"])

    def run_test(self, name, questions):
        win = tk.Toplevel(self)
        win.title(name)
        win.geometry("520x500")
        win.configure(bg="#1a1a2e")
        tk.Label(win, text=name, font=("Segoe UI", 16, "bold"), bg="#1a1a2e", fg="#4a90e2").pack(pady=10)

        answers = []
        for q in questions:
            f = tk.Frame(win, bg="#1a1a2e")
            f.pack(fill=tk.X, padx=20, pady=8)
            tk.Label(f, text=f"• {q}", bg="#1a1a2e", fg="#cdd6f4", wraplength=450, justify=tk.LEFT).pack(anchor=tk.W)
            var = tk.IntVar(value=0)
            for i, t in enumerate(["Нет (0)", "Иногда (1)", "Часто (2)", "Постоянно (3)"]):
                rb = tk.Radiobutton(f, text=t, variable=var, value=i, bg="#1a1a2e", fg="#cdd6f4", selectcolor="#1a1a2e",
                                    activebackground="#1a1a2e")
                rb.pack(anchor=tk.W, padx=20)
            answers.append(var)

        def calc():
            score = sum(v.get() for v in answers)
            maxs = len(questions) * 3
            if score <= maxs * 0.3:
                res = "✅ Низкий уровень. Всё в порядке, продолжайте заботиться о себе!"
            elif score <= maxs * 0.6:
                res = "⚠️ Средний уровень. Обратите внимание на своё состояние, попробуйте техники релаксации."
            else:
                res = "🔴 Высокий уровень. Рекомендуем обратиться к специалисту для консультации."
            messagebox.showinfo("📊 Результат", f"Ваш счёт: {score} из {maxs}\n\n{res}")
            win.destroy()

        tk.Button(win, text="Узнать результат", bg="#4a90e2", fg="white", relief=tk.FLAT, command=calc).pack(pady=20)


# ==================== РЕАБИЛИТАЦИЯ ====================
class RehabScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=app.colors["bg"])
        self.app = app
        self.pack(fill=tk.BOTH, expand=True)

        header = tk.Frame(self, bg=app.colors["surface2"], height=50)
        header.pack(fill=tk.X)
        tk.Button(header, text="← Назад", bg=app.colors["primary"], fg="white",
                  relief=tk.FLAT, command=self.app.go_back).pack(side=tk.LEFT, padx=10, pady=5)
        tk.Label(header, text="💪 Реабилитация", font=("Segoe UI", 16, "bold"),
                 bg=app.colors["surface2"], fg=app.colors["primary"]).pack(side=tk.LEFT, padx=10)

        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # === УПРАЖНЕНИЯ ===
        ex_tab = tk.Frame(notebook, bg=app.colors["surface"])
        notebook.add(ex_tab, text="🏃 Упражнения")

        categories = [
            (
            "🦵 Ноги", ["Подъёмы на носки (15 раз)", "Махи ногой вперёд/назад (10 раз)", "Приседания у стены (10 раз)"]),
            ("💪 Руки",
             ["Сгибание рук с весом (12 раз)", "Разведение рук в стороны (10 раз)", "Вращение кистями (20 раз)"]),
            ("🌬️ Дыхание",
             ["Диафрагмальное дыхание (5 мин)", "Дыхание 4-7-8 (4 цикла)", "Квадратное дыхание (4-4-4-4)"]),
            (
            "🚶 Ходьба", ["Ходьба на месте (1 мин)", "Ходьба с пятки на носок (2 мин)", "Баланс на одной ноге (30 сек)"])
            # ИСПРАВЛЕНО: добавлена ]
        ]

        for cat, exs in categories:
            frame = tk.Frame(ex_tab, bg=app.colors["surface2"], relief=tk.RIDGE, bd=1)
            frame.pack(fill=tk.X, padx=20, pady=5)
            tk.Label(frame, text=cat, font=("Segoe UI", 12, "bold"),
                     bg=app.colors["surface2"], fg=app.colors["primary"]).pack(anchor=tk.W, padx=10, pady=5)
            for ex in exs:
                row = tk.Frame(frame, bg=app.colors["surface2"])
                row.pack(fill=tk.X, padx=10, pady=2)
                tk.Label(row, text=f"• {ex}", bg=app.colors["surface2"], fg=app.colors["text"]).pack(side=tk.LEFT)
                tk.Button(row, text="▶ Выполнить", bg=app.colors["success"], fg="black", relief=tk.FLAT,
                          command=lambda e=ex: messagebox.showinfo("Упражнение",
                                                                   f"Начинаем: {e}\n\nСлушайте своё тело!")).pack(
                    side=tk.RIGHT, padx=5)

        # === СОВЕТЫ ===
        tips_tab = tk.Frame(notebook, bg=app.colors["surface"])
        notebook.add(tips_tab, text="💡 Советы")
        tips = [
            "🎯 Начинайте с малого — 5-10 минут в день достаточно для старта",
            "💧 Пейте воду до и после упражнений для лучшего восстановления",
            "⏱️ Отдыхайте между подходами 30-60 секунд",
            "📈 Не сравнивайте себя с другими — важен ваш личный прогресс",
            "🔄 Занимайтесь регулярно, лучше каждый день понемногу",
            "👂 Прислушивайтесь к телу — боль это сигнал остановиться",
            "😴 Высыпайтесь — восстановление важно не меньше тренировок",
            "🥗 Правильное питание ускорит прогресс"
        ]
        for tip in tips:
            tk.Label(tips_tab, text=tip, bg=app.colors["surface2"], fg=app.colors["text2"],
                     font=("Segoe UI", 10), wraplength=500, justify=tk.LEFT).pack(anchor=tk.W, padx=20, pady=4)


# ==================== ЖЕСТЫ (ИСПРАВЛЕННЫЙ) ====================
class GestureScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=app.colors["bg"])
        self.app = app
        self.pack(fill=tk.BOTH, expand=True)

        self.mode = "gesture_to_text"
        self.cam_on = False
        self.cap = None
        self.auto = False
        self.last_gesture = ""
        self.video_thread = None
        self._stop_video_thread = False

        # MediaPipe
        self.mp_hands = None
        self.hands = None
        self.mp_draw = None
        self._init_mediapipe()

        # Словарь параметров pack для виджетов
        self.widget_packs = {}

        self.build_ui()

    def _init_mediapipe(self):
        """Безопасная инициализация MediaPipe"""
        try:
            self.mp_hands = mp.solutions.hands
            self.mp_draw = mp.solutions.drawing_utils
            self.hands = self.mp_hands.Hands(
                min_detection_confidence=0.7,
                min_tracking_confidence=0.5,
                max_num_hands=1,
                model_complexity=0,
                static_image_mode=False
            )
        except ImportError:
            messagebox.showerror("Ошибка", "Установите mediapipe:\npip install mediapipe")
        except Exception as e:
            print(f"MediaPipe error: {e}")
            self.hands = None

    def build_ui(self):
        # === HEADER ===
        header = tk.Frame(self, bg=self.app.colors["surface2"], height=50)
        header.pack(fill=tk.X)
        tk.Button(header, text="← Назад", bg=self.app.colors["primary"], fg="white",
                  relief=tk.FLAT, command=self.on_back).pack(side=tk.LEFT, padx=10, pady=5)
        tk.Label(header, text="🤟 Перевод жестов", font=("Segoe UI", 16, "bold"),
                 bg=self.app.colors["surface2"], fg=self.app.colors["primary"]).pack(side=tk.LEFT, padx=10)

        # === MODE SWITCHER ===
        mode_frame = tk.Frame(self, bg=self.app.colors["surface2"])
        mode_frame.pack(fill=tk.X, padx=10, pady=5)

        self.btn_gesture_to_text = tk.Button(
            mode_frame, text="🤟 Жесты → Текст", bg=self.app.colors["primary"], fg="white",
            relief=tk.FLAT, width=20, command=self.set_mode_gesture_to_text)
        self.btn_gesture_to_text.pack(side=tk.LEFT, padx=5)

        self.btn_text_to_gesture = tk.Button(
            mode_frame, text="✍️ Текст → Жесты", bg=self.app.colors["surface"], fg="white",
            relief=tk.FLAT, width=20, command=self.set_mode_text_to_gesture)
        self.btn_text_to_gesture.pack(side=tk.LEFT, padx=5)

        # === MAIN CONTENT ===
        main = tk.Frame(self, bg=self.app.colors["bg"])
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # LEFT: Video + Controls
        left = tk.Frame(main, bg=self.app.colors["surface"], relief=tk.RIDGE, bd=1)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        self.video_label = tk.Label(left, bg=self.app.colors["bg"], width=500, height=380)
        self.video_label.pack(padx=15, pady=15)

        btn_frame = tk.Frame(left, bg=self.app.colors["surface"])
        btn_frame.pack(fill=tk.X, padx=15, pady=15)

        self.cam_btn = tk.Button(btn_frame, text="🟢 Включить камеру", bg=self.app.colors["success"],
                                 fg="black", relief=tk.FLAT, command=self.toggle_camera)
        self.cam_btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        self.auto_btn = tk.Button(btn_frame, text="🔄 Авто: ВЫКЛ", bg=self.app.colors["primary"],
                                  fg="white", relief=tk.FLAT, command=self.toggle_auto)
        self.auto_btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        self.rec_btn = tk.Button(btn_frame, text="🔍 Распознать", bg=self.app.colors["primary"],
                                 fg="white", relief=tk.FLAT, command=self.recognize, state=tk.DISABLED)
        self.rec_btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        # RIGHT: Results / Input
        right = tk.Frame(main, bg=self.app.colors["surface"], relief=tk.RIDGE, bd=1, width=350)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        right.pack_propagate(False)

        # === MODE: Gesture → Text ===
        self.result_label = tk.Label(right, text="📝 Результат", font=("Segoe UI", 14, "bold"),
                                     bg=self.app.colors["surface"], fg=self.app.colors["text"])
        self.widget_packs[self.result_label] = {"anchor": tk.W, "padx": 15, "pady": 10}

        self.result_text = tk.Text(right, height=5, font=("Segoe UI", 18),
                                   bg=self.app.colors["surface2"], fg=self.app.colors["text"], wrap=tk.WORD)
        self.widget_packs[self.result_text] = {"fill": tk.X, "padx": 15, "pady": 5}

        # === MODE: Text → Gesture ===
        self.text_input_label = tk.Label(right, text="✍️ Введите текст для перевода:",
                                         font=("Segoe UI", 12), bg=self.app.colors["surface"],
                                         fg=self.app.colors["text"])
        self.widget_packs[self.text_input_label] = {"anchor": tk.W, "padx": 15, "pady": 10}

        self.text_input = tk.Entry(right, font=("Segoe UI", 14),
                                   bg=self.app.colors["surface2"], fg=self.app.colors["text"], relief=tk.FLAT)
        self.widget_packs[self.text_input] = {"fill": tk.X, "padx": 15, "pady": 5}
        self.text_input.bind("<Return>", lambda e: self.text_to_gesture())

        self.translate_btn = tk.Button(right, text="🔄 Перевести в жест", bg=self.app.colors["primary"],
                                       fg="white", relief=tk.FLAT, command=self.text_to_gesture)
        self.widget_packs[self.translate_btn] = {"fill": tk.X, "padx": 15, "pady": 5}

        self.gesture_result_label = tk.Label(right, text="", font=("Segoe UI", 28),
                                             bg=self.app.colors["surface2"], fg=self.app.colors["primary"],
                                             height=2, wraplength=300, justify=tk.CENTER)
        self.widget_packs[self.gesture_result_label] = {"fill": tk.X, "padx": 15, "pady": 10}

        # === ACTION BUTTONS ===
        rbtn = tk.Frame(right, bg=self.app.colors["surface"])
        rbtn.pack(fill=tk.X, padx=15, pady=10)

        self.speak_btn = tk.Button(rbtn, text="🔊 Озвучить", bg=self.app.colors["primary"],
                                   fg="white", relief=tk.FLAT, command=self.speak)
        self.widget_packs[self.speak_btn] = {"side": tk.LEFT, "padx": 2, "expand": True, "fill": tk.X}

        tk.Button(rbtn, text="📋 Копировать", bg=self.app.colors["primary"], fg="white",
                  relief=tk.FLAT, command=self.copy).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        tk.Button(rbtn, text="🗑️ Очистить", bg=self.app.colors["danger"], fg="white",
                  relief=tk.FLAT, command=self.clear).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)

        self.status = tk.Label(right, text="✅ Готов к работе", bg=self.app.colors["surface"],
                               fg=self.app.colors["success"], font=("Segoe UI", 9))
        self.status.pack(pady=10)

        # === HINTS ===
        tk.Label(right, text="📚 Доступные жесты", font=("Segoe UI", 12, "bold"),
                 bg=self.app.colors["surface"], fg=self.app.colors["primary"]).pack(anchor=tk.W, padx=15)

        hints = """🖐️ 1 палец (большой) → привет
✌️ 2 пальца → да
🤟 3 пальца → нет  
🖖 4 пальца → спасибо
🆘 5 пальцев → помощь
✊ Кулак → стоп
👍 Большой вверх → отлично
👎 Большой вниз → плохо"""
        tk.Label(right, text=hints, bg=self.app.colors["surface"], fg=self.app.colors["text2"],
                 justify=tk.LEFT, font=("Segoe UI", 9)).pack(anchor=tk.W, padx=15, pady=5)

        # Инициализация режима по умолчанию
        self.set_mode_gesture_to_text()

    def set_mode_gesture_to_text(self):
        """Переключение в режим: жесты → текст"""
        self.mode = "gesture_to_text"
        self.btn_gesture_to_text.configure(bg=self.app.colors["primary"])
        self.btn_text_to_gesture.configure(bg=self.app.colors["surface"])

        # Показать элементы режима жесты→текст
        self.result_label.pack(**self.widget_packs[self.result_label])
        self.result_text.pack(**self.widget_packs[self.result_text])
        self.speak_btn.pack(**self.widget_packs[self.speak_btn])

        # Скрыть элементы режима текст→жесты
        for widget in [self.text_input_label, self.text_input, self.translate_btn, self.gesture_result_label]:
            widget.pack_forget()

        self.status.configure(text="🎯 Режим: жесты → текст", fg=self.app.colors["success"])

    def set_mode_text_to_gesture(self):
        """Переключение в режим: текст → жесты"""
        self.mode = "text_to_gesture"
        self.btn_gesture_to_text.configure(bg=self.app.colors["surface"])
        self.btn_text_to_gesture.configure(bg=self.app.colors["primary"])

        # Скрыть элементы режима жесты→текст
        for widget in [self.result_label, self.result_text, self.speak_btn]:
            widget.pack_forget()

        # Показать элементы режима текст→жесты
        self.text_input_label.pack(**self.widget_packs[self.text_input_label])
        self.text_input.pack(**self.widget_packs[self.text_input])
        self.translate_btn.pack(**self.widget_packs[self.translate_btn])
        self.gesture_result_label.pack(**self.widget_packs[self.gesture_result_label])

        self.status.configure(text="✍️ Режим: текст → жесты", fg=self.app.colors["success"])

    def text_to_gesture(self):
        """Конвертация текста в визуальные жесты (эмодзи)"""
        text = self.text_input.get().strip().lower()
        if not text:
            messagebox.showwarning("Внимание", "Введите текст для перевода", parent=self)
            return

        gesture_map = {
            "привет": "🖐️", "здравствуй": "🖐️", "hi": "🖐️", "hello": "🖐️",
            "да": "✌️", "yes": "✌️", "ага": "✌️", "угу": "✌️",
            "нет": "🤟", "no": "🤟", "не": "🤟", "неа": "🤟",
            "спасибо": "🖖", "благодарю": "🖖", "thanks": "🖖", "мерси": "🖖",
            "помощь": "🆘", "помогите": "🆘", "sos": "🆘", "спасите": "🆘",
            "стоп": "✊", "хватит": "✊", "stop": "✊", "подожди": "✊",
            "отлично": "👍", "класс": "👍", "good": "👍", "супер": "👍",
            "плохо": "👎", "ужас": "👎", "bad": "👎", "кошмар": "👎"
        }

        words = text.split()
        gestures = []
        for word in words:
            clean_word = ''.join(c for c in word if c.isalpha() or c == '-').lower()
            gesture = gesture_map.get(clean_word, None)
            if gesture:
                gestures.append(gesture)

        if gestures:
            result = " ".join(gestures)
            self.gesture_result_label.configure(text=result)
            self.status.configure(text=f"✓ Переведено: {text} → {result}", fg=self.app.colors["success"])
        else:
            self.gesture_result_label.configure(text="❓")
            self.status.configure(text="⚠ Жест не найден в словаре", fg="#f39c12")

    def on_back(self):
        """Возврат в главное меню"""
        self.stop_camera()
        if self.hands:
            self.hands.close()
        self.app.go_back()

    def toggle_camera(self):
        """Включение/выключение камеры с запросом разрешения"""
        if not self.cam_on:
            self.request_camera_permission()
        else:
            self.stop_camera()

    def request_camera_permission(self):
        """Диалог запроса разрешения на доступ к камере"""
        dialog = tk.Toplevel(self)
        dialog.title("📷 Доступ к камере")
        dialog.geometry("440x260")
        dialog.configure(bg=self.app.colors["surface"])
        dialog.transient(self)
        dialog.grab_set()
        dialog.resizable(False, False)

        # Центрирование

        x = self.winfo_rootx() + (self.winfo_width() - 440) // 2
        y = self.winfo_rooty() + (self.winfo_height() - 260) // 2
        dialog.geometry(f"+{x}+{y}")

        tk.Label(dialog, text="📷 Требуется доступ к камере",
                 font=("Segoe UI", 14, "bold"),
                 bg=self.app.colors["surface"], fg=self.app.colors["primary"]
                 ).pack(pady=(20, 10))

        tk.Label(dialog,
                 text="Для распознавания жестов приложению нужен доступ к камере.\n"
                      "✅ Все данные обрабатываются локально на вашем устройстве\n"
                      "🔒 Видео не записывается и не отправляется в интернет\n"
                      "🗑️ Данные не сохраняются после закрытия приложения",
                 bg=self.app.colors["surface"], fg=self.app.colors["text2"],
                 justify=tk.LEFT, font=("Segoe UI", 9)).pack(pady=(0, 15), padx=25)

        btn_frame = tk.Frame(dialog, bg=self.app.colors["surface"])
        btn_frame.pack(pady=(0, 15))

        def on_allow():
            dialog.destroy()
            self.start_camera()

        def on_deny():
            dialog.destroy()
            self.status.configure(text="⚠ Доступ к камере запрещён", fg=self.app.colors["danger"])
            messagebox.showinfo(
                "Информация",
                "Вы можете включить камеру позже через кнопку «Включить камеру».\n"
                "Без камеры доступен только режим «Текст → Жесты».",
                parent=self
            )

        tk.Button(btn_frame, text="✅ Разрешить доступ", bg=self.app.colors["success"],
                  fg="black", relief=tk.FLAT, font=("Segoe UI", 10, "bold"),
                  width=18, command=on_allow).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="❌ Отмена", bg=self.app.colors["surface2"],
                  fg=self.app.colors["text"], relief=tk.FLAT, font=("Segoe UI", 10),
                  width=18, command=on_deny).pack(side=tk.LEFT, padx=10)

        dialog.protocol("WM_DELETE_WINDOW", on_deny)

    def start_camera(self):
        """Запуск камеры с обработкой ошибок"""
        try:
            # Пробуем разные backend'ы для совместимости
            backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_AVFOUNDATION, cv2.CAP_V4L2, None]
            self.cap = None

            for backend in backends:
                if backend is None:
                    self.cap = cv2.VideoCapture(0)
                else:
                    self.cap = cv2.VideoCapture(0, backend)
                if self.cap and self.cap.isOpened():
                    break

            if not self.cap or not self.cap.isOpened():
                raise Exception("Не удалось открыть камеру. Проверьте подключение.")

            # Настройки
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)

            self.cam_on = True
            self._stop_video_thread = False

            self.cam_btn.configure(text="🔴 Выключить камеру", bg=self.app.colors["danger"])
            self.rec_btn.configure(state=tk.NORMAL)
            self.status.configure(text="📹 Камера активна", fg=self.app.colors["success"])

            # Запуск потока
            self.video_thread = threading.Thread(target=self.update_video, daemon=True)
            self.video_thread.start()

        except Exception as e:
            self.cam_on = False
            self.status.configure(text=f"❌ Ошибка: {str(e)[:50]}", fg=self.app.colors["danger"])
            messagebox.showerror("Ошибка камеры", f"Не удалось подключить камеру:\n\n{str(e)}\n\n"
                                                  "Проверьте:\n"
                                                  "• Камера подключена и не используется другими программами\n"
                                                  "• Установлены драйверы камеры\n"
                                                  "• Разрешения на доступ к камере в настройках ОС")

    def stop_camera(self):
        """Корректная остановка камеры"""
        self.cam_on = False
        self._stop_video_thread = True

        if self.cap:
            self.cap.release()
            self.cap = None

        self.cam_btn.configure(text="🟢 Включить камеру", bg=self.app.colors["success"])
        self.rec_btn.configure(state=tk.DISABLED)
        self.video_label.configure(image="")
        self.video_label.image = None
        self.status.configure(text="⏹ Камера выключена", fg=self.app.colors["text2"])

        # Ждём завершения потока
        if self.video_thread and self.video_thread.is_alive():
            self.video_thread.join(timeout=1.0)

    def update_video(self):
        """Поток обновления видео"""
        while self.cam_on and self.cap and self.cap.isOpened() and not self._stop_video_thread:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    break

                frame = cv2.flip(frame, 1)  # Зеркальное отображение

                # Распознавание в авто-режиме
                if self.mode == "gesture_to_text" and self.hands:
                    gesture = self.detect_gesture(frame)
                    if gesture and self.auto and gesture != self.last_gesture:
                        self.last_gesture = gesture
                        self.app.root.after(0, lambda g=gesture: self.add_result(g))

                # Подготовка кадра
                frame = cv2.resize(frame, (500, 380))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)

                self.app.root.after(0, lambda img=imgtk: self.update_video_image(img))

            except Exception as e:
                print(f"Video update error: {e}")
                break

            time.sleep(0.033)  # ~30 FPS

        if self.cam_on:
            self.app.root.after(0, self.stop_camera)

    def update_video_image(self, imgtk):
        """Обновление изображения"""
        self.video_label.configure(image=imgtk)
        self.video_label.image = imgtk

    def detect_gesture(self, frame):
        """Распознавание жестов с улучшенной логикой"""
        if not self.hands:
            return None

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                if self.mp_draw:
                    self.mp_draw.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                    )

                lm = hand_landmarks.landmark

                # === ПОДСЧЁТ ПАЛЬЦЕВ ===
                fingers = 0

                # Большой палец (после зеркального отражения)
                if lm[4].x > lm[3].x:  # Кончик правее основания = отведён
                    fingers += 1

                # Остальные пальцы: кончик выше основания = поднят
                for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:
                    if lm[tip].y < lm[pip].y:
                        fingers += 1

                # === ОПРЕДЕЛЕНИЕ ЖЕСТА ===
                # Приоритет: жесты с большим пальцем (👍/👎)
                thumb_up = lm[4].y < lm[8].y and lm[4].x > lm[3].x
                thumb_down = lm[4].y > lm[8].y and lm[4].x > lm[3].x

                if fingers == 1 and thumb_up:
                    return "отлично"  # 👍
                if fingers == 1 and thumb_down:
                    return "плохо"  # 👎

                # Жесты по количеству пальцев
                gesture_map = {
                    1: "привет",  # 🖐️
                    2: "да",  # ✌️
                    3: "нет",  # 🤟
                    4: "спасибо",  # 🖖
                    5: "помощь",  # 🖐️
                    0: "стоп"  # ✊
                }
                return gesture_map.get(fingers)

        return None

    def recognize(self):
        """Ручное распознавание"""
        if not self.cam_on or not self.cap or not self.cap.isOpened():
            messagebox.showwarning("Внимание", "Сначала включите камеру", parent=self)
            return

        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            gesture = self.detect_gesture(frame)

            if gesture:
                self.add_result(gesture)
                self.speak_word(gesture)
                self.status.configure(text=f"✓ Распознано: «{gesture}»", fg=self.app.colors["success"])
            else:
                self.status.configure(text="⚠ Жест не распознан", fg="#f39c12")
                if self.hands:
                    import cv2
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = self.hands.process(rgb)
                    if not results.multi_hand_landmarks:
                        self.status.configure(text="⚠ Рука не обнаружена", fg="#f39c12")
        else:
            self.status.configure(text="❌ Ошибка чтения кадра", fg=self.app.colors["danger"])

    def toggle_auto(self):
        """Переключение авто-режима"""
        self.auto = not self.auto
        self.auto_btn.configure(
            text="🔄 Авто: ВКЛ" if self.auto else "🔄 Авто: ВЫКЛ",
            bg=self.app.colors["success"] if self.auto else self.app.colors["primary"]
        )
        self.status.configure(
            text="🔄 Авто-распознавание активно" if self.auto else "🔄 Авто-распознавание отключено",
            fg=self.app.colors["success"] if self.auto else self.app.colors["text2"]
        )

    def add_result(self, word):
        """Добавление результата"""
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", word.capitalize())

    def speak_word(self, text):
        """Озвучивание"""
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.9)

            voices = engine.getProperty('voices')
            for voice in voices:
                if 'russian' in voice.name.lower() or 'ru' in voice.id.lower():
                    engine.setProperty('voice', voice.id)
                    break

            engine.say(text)
            engine.runAndWait()
        except ImportError:
            print("💡 Установите pyttsx3: pip install pyttsx3")
        except Exception as e:
            print(f"🔊 Ошибка озвучивания: {e}")

    def speak(self):
        """Озвучить текущий текст"""
        if self.mode == "gesture_to_text":
            text = self.result_text.get("1.0", tk.END).strip()
        else:
            text = self.text_input.get().strip()
        if text:
            self.speak_word(text)
            self.status.configure(text=f"🔊 Озвучиваю: {text}", fg=self.app.colors["primary"])

    def copy(self):
        """Копировать в буфер"""
        if self.mode == "gesture_to_text":
            text = self.result_text.get("1.0", tk.END).strip()
        else:
            text = self.text_input.get().strip()
        if text:
            self.app.root.clipboard_clear()
            self.app.root.clipboard_append(text)
            self.app.root.update()
            self.status.configure(text="📋 Скопировано!", fg=self.app.colors["success"])

    def clear(self):
        """Очистить"""
        if self.mode == "gesture_to_text":
            self.result_text.delete("1.0", tk.END)
            self.last_gesture = ""
        else:
            self.text_input.delete(0, tk.END)
            self.gesture_result_label.configure(text="")
        self.status.configure(text="🗑️ Очищено", fg=self.app.colors["text2"])

if __name__ == "__main__":
    app = SignBridgeApp()
    app.run()