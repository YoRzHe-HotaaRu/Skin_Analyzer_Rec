# face_detector.py

import cv2
from skin_analyzer import analyze_skin
from PIL import Image
import numpy as np


def face_detector(image):
    # Example: Using OpenCV's Haar Cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    results = []
    for (x, y, w, h) in faces:
        results.append({
            'label': 'face',
            'box': {'xmin': x, 'ymin': y, 'xmax': x + w, 'ymax': y + h},
            'score': 1.0  # Confidence score (you can adjust this)
        })

    return results


def detect_and_analyze_face(face_img):
    # Convert PIL Image to NumPy array
    face_array = np.array(face_img)

    # Detect faces using Hugging Face pipeline
    results = face_detector(face_array)
    for res in results:
        if "face" in res['label'].lower():
            box = res['box']
            score = res['score']
            x1, y1, x2, y2 = box.values()

            # Crop face region
            face_region = face_array[y1:y2, x1:x2]

            # Analyze skin condition
            label, confidence = analyze_skin(face_region)
            print(f"Detected: {label}, Confidence: {confidence:.2f}")

            # Draw bounding box and label on the original frame
            cv2.rectangle(face_array, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(face_array, f"{label} ({confidence:.2f})", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Convert back to PIL Image for consistency
    pil_image = Image.fromarray(cv2.cvtColor(face_array, cv2.COLOR_BGR2RGB))
    return pil_image