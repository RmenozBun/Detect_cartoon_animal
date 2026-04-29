import tkinter as tk
import os
from PIL import Image, ImageTk
import random
import speech_recognition as sr
import pyttsx3
import cv2
from ultralytics import YOLO
import math

class g_c_picture:
    def __init__(self, root):
        self.root = root
        self.model = YOLO("detect_cartoon_animal/runs/detect/train/weights/best.pt")
        self.animal_signs = ['anteater', 'chicken', 'donkey', 'dugong', 'elephant', 'giraffe', 'kangaroo', 'monkey', 'panda', 'rabbit']
        self.current_sign = self.new_task()
        self.score = 0
        self.root = root
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)
        self.engine.setProperty("volume", 1.0)
        voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", voices[1].id)
        self.frame_label = tk.Label(root)
        self.frame_label.pack(pady=10)
        self.result_label = tk.Label(root, text="", font=("Arial", 14))
        self.result_label.pack(pady=20)
        self.start_button = tk.Button(root, text="Restart", command=self.start_game, font=("Arial", 12))
        self.start_button.pack(pady=30)
        self.start_button.pack_forget()
        self.back_button = tk.Button(root, text="Back to Menu", command=self.back_to_menu, font=("Arial", 12))
        self.back_button.pack(pady=40)
        self.back_button.pack_forget()
        self.cap = cv2.VideoCapture(0)
        self.speak(f"Guessing Questions: {self.current_sign}")
        self.update_frame()
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
    def new_task(self):
        return random.choice(self.animal_signs)
    def start_game(self):
        self.start_button.pack_forget()
        self.back_button.pack_forget()
        self.speak("Start!")
        self.result_label.config(text=f"")
        self.score = 0
        self.current_sign = self.new_task()
        self.cap = cv2.VideoCapture(0)
        self.update_frame()
    def back_to_menu(self):
        self.cap.release()
        cv2.destroyAllWindows()
        clear_widgets()
        show_menu()
    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        results = self.model(frame)
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                class_id = int(box.cls[0])
                label = self.animal_signs[class_id]
                conff = math.ceil(conf * 100)
                self.cf = conff
                self.root.after(100)
                if conff < 70 or label != self.current_sign:
                    continue
                if conff > 70 and label == self.current_sign:
                    self.speak("That's right!")
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    self.score += 1
                    self.current_sign = self.new_task()
                    if self.score < 10:
                        self.speak(f"Guessing Questions: {self.current_sign}")
        if self.score < 10:
            cv2.putText(frame, f'Guessing Questions: {self.current_sign}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
            cv2.putText(frame, f'Score: {self.score}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        self.result_label.config(text=f"Your score: {self.score}/10")
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img_tk = ImageTk.PhotoImage(img)
        self.frame_label.img_tk = img_tk
        self.frame_label.config(image=img_tk)
        if self.score < 10:
            self.root.after(50, self.update_frame)
        else:
            self.result_label.config(text=f"Game over! Your score: {self.score}/10")
            self.speak(f"You have scored {self.score} points out of 10.")
            self.cap.release()
            cv2.destroyAllWindows()
            self.start_button.pack()
            self.back_button.pack()

class g_c_name:
    def __init__(self, root):
        self.root = root
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)
        self.engine.setProperty("volume", 1.0)
        voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", voices[1].id)
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=10)
        self.result_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)
        self.start_button = tk.Button(self.root, text="Start", command=self.start_game, font=("Arial", 12))
        self.start_button.pack(pady=20)
        self.back_button = tk.Button(self.root, text="Back to Menu", command=self.back_to_menu, font=("Arial", 12))
        self.back_button.pack(pady=30)
        self.image_files = self.load_images("c_picture")
        self.score = 0
        self.round_num = 0
        self.used_images = []
        self.current_image = None
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
    def listen(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.speak("🎤 Say the name of the picture...")
            self.result_label.config(text="🎤 Say the name of the picture...")
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout=10)
                text = recognizer.recognize_google(audio, language="en-EN")
                self.result_label.config(text=f"👂 You say : {text}")
                self.speak(f"👂 You say : {text}")
                return text.strip().lower()
            except:
                self.result_label.config(text="Can't understand or too quiet")
                self.speak("Can't understand or too quiet")
                return None
    def load_images(self, folder="c_picture"):
        images = []
        for file in os.listdir(folder):
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                name = os.path.splitext(file)[0].lower()
                images.append((name, os.path.join(folder, file)))
        return images
    def show_image(self, path):
        img = Image.open(path)
        img = img.resize((300, 300))
        photo = ImageTk.PhotoImage(img)
        self.image_label.config(image=photo)
        self.image_label.image = photo
    def start_game(self):
        self.start_button.pack_forget()
        self.back_button.pack_forget()
        self.speak("Start!")
        self.score = 0
        self.round_num = 0
        self.used_images = []
        self.game_running = True
        self.next_round()
    def back_to_menu(self):
        self.game_running = False
        clear_widgets()
        show_menu()
    def next_round(self):
        if not self.game_running: return
        if self.round_num >= 10:
            self.result_label.config(text=f"Game over! Your score: {self.score}/10")
            self.speak(f"You have scored {self.score} points out of 10.")
            self.start_button.pack()
            self.back_button.pack()
            return
        available = [img for img in self.image_files if img not in self.used_images]
        if not available:
            self.result_label.config(text="There are no more images left to randomize.")
            return
        self.current_image = random.choice(available)
        self.used_images.append(self.current_image)
        self.show_image(self.current_image[1])
        self.round_num += 1
        self.result_label.config(text="What is this picture?")
        self.speak("What is this picture?")
        self.root.after(1000, self.get_user_answer)
    def get_user_answer(self):
        if not self.game_running: return
        user_input = self.listen()
        if not self.game_running: return
        if user_input:
            if user_input == self.current_image[0]:
                self.result_label.config(text="That's right!")
                self.speak("That's right!")
                self.score += 1
            else:
                self.result_label.config(text=f"Wrong. The answer is {self.current_image[0]}")
                self.speak(f"Wrong. The answer is {self.current_image[0]}")
        else:
            self.result_label.config(text=f"Unable to hear the answer. The answer is {self.current_image[0]}")
            self.speak(f"Unable to hear the answer. The answer is {self.current_image[0]}")
        self.root.after(1500, self.next_round)
        
def clear_widgets():
    for widget in root.winfo_children():
        widget.destroy()
def show_menu():
    label = tk.Label(root, text="CHOOSE MODE", font=("Arial", 12))
    label.pack(pady=10)
    button_picture = tk.Button(root, text="GUESSING PICTURE", command=lambda: [clear_widgets(), g_c_picture(root)])
    button_picture.pack(pady=20)
    button_name = tk.Button(root, text="GUESSING NAME", command=lambda: [clear_widgets(), g_c_name(root)])
    button_name.pack(pady=20)
    button_exit = tk.Button(root, text="EXIT", command=root.quit)
    button_exit.pack(pady=10)
def main():
    global root
    root = tk.Tk()
    root.title("ANIMAL GUESSING GAME")
    root.geometry("800x800")
    show_menu()
    root.mainloop()
if __name__ == '__main__': main()