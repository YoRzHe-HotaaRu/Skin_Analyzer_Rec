# gui_menu.py

import customtkinter as ctk
from tkinter import messagebox
import cv2

from webcam_handler import launch_webcam_app


class FaceAnalyzerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Face Analyzer <3")
        self.geometry("400x300")

        self.label = ctk.CTkLabel(self, text="Welcome to Face Analyzer", font=("Arial", 20))
        self.label.pack(pady=20)

        # Button to choose webcam
        self.choose_webcam_btn = ctk.CTkButton(self, text="Choose Webcam", command=self.choose_webcam)
        self.choose_webcam_btn.pack(pady=10)

        self.start_btn = ctk.CTkButton(self, text="Start", command=self.start_app)
        self.start_btn.pack(pady=10)

        self.exit_btn = ctk.CTkButton(self, text="Exit App", command=self.destroy)
        self.exit_btn.pack(pady=10)

        # Store selected webcam index
        self.selected_webcam_index = None

    def choose_webcam(self):
        """Detect available webcams and let the user choose one."""
        available_cameras = get_available_webcams()

        if not available_cameras:
            messagebox.showinfo("No Webcams Found", "No webcams detected on your system.")
            return

        # Show available webcams in a message box
        webcam_list = "\n".join([f"Webcam {i}" for i in available_cameras])
        choice = messagebox.askquestion(
            "Available Webcams",
            f"Found {len(available_cameras)} webcams:\n{webcam_list}\n\nSelect which webcam to use."
        )

        if choice == "yes":
            # For simplicity, we'll just use the first available webcam
            # You can add a more advanced selection method if needed
            self.selected_webcam_index = available_cameras[0]
            print(f"Selected Webcam: {self.selected_webcam_index}")
        else:
            print("Webcam selection canceled.")

    def start_app(self):
        print("Starting webcam preview...")
        # Pass the selected webcam index to the webcam handler
        if self.selected_webcam_index is not None:
            launch_webcam_app(self.selected_webcam_index)
        else:
            messagebox.showwarning("No Webcam Selected", "Please select a webcam before starting.")


def get_available_webcams():
    """Detect all available webcams."""
    index = 0
    available_cameras = []

    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            available_cameras.append(index)
        cap.release()
        index += 1

    return available_cameras


if __name__ == "__main__":
    app = FaceAnalyzerApp()
    app.mainloop()