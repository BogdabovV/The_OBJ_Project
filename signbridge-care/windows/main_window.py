import tkinter as tk
from tkinter import messagebox
import hashlib
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from encryption import SecureStorage

class MainWindow:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.current_user = None
        self.storage = SecureStorage()
        self.users = self.load_users()

        self.colors = {
            "bg": "#0f0f1a", "surface": "#1a1a2e", "surface2": "#16213e",
            "primary": "#4a90e2", "success": "#2ecc71", "danger": "#e74c3c",
            "text": "#cdd6f4", "text2": "#a8b2d1"
        }

        self.create_login()

    def hash_pass(self, pwd):
        return hashlib.sha256(pwd.encode()).hexdigest()

    def load_users(self):
        if os.path.exists("data/users.dat"):
            return self.storage.load("data/users.dat")
        return {}

    def save_users(self):
        self.storage.save(self.users, "data/users.dat")

    def toggle_pass(self, entry, btn):
        if entry.cget('show') == '*':
            entry.configure(show='')
            btn.configure(text="🔒")
        else:
            entry.configure(show='*')
            btn.configure(text="👁️")

    def create_login(self):
        for w in self.parent.winfo_children():
            w.destroy()

        box = tk.Frame(self.parent, bg=self.colors["surface"], relief=tk.RIDGE, bd=1)
        box.place(relx=0.5, rely=0.5, anchor="center", width=380, height=480)

        tk.Label(box, text="SignBridge Care", font=("Segoe UI", 20, "bold"),
                 bg=self.colors["surface"], fg=self.colors["primary"]).pack(pady=25)

        tk.Label(box, text="Логин", bg=self.colors["surface"], fg=self.colors["text"]).pack(anchor=tk.W, padx=30)
        self.login_entry = tk.Entry(box, bg=self.colors["surface2"], fg=self.colors["text"], relief=tk.FLAT)
        self.login_entry.pack(padx=30, pady=5, fill=tk.X)

        tk.Label(box, text="Пароль", bg=self.colors["surface"], fg=self.colors["text"]).pack(anchor=tk.W, padx=30, pady=(10,0))

        pf = tk.Frame(box, bg=self.colors["surface"])
        pf.pack(padx=30, pady=5, fill=tk.X)
        self.pass_entry = tk.Entry(pf, show="*", bg=self.colors["surface2"], fg=self.colors["text"], relief=tk.FLAT)
        self.pass_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.pass_btn = tk.Button(pf, text="👁️", bg=self.colors["surface2"], fg=self.colors["text"],
                                  relief=tk.FLAT, width=3, command=lambda: self.toggle_pass(self.pass_entry, self.pass_btn))
        self.pass_btn.pack(side=tk.RIGHT, padx=(5,0))

        tk.Button(box, text="Войти", bg=self.colors["primary"], fg="white",
                  relief=tk.FLAT, height=2, command=self.do_login).pack(fill=tk.X, padx=30, pady=20)

        tk.Frame(box, bg=self.colors["text2"], height=1).pack(fill=tk.X, padx=30, pady=10)
        tk.Label(box, text="Нет аккаунта?", bg=self.colors["surface"], fg=self.colors["text2"]).pack()
        tk.Button(box, text="Регистрация", bg=self.colors["success"], fg="black",
                  relief=tk.FLAT, height=2, command=self.show_register).pack(fill=tk.X, padx=30, pady=10)

    def do_login(self):
        login = self.login_entry.get().strip()
        pwd = self.pass_entry.get().strip()
        if login in self.users and self.users[login]["pwd"] == self.hash_pass(pwd):
            self.current_user = login
            self.create_main()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")

    def show_register(self):
        win = tk.Toplevel(self.parent)
        win.title("Регистрация")
        win.geometry("380x480")
        win.configure(bg=self.colors["surface"])
        win.transient(self.parent)
        win.grab_set()

        tk.Label(win, text="Регистрация", font=("Segoe UI", 20, "bold"),
                 bg=self.colors["surface"], fg=self.colors["primary"]).pack(pady=20)

        tk.Label(win, text="Логин", bg=self.colors["surface"], fg=self.colors["text"]).pack(anchor=tk.W, padx=30)
        r_login = tk.Entry(win, bg=self.colors["surface2"], fg=self.colors["text"], relief=tk.FLAT)
        r_login.pack(padx=30, pady=5, fill=tk.X)

        tk.Label(win, text="Пароль", bg=self.colors["surface"], fg=self.colors["text"]).pack(anchor=tk.W, padx=30)
        pf = tk.Frame(win, bg=self.colors["surface"])
        pf.pack(padx=30, pady=5, fill=tk.X)
        r_pass = tk.Entry(pf, show="*", bg=self.colors["surface2"], fg=self.colors["text"], relief=tk.FLAT)
        r_pass.pack(side=tk.LEFT, fill=tk.X, expand=True)
        pb = tk.Button(pf, text="👁️", bg=self.colors["surface2"], fg=self.colors["text"],
                       relief=tk.FLAT, width=3, command=lambda: self.toggle_pass(r_pass, pb))
        pb.pack(side=tk.RIGHT, padx=(5,0))

        tk.Label(win, text="Повтор пароля", bg=self.colors["surface"], fg=self.colors["text"]).pack(anchor=tk.W, padx=30)
        pf2 = tk.Frame(win, bg=self.colors["surface"])
        pf2.pack(padx=30, pady=5, fill=tk.X)
        r_pass2 = tk.Entry(pf2, show="*", bg=self.colors["surface2"], fg=self.colors["text"], relief=tk.FLAT)
        r_pass2.pack(side=tk.LEFT, fill=tk.X, expand=True)
        pb2 = tk.Button(pf2, text="👁️", bg=self.colors["surface2"], fg=self.colors["text"],
                        relief=tk.FLAT, width=3, command=lambda: self.toggle_pass(r_pass2, pb2))
        pb2.pack(side=tk.RIGHT, padx=(5,0))

        def register():
            login = r_login.get().strip()
            pwd = r_pass.get().strip()
            pwd2 = r_pass2.get().strip()
            if not login or not pwd:
                messagebox.showerror("Ошибка", "Заполните поля")
                return
            if pwd != pwd2:
                messagebox.showerror("Ошибка", "Пароли не совпадают")
                return
            if login in self.users:
                messagebox.showerror("Ошибка", "Пользователь существует")
                return
            self.users[login] = {"pwd": self.hash_pass(pwd)}
            self.save_users()
            messagebox.showinfo("Успех", "Регистрация прошла")
            win.destroy()
            self.login_entry.delete(0, tk.END)
            self.login_entry.insert(0, login)

        tk.Button(win, text="Зарегистрироваться", bg=self.colors["success"], fg="black",
                  relief=tk.FLAT, height=2, command=register).pack(fill=tk.X, padx=30, pady=20)

    def create_main(self):
        for w in self.parent.winfo_children():
            w.destroy()

        header = tk.Frame(self.parent, bg=self.colors["surface2"], height=60)
        header.pack(fill=tk.X)
        tk.Label(header, text="SignBridge Care", font=("Segoe UI", 20, "bold"),
                 bg=self.colors["surface2"], fg=self.colors["primary"]).pack(side=tk.LEFT, padx=20)
        tk.Label(header, text=self.current_user, bg=self.colors["surface2"], fg=self.colors["text2"]).pack(side=tk.RIGHT, padx=20)
        tk.Button(header, text="Выйти", bg=self.colors["danger"], fg="white",
                  relief=tk.FLAT, command=self.logout).pack(side=tk.RIGHT, padx=10)

        main = tk.Frame(self.parent, bg=self.colors["bg"])
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        menu = tk.Frame(main, bg=self.colors["surface"], relief=tk.RIDGE, bd=1)
        menu.pack(fill=tk.X, pady=10)
        tk.Label(menu, text="Модули", font=("Segoe UI", 14, "bold"),
                 bg=self.colors["surface"], fg=self.colors["primary"]).pack(anchor=tk.W, padx=15, pady=10)

        btns = tk.Frame(menu, bg=self.colors["surface"])
        btns.pack(padx=15, pady=10)

        modules = [
            ("🧠 Психология", self.controller.open_psychology, self.colors["primary"]),
            ("🏋️ Реабилитация", self.controller.open_rehab, self.colors["success"]),
            ("🤟 Перевод жестов", self.controller.open_gesture, self.colors["danger"])
        ]

        for i, (text, cmd, color) in enumerate(modules):
            btn = tk.Button(btns, text=text, bg=color, fg="white",
                            font=("Segoe UI", 11), relief=tk.FLAT, height=2, command=cmd)
            btn.grid(row=i, column=0, padx=5, pady=5, sticky="ew")
        btns.grid_columnconfigure(0, weight=1)

        info = tk.Frame(main, bg=self.colors["surface2"], relief=tk.RIDGE, bd=1)
        info.pack(fill=tk.X, pady=10)
        tk.Label(info, text="Совет дня", font=("Segoe UI", 12, "bold"),
                 bg=self.colors["surface2"], fg=self.colors["primary"]).pack(anchor=tk.W, padx=15, pady=5)
        tk.Label(info, text="Сделайте глубокий вдох", bg=self.colors["surface2"], fg=self.colors["text2"]).pack(anchor=tk.W, padx=15, pady=5)

    def logout(self):
        self.current_user = None
        self.create_login()