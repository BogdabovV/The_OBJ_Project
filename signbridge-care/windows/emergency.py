import tkinter as tk
from tkinter import messagebox


class EmergencyWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("🆘 Экстренная помощь")
        self.window.geometry("500x400")
        self.window.configure(bg="#0f0f1a")

        tk.Button(
            self.window, text="🆘 МНЕ ПЛОХО", font=("Segoe UI", 20, "bold"),
            bg="#e74c3c", fg="white", height=2, command=self.emergency
        ).pack(pady=30, padx=30, fill=tk.X)

        hotlines_frame = tk.Frame(self.window, bg="#1a1a2e", relief=tk.RIDGE, bd=1)
        hotlines_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(hotlines_frame, text="📞 Горячие линии", font=("Segoe UI", 14, "bold"), bg="#1a1a2e",
                 fg="#4a90e2").pack(anchor=tk.W, padx=15, pady=5)

        hotlines = [("Психологическая помощь", "8-800-XXX-XX-XX"), ("Скорая помощь", "103"),
                    ("Кризисная линия", "8-800-XXX-XX-XX")]
        for name, phone in hotlines:
            frame = tk.Frame(hotlines_frame, bg="#1a1a2e")
            frame.pack(fill=tk.X, padx=15, pady=3)
            tk.Label(frame, text=name, bg="#1a1a2e", fg="#cdd6f4").pack(side=tk.LEFT)
            tk.Label(frame, text=phone, bg="#1a1a2e", fg="#4a90e2").pack(side=tk.RIGHT)

    def emergency(self):
        if messagebox.askyesno("Экстренная помощь", "Вызвать помощь?"):
            messagebox.showinfo("Помощь", "Специалист свяжется с вами")