import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading
import time
import cv2
import mediapipe as mp

class GestureWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Перевод жестов")
        self.window.geometry("900x650")
        self.window.configure(bg="#0f0f1a")

        self.cam_on = False
        self.cam = None
        self.auto = False
        self.last_gesture = ""

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        self.mp_draw = mp.solutions.drawing_utils

        self.colors = {
            "bg": "#0f0f1a", "surface": "#1a1a2e", "surface2": "#16213e",
            "primary": "#4a90e2", "success": "#2ecc71", "danger": "#e74c3c",
            "text": "#cdd6f4", "text2": "#a8b2d1"
        }

        self.build()

    def build(self):
        tk.Label(self.window, text="Перевод жестов", font=("Segoe UI", 20, "bold"),
                 bg=self.colors["bg"], fg=self.colors["primary"]).pack(pady=10)

        main = tk.Frame(self.window, bg=self.colors["bg"])
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        left = tk.Frame(main, bg=self.colors["surface"], relief=tk.RIDGE, bd=1)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,10))

        self.video = tk.Label(left, bg=self.colors["bg"], width=500, height=380)
        self.video.pack(padx=15, pady=15)

        btnf = tk.Frame(left, bg=self.colors["surface"])
        btnf.pack(fill=tk.X, padx=15, pady=15)

        self.cam_btn = tk.Button(btnf, text="Включить камеру", bg=self.colors["success"], fg="black",
                                 relief=tk.FLAT, command=self.toggle_cam)
        self.cam_btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        self.auto_btn = tk.Button(btnf, text="Авто", bg=self.colors["primary"], fg="white",
                                  relief=tk.FLAT, command=self.toggle_auto)
        self.auto_btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        self.rec_btn = tk.Button(btnf, text="Распознать", bg=self.colors["primary"], fg="white",
                                 relief=tk.FLAT, command=self.recognize, state=tk.DISABLED)
        self.rec_btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        right = tk.Frame(main, bg=self.colors["surface"], relief=tk.RIDGE, bd=1, width=300)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        right.pack_propagate(False)

        tk.Label(right, text="Результат", font=("Segoe UI", 14, "bold"),
                 bg=self.colors["surface"], fg=self.colors["text"]).pack(anchor=tk.W, padx=15, pady=10)

        self.result = tk.Text(right, height=5, font=("Segoe UI", 18), bg=self.colors["surface2"],
                              fg=self.colors["text"], wrap=tk.WORD)
        self.result.pack(fill=tk.X, padx=15, pady=5)

        rbtn = tk.Frame(right, bg=self.colors["surface"])
        rbtn.pack(fill=tk.X, padx=15, pady=10)

        tk.Button(rbtn, text="Озвучить", bg=self.colors["primary"], fg="white", relief=tk.FLAT, command=self.speak).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        tk.Button(rbtn, text="Копировать", bg=self.colors["primary"], fg="white", relief=tk.FLAT, command=self.copy).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        tk.Button(rbtn, text="Очистить", bg=self.colors["danger"], fg="white", relief=tk.FLAT, command=self.clear).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)

        self.status = tk.Label(right, text="Готов", bg=self.colors["surface"], fg=self.colors["success"])
        self.status.pack(pady=10)

        tk.Label(right, text="Доступные жесты", font=("Segoe UI", 12, "bold"),
                 bg=self.colors["surface"], fg=self.colors["primary"]).pack(anchor=tk.W, padx=15)

        hints = """1 палец → привет
2 пальца → да
3 пальца → нет
4 пальца → спасибо
5 пальцев → помощь
Кулак → стоп
👍 → отлично
👎 → плохо"""
        tk.Label(right, text=hints, bg=self.colors["surface"], fg=self.colors["text2"], justify=tk.LEFT).pack(anchor=tk.W, padx=15, pady=5)

    def toggle_cam(self):
        if not self.cam_on:
            try:
                self.cam = cv2.VideoCapture(0)
                if not self.cam.isOpened():
                    raise Exception()
                self.cam_on = True
                self.cam_btn.configure(text="Выключить", bg=self.colors["danger"])
                self.rec_btn.configure(state=tk.NORMAL)
                threading.Thread(target=self.update, daemon=True).start()
            except:
                messagebox.showerror("Ошибка", "Камера не найдена")
        else:
            self.cam_on = False
            if self.cam:
                self.cam.release()
            self.cam_btn.configure(text="Включить", bg=self.colors["success"])
            self.rec_btn.configure(state=tk.DISABLED)
            self.video.configure(image="")
            self.status.configure(text="Камера выключена", fg=self.colors["danger"])

    def update(self):
        while self.cam_on and self.cam:
            ret, frame = self.cam.read()
            if ret:
                frame = cv2.flip(frame, 1)
                gesture = self.detect(frame)

                if gesture and self.auto and gesture != self.last_gesture:
                    self.last_gesture = gesture
                    self.window.after(0, lambda: self.add(gesture))

                frame = cv2.resize(frame, (500, 380))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(img)

                self.video.configure(image=imgtk)
                self.video.image = imgtk
            time.sleep(0.03)

    def detect(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = self.hands.process(rgb)
        if res.multi_hand_landmarks:
            for hand in res.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand, self.mp_hands.HAND_CONNECTIONS)
                lm = hand.landmark
                fingers = 0
                if lm[4].x < lm[3].x:
                    fingers += 1
                for tip in [8, 12, 16, 20]:
                    if lm[tip].y < lm[tip-2].y:
                        fingers += 1

                thumb_up = lm[4].y < lm[3].y
                if thumb_up and fingers == 1:
                    return "отлично"
                if not thumb_up and fingers == 1:
                    return "плохо"
                return {1: "привет", 2: "да", 3: "нет", 4: "спасибо", 5: "помощь", 0: "стоп"}.get(fingers)
        return None

    def toggle_auto(self):
        self.auto = not self.auto
        self.auto_btn.configure(text="Авто вкл" if self.auto else "Авто",
                                bg=self.colors["success"] if self.auto else self.colors["primary"])
        self.status.configure(text="Авто вкл" if self.auto else "Авто выкл",
                              fg=self.colors["success"] if self.auto else self.colors["text2"])

    def recognize(self):
        if not self.cam_on:
            return
        ret, frame = self.cam.read()
        if ret:
            frame = cv2.flip(frame, 1)
            g = self.detect(frame)
            if g:
                self.add(g)
                self.speak_word(g)
                self.status.configure(text=f"Распознано: {g}", fg=self.colors["success"])
            else:
                self.status.configure(text="Жест не распознан", fg=self.colors["danger"])

    def add(self, word):
        self.result.delete("1.0", tk.END)
        self.result.insert("1.0", word)

    def speak_word(self, word):
        try:
            import pyttsx3
            e = pyttsx3.init()
            e.say(word)
            e.runAndWait()
        except:
            pass

    def speak(self):
        t = self.result.get("1.0", tk.END).strip()
        if t:
            self.speak_word(t)

    def copy(self):
        t = self.result.get("1.0", tk.END).strip()
        if t:
            self.window.clipboard_clear()
            self.window.clipboard_append(t)

    def clear(self):
        self.result.delete("1.0", tk.END)
        self.status.configure(text="Очищено", fg=self.colors["text2"])