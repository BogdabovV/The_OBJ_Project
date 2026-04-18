import tkinter as tk
from windows.main_window import MainWindow


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SignBridge")
        self.root.geometry("900x600")
        self.root.configure(bg="#0f0f1a")

        self.main = MainWindow(self.root, self)

    def open_psychology(self):
        from windows.psychology import PsychologyWindow
        PsychologyWindow(self.root)

    def open_rehab(self):
        from windows.rehab import RehabWindow
        RehabWindow(self.root)

    def open_gesture(self):
        from windows.gesture import GestureWindow
        GestureWindow(self.root)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()