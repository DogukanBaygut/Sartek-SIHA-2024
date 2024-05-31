# -*- coding: utf-8 -*-
"""
Created on Fri May 31 15:18:57 2024
SARTEK SİHA PROJESİ
@author: Doğukan AVCI
"""

# görüntü_isleme.py
from ultralytics import YOLO
import cv2
import cvzone
import math
import time

class GoruntuIsleme:
    def __init__(self, model_path, video_path):
        self.model = YOLO(model_path)
        self.cap = cv2.VideoCapture(video_path)
        self.cv2_fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        success, img = self.cap.read()
        if not success:
            print("Video okunamadı")
            self.cap.release()
            exit()
        
        size = list(img.shape)
        del size[2]
        size.reverse()
        self.video = cv2.VideoWriter("kaydedilen_video.mp4", self.cv2_fourcc, 24, size)
        self.start_time = None
        self.inside_green_area = False

    def process_frame(self):
        success, img = self.cap.read()
        if not success:
            return None, False

        img = cv2.resize(img, (1280, 720), interpolation=cv2.INTER_AREA)
        results = self.model(img, stream=True)
        detected = False
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1
                cvzone.cornerRect(img, (x1, y1, w, h))
                conf = math.ceil((box.conf[0] * 100)) / 100
                cls = int(box.cls[0])

                cvzone.putTextRect(img, f' UAV {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

                cx, cy = x1 + w // 2, y1 + h // 2
                cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

                cx2, cy2 = 1280 // 2, 720 // 2
                cv2.circle(img, (cx2, cy2), 5, (255, 0, 255), cv2.FILLED)

                rect_color = (0, 0, 255)  # Başlangıçta kırmızı (RGB)
                text = "Ateşlemeye Hazır Değil"
                lock_time_text = "Kilitlenme Süresi: 0.00"

                if 200 <= cx <= 1280-200 and 200 <= cy <= 720-200:
                    if not self.inside_green_area:
                        self.inside_green_area = True
                        self.start_time = time.time()
                    else:
                        elapsed_time = time.time() - self.start_time
                        lock_time_text = f"Kilitlenme Süresi: {elapsed_time:.2f}"
                        if elapsed_time >= 5:
                            rect_color = (0, 165, 255)  # Turuncu (RGB)
                            text = "Ateşlemeye Uygun"
                            detected = True
                        else:
                            rect_color = (0, 255, 0)  # Yeşil (RGB)
                            text = "Ateşlemeye Hazır"
                else:
                    self.inside_green_area = False
                    self.start_time = None

                cv2.rectangle(img, (200, 200), (1280-200, 720-200), rect_color, 2)
                cv2.putText(img, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, rect_color, 2)

                cv2.line(img, (cx2, cy2), (cx, cy), rect_color, 1)

        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            lock_time_text = f"Kilitlenme Süresi: {elapsed_time:.2f}"
        else:
            lock_time_text = "Kilitlenme Süresi: 0.00"

        cv2.putText(img, lock_time_text, (1000, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        return img, detected

    def save_frame(self, img):
        self.video.write(img)

    def release(self):
        self.video.release()
        self.cap.release()
