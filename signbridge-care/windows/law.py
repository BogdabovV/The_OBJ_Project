import tkinter as tk
from tkinter import messagebox


class LawWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("⚖️ Юридическая помощь")
        self.window.geometry("600x450")
        self.window.configure(bg="#0f0f1a")

        tk.Label(
            self.window, text="⚖️ Юридическая помощь", font=("Segoe UI", 20, "bold"),
            bg="#0f0f1a", fg="#e74c3c"
        ).pack(pady=20)

        benefits = ["🏠 Бесплатное жилье", "💊 Бесплатные лекарства", "🚗 Налоговые льготы", "🏥 Санаторное лечение"]
        for b in benefits:
            tk.Label(self.window, text=b, font=("Segoe UI", 12), bg="#0f0f1a", fg="#a8b2d1").pack(anchor=tk.W, padx=30,
                                                                                                  pady=3)

        tk.Button(self.window, text="📝 Заявление на льготы", bg="#4a90e2", fg="white", relief=tk.FLAT, height=2,
                  command=lambda: messagebox.showinfo("Заявление", "Сформировано заявление")).pack(pady=20, padx=30,
                                                                                                   fill=tk.X)
        tk.Button(self.window, text="💬 Чат с юристом", bg="#9b59b6", fg="white", relief=tk.FLAT, height=2,
                  command=lambda: messagebox.showinfo("Чат", "Юрист ответит в ближайшее время")).pack(pady=5, padx=30,
                                                                                                      fill=tk.X)