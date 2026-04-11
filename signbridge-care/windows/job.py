import tkinter as tk
from tkinter import ttk, messagebox


class JobWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("💼 Трудоустройство")
        self.window.geometry("800x600")
        self.window.configure(bg="#1a1a2e")
        self.window.transient(parent)

        self.build()

    def build(self):
        tk.Label(
            self.window,
            text="💼 Трудоустройство и образование",
            font=("Segoe UI", 20, "bold"),
            bg="#1a1a2e",
            fg="#f39c12"
        ).pack(pady=10)

        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Вакансии
        vac_frame = tk.Frame(notebook, bg="#16213e")
        notebook.add(vac_frame, text="📋 Вакансии")

        vacancies = [
            ("IT-специалист", "Удаленно", "от 80 000 ₽"),
            ("Менеджер по работе с клиентами", "Москва", "от 60 000 ₽"),
            ("Водитель", "Санкт-Петербург", "от 70 000 ₽"),
            ("Охранник", "Москва", "от 50 000 ₽"),
            ("Сборщик заказов", "Удаленно", "от 45 000 ₽")
        ]

        for title, city, salary in vacancies:
            frame = tk.Frame(vac_frame, bg="#0f172a", relief=tk.RIDGE)
            frame.pack(fill=tk.X, padx=10, pady=5)

            tk.Label(
                frame,
                text=title,
                font=("Segoe UI", 12, "bold"),
                bg="#0f172a",
                fg="#f39c12"
            ).pack(anchor=tk.W, padx=10, pady=2)

            tk.Label(
                frame,
                text=f"📍 {city} | 💰 {salary}",
                font=("Segoe UI", 10),
                bg="#0f172a",
                fg="#a8b2d1"
            ).pack(anchor=tk.W, padx=10)

            tk.Button(
                frame,
                text="Откликнуться",
                bg="#2ecc71",
                fg="white",
                command=lambda t=title: self.apply(t)
            ).pack(anchor=tk.E, padx=10, pady=5)

        # Курсы
        courses_frame = tk.Frame(notebook, bg="#16213e")
        notebook.add(courses_frame, text="📚 Курсы")

        courses = [
            "Программирование Python",
            "Веб-дизайн",
            "1С Предприятие",
            "Английский язык",
            "Бухгалтерия"
        ]

        for c in courses:
            tk.Button(
                courses_frame,
                text=c,
                font=("Segoe UI", 12),
                bg="#4a90e2",
                fg="white",
                width=30,
                height=2,
                command=lambda t=c: self.enroll(t)
            ).pack(pady=5)

        # Резюме
        resume_frame = tk.Frame(notebook, bg="#16213e")
        notebook.add(resume_frame, text="📄 Конструктор резюме")

        tk.Label(
            resume_frame,
            text="Создайте резюме за 5 минут",
            font=("Segoe UI", 14),
            bg="#16213e",
            fg="white"
        ).pack(pady=10)

        fields = [
            ("ФИО", tk.Entry),
            ("Телефон", tk.Entry),
            ("Опыт работы", tk.Text),
            ("Образование", tk.Entry)
        ]

        for label, widget_type in fields:
            frame = tk.Frame(resume_frame, bg="#16213e")
            frame.pack(fill=tk.X, padx=20, pady=5)

            tk.Label(
                frame,
                text=label,
                bg="#16213e",
                fg="white",
                width=15,
                anchor=tk.W
            ).pack(side=tk.LEFT)

            if widget_type == tk.Text:
                w = tk.Text(frame, height=3, bg="#0f172a", fg="white")
                w.pack(side=tk.LEFT, fill=tk.X, expand=True)
            else:
                w = tk.Entry(frame, bg="#0f172a", fg="white")
                w.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Button(
            resume_frame,
            text="Сохранить резюме",
            bg="#2ecc71",
            fg="white",
            command=lambda: messagebox.showinfo("Готово", "Резюме сохранено")
        ).pack(pady=20)

    def apply(self, title):
        messagebox.showinfo("Отклик", f"Вы откликнулись на вакансию: {title}\n\nСпециалист свяжется с вами")

    def enroll(self, course):
        messagebox.showinfo("Запись", f"Вы записаны на курс: {course}\n\nСсылка придет на email")