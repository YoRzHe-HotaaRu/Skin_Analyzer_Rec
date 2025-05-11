# webcam_handler.py
from tkinter import messagebox

import cv2
import tkinter as tk
from PIL import Image, ImageTk
from face_detector import detect_and_analyze_face
import numpy as np

class WebcamApp:
    def __init__(self, window, video_source=0):
        self.window = window
        self.video_source = video_source

        self.vid = MyVideoCapture(self.video_source)

        self.canvas = tk.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        self.delay = 15
        self.update()

        self.window.mainloop()

    def update(self):
        ret, frame = self.vid.get_frame()
        if ret:
            # Adjust brightness
            brightness_factor = 1.2  # Increase or decrease as needed
            adjusted_frame = cv2.convertScaleAbs(frame, alpha=brightness_factor, beta=0)
            rgb_frame = cv2.cvtColor(adjusted_frame, cv2.COLOR_BGR2RGB)

            # Convert frame to PIL Image before passing to detect_and_analyze_face
            pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            analyzed_frame = detect_and_analyze_face(pil_image)

            # Convert back to NumPy array for display
            analyzed_frame_np = np.array(analyzed_frame)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(analyzed_frame_np))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)



        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Adjust camera settings (optional)
        self.vid.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)  # Range: 0.0 to 1.0
        self.vid.set(cv2.CAP_PROP_CONTRAST, 0.6)  # Range: 0.0 to 1.0
        self.vid.set(cv2.CAP_PROP_SATURATION, 0.9)  # Range: 0.0 to 1.0
        self.vid.set(cv2.CAP_PROP_HUE, 1.0)  # Adjust hue
        self.vid.set(cv2.CAP_PROP_GAIN, 0.5)  # Adjust gain
        self.vid.set(cv2.CAP_PROP_EXPOSURE, -4)  # Adjust exposure (-1 = auto, 0–1 = manual)


        self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))





    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return ret, frame
            else:
                return ret, None
        else:
            return None


def launch_webcam_app(webcam_index):
    root = tk.Toplevel()
    root.title("Webcam Preview")
    try:
        WebcamApp(root, video_source=webcam_index)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open webcam:\n{e}")