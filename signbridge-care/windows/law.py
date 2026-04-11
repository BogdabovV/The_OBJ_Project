import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox


class LawWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("⚖️ Юридический помощник")
        self.window.geometry("800x600")
        self.window.configure(bg="#1a1a2e")
        self.window.transient(parent)

        self.build()

    def build(self):
        tk.Label(
            self.window,
            text="⚖️ Юридический помощник",
            font=("Segoe UI", 20, "bold"),
            bg="#1a1a2e",
            fg="#9b59b6"
        ).pack(pady=10)

        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Льготы
        benefits_frame = tk.Frame(notebook, bg="#16213e")
        notebook.add(benefits_frame, text="📋 Льготы")

        benefits = [
            "🏠 Бесплатное жилье",
            "💊 Бесплатные лекарства",
            "🚗 Налоговые льготы",
            "🏥 Санаторно-курортное лечение",
            "📚 Бесплатное образование",
            "🚌 Бесплатный проезд"
        ]

        for b in benefits:
            tk.Label(
                benefits_frame,
                text=b,
                font=("Segoe UI", 12),
                bg="#16213e",
                fg="#a8b2d1"
            ).pack(anchor=tk.W, padx=20, pady=5)

        # Генератор заявлений
        gen_frame = tk.Frame(notebook, bg="#16213e")
        notebook.add(gen_frame, text="📝 Генератор заявлений")

        tk.Label(
            gen_frame,
            text="Выберите тип заявления:",
            font=("Segoe UI", 12),
            bg="#16213e",
            fg="white"
        ).pack(pady=10)

        types = ["На получение льгот", "На выплату", "На санаторное лечение"]

        for t in types:
            tk.Button(
                gen_frame,
                text=t,
                bg="#9b59b6",
                fg="white",
                width=30,
                command=lambda x=t: self.generate(x)
            ).pack(pady=5)

        # Чат
        chat_frame = tk.Frame(notebook, bg="#16213e")
        notebook.add(chat_frame, text="💬 Чат с юристом")

        self.chat_area = scrolledtext.ScrolledText(
            chat_frame,
            height=15,
            bg="#0f172a",
            fg="white"
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.chat_area.insert(tk.END, "Юрист: Здравствуйте! Задайте ваш вопрос о льготах и выплатах\n\n")
        self.chat_area.config(state=tk.DISABLED)

        input_frame = tk.Frame(chat_frame, bg="#16213e")
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        self.msg_entry = tk.Entry(input_frame, bg="#0f172a", fg="white")
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.msg_entry.bind("<Return>", self.send_legal)

        tk.Button(
            input_frame,
            text="Отправить",
            bg="#9b59b6",
            fg="white",
            command=self.send_legal
        ).pack(side=tk.RIGHT)

    def generate(self, doc_type):
        messagebox.showinfo("Заявление", f"Сформировано заявление: {doc_type}\n\nПроверьте данные и отправьте")

    def send_legal(self, event=None):
        msg = self.msg_entry.get().strip()
        if msg:
            self.chat_area.config(state=tk.NORMAL)
            self.chat_area.insert(tk.END, f"Вы: {msg}\n")
            self.chat_area.insert(tk.END,
                                  f"Юрист: Спасибо за вопрос. Мы свяжемся с вами в ближайшее время для консультации\n\n")
            self.chat_area.see(tk.END)
            self.chat_area.config(state=tk.DISABLED)
            self.msg_entry.delete(0, tk.END)