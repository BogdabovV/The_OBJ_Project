import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pyttsx3
import json
import os
from datetime import datetime

# Конфигурация жестов
GESTURES = {
    1: "Привет",
    2: "Да",
    3: "Нет",
    4: "Спасибо",
    5: "Помощь"
}

# Глобальные переменные состояния
cap = None
is_running = False
engine = pyttsx3.init()
history_log = []

# Инициализация MediaPipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands_detector = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7
)


def count_fingers(landmarks):
    """Подсчет поднятых пальцев."""
    tips_ids = [4, 8, 12, 16, 20]
    pip_ids = [3, 6, 10, 14, 18]
    count = 0
    for tip, pip in zip(tips_ids, pip_ids):
        if landmarks.landmark[tip].y < landmarks.landmark[pip].y:
            count += 1
    return count


def process_frame():
    """Основной цикл обработки видео."""
    global is_running

    if is_running:
        ret, frame = cap.read()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands_detector.process(rgb_frame)

            detected_word = ""

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    fingers_count = count_fingers(hand_landmarks)
                    detected_word = GESTURES.get(fingers_count, "")

            # Обновление интерфейса
            update_ui(frame, detected_word)

            # Рекурсивный вызов для обновления кадров
            root.after(10, process_frame)


def update_ui(frame, word):
    """Отрисовка кадра и обработка распознанного жеста."""
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    img = img.resize((640, 480))
    imgtk = ImageTk.PhotoImage(image=img)

    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    if word:
        status_var.set(f"Распознано: {word}")
        add_history("Жест", word)
        speak_text(word)
        update_history_display()
    else:
        status_var.set("Камера активна")


def add_history(source, text):
    """Добавление записи в историю."""
    entry = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "source": source,
        "text": text
    }
    history_log.append(entry)
    save_history()


def save_history():
    """Сохранение истории в файл."""
    with open("history.json", "w", encoding="utf-8") as f:
        json.dump(history_log, f, ensure_ascii=False, indent=2)


def load_history():
    """Загрузка истории при старте."""
    global history_log
    if os.path.exists("history.json"):
        try:
            with open("history.json", "r", encoding="utf-8") as f:
                history_log = json.load(f)
        except:
            history_log = []


def update_history_display():
    """Вывод истории в текстовое поле."""
    history_text.delete("1.0", tk.END)
    for item in history_log[-15:]:
        line = f"[{item['time']}] {item['source']}: {item['text']}\n"
        history_text.insert(tk.END, line)


def speak_text(text):
    """Озвучивание текста."""
    if text:
        engine.say(text)
        engine.runAndWait()


def toggle_camera():
    """Включение/выключение камеры."""
    global is_running, cap

    if is_running:
        is_running = False
        if cap:
            cap.release()
        btn_camera.config(text="Включить камеру", bg="#3498db")
        video_label.config(image='')
        status_var.set("Камера выключена")
    else:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Ошибка", "Не удалось открыть камеру")
            return
        is_running = True
        btn_camera.config(text="Выключить камеру", bg="#e74c3c")
        process_frame()


def manual_speak():
    """Озвучивание введенного текста."""
    text = input_text.get("1.0", tk.END).strip()
    if text:
        speak_text(text)
        add_history("Текст", text)
        update_history_display()


def send_sos():
    """Экстренный сигнал."""
    msg = "ТРЕБУЕТСЯ ПОМОЩЬ"
    messagebox.showwarning("ВНИМАНИЕ", msg)
    speak_text(msg)
    add_history("SOS", msg)
    update_history_display()


# --- Интерфейс (Tkinter) ---
root = tk.Tk()
root.title("SignBridge Project")
root.geometry("900x750")
root.configure(bg="#f5f5f5")

# Заголовок
header = tk.Label(root, text="SignBridge", font=("Arial", 20, "bold"), bg="#f5f5f5")
header.pack(pady=10)

# Область видео
video_label = tk.Label(root, bg="black", width=640, height=480)
video_label.pack(pady=5)

# Статус
status_var = tk.StringVar(value="Готов к работе")
status_lbl = tk.Label(root, textvariable=status_var, font=("Arial", 10), bg="#f5f5f5", fg="#555")
status_lbl.pack()

# Панель управления
control_frame = tk.Frame(root, bg="#f5f5f5")
control_frame.pack(pady=10)

btn_camera = tk.Button(control_frame, text="Включить камеру", command=toggle_camera,
                       bg="#3498db", fg="white", font=("Arial", 10), width=15)
btn_camera.grid(row=0, column=0, padx=5)

btn_speak = tk.Button(control_frame, text="Озвучить текст", command=manual_speak,
                      bg="#2ecc71", fg="white", font=("Arial", 10), width=15)
btn_speak.grid(row=0, column=1, padx=5)

btn_sos = tk.Button(control_frame, text="SOS", command=send_sos,
                    bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), width=10)
btn_sos.grid(row=0, column=2, padx=5)

# Поле ввода текста
tk.Label(root, text="Ввод текста:", bg="#f5f5f5").pack(anchor="w", padx=140)
input_text = tk.Text(root, height=3, width=70)
input_text.pack(padx=140)

# История
tk.Label(root, text="История сообщений:", font=("Arial", 10, "bold"), bg="#f5f5f5").pack(anchor="w", padx=140,
                                                                                         pady=(10, 0))
history_text = tk.Text(root, height=12, width=75, state="normal")
history_text.pack(padx=140, pady=5)

# Загрузка данных при старте
load_history()
update_history_display()
engine.setProperty('rate', 150)


# Обработка закрытия окна
def on_closing():
    global is_running
    is_running = False
    if cap:
        cap.release()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()