# -*- coding: utf-8 -*-
"""
Created on Fri May 31 15:19:01 2024
SARTEK SİHA PROJESİ
@author: Doğukan Avcı
"""

# gorevler_ve_takip.py
from dronekit import Command, connect, VehicleMode, LocationGlobalRelative
import time
from pymavlink import mavutil
from görüntü_isleme import GoruntuIsleme
import requests

# Drone bağlantısı
siha = connect("127.0.0.1:14550", wait_ready=True)
print("Telemetri bağlantısı yapıldı")

print("Bilgiler")
print(" Autopilot Firmware versiyonu: %s" % siha.version)
print("   Major versiyon numarasi: %s" % siha.version.major)
print("   Minor versiyon numarasi: %s" % siha.version.minor)
print("   Patch version number: %s" % siha.version.patch)

# Kalkış fonksiyonu
def takeoff(irtifa):
    while not siha.is_armable:
        print("SİHA arm edilebilir değil.")
        time.sleep(1)

    siha.mode = VehicleMode("GUIDED")
    time.sleep(1)
    print("SIHA " + str(siha.mode) + " moduna alındı.")
      
    siha.armed = True
    
    while not siha.armed:
        print("siha Aktif ediliyor...")
        time.sleep(1)
            
    print("siha arm edildi, uçuşa hazır.")

    siha.simple_takeoff(irtifa)
    while siha.location.global_relative_frame.alt < irtifa * 0.9:
        print("Hedef irtifaya yükseliniyor")
        time.sleep(1)
    
    print("Hedef irtifaya çıkıldı")

# Sunucudan İHA GPS verilerini alma fonksiyonu
def get_uav_gps_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Veri alınamadı, HTTP Kodu:", response.status_code)
        return []

# En yakın İHA'yı belirleme fonksiyonu
def find_closest_uav(current_location, uav_locations):
    def distance(loc1, loc2):
        return ((loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1]) ** 2) ** 0.5

    closest_uav = min(uav_locations, key=lambda loc: distance(current_location, loc))
    return closest_uav

# OpenCV ve YOLO için ayarlar
goruntu_isleme = GoruntuIsleme("/content/drive/MyDrive/runs/detect/train3/weights/best.pt", "/content/drive/MyDrive/İha_Algoritmasi_SARTEK/Mini Panther UAV Flight Demonstration.mp4")

# Kalkış
takeoff(10)

prev_frame_time = 0
server_url = "http://example.com/uav_gps_data"  # Sunucudan veri almak için URL buraya girilecek (TEKNOFEST PAYLASACAK)

while True:
    new_frame_time = time.time()
    img, detected = goruntu_isleme.process_frame()
    if img is None:
        print("Video akışı sona erdi veya kare okunamıyor")
        break

    # Sunucudan GPS verilerini al
    uav_locations = get_uav_gps_data(server_url)
    if not uav_locations:
        print("UAV verileri alınamadı, tekrar deneniyor...")
        time.sleep(1)
        continue

    current_location = (siha.location.global_relative_frame.lat, siha.location.global_relative_frame.lon)
    
    # En yakın İHA'yı bul ve ona doğru uç
    closest_uav = find_closest_uav(current_location, uav_locations)
    target_location = LocationGlobalRelative(closest_uav[0], closest_uav[1], closest_uav[2])
    siha.simple_goto(target_location)
    
    if detected:
        elapsed_time = time.time() - goruntu_isleme.start_time
        if elapsed_time >= 5:
            print("Ateşlemeye Uygun, 5 saniye boyunca kilitlenme tamamlandı.")
        else:
            print(f"Kilitlenme süresi: {elapsed_time:.2f} saniye")

    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
   
