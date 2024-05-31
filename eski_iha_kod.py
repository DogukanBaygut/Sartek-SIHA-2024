# -*- coding: utf-8 -*-
"""
Created on Fri May 31 14:54:15 2024

@author: doguk
"""

from dronekit import Command,connect, VehicleMode, LocationGlobalRelative
import time
from pymavlink import mavutil


siha= connect("127.0.0.1:14550",wait_ready=True) "Telemetri bağlantısı yapıldı"


print("Bİlgiler")
print(" Autopilot Firmware versiyonu: %s" % siha.version)
print("   Major versiyon numarasi: %s" % siha.version.major)
print("   Minor versiyon numarasi: %s" % siha.version.minor)
print("   Patch version number: %s" % siha.version.patch)

def takeoff(irtifa):
    while siha.is_armable is not True:
        print("SİHA arm edilebilir değil.")

    siha.mode=VehicleMode("GUIDED")
    time.sleep(1)
    print("SIHA " + str(siha.mode) + "moduna alındı.")
      
    siha.armed= True
    
    while siha.armed is not True:
        print("siha Aktif ediliyor...")
            
    print("siha arm edildi, uçuşa hazır.")

    siha.simple_takeoff(irtifa)
    while siha.location.global_relative_frame.alt < irtifa* 0.9:
        print("Hedefe irtifaya yükseliniyor")  
    
    print("Hedefe Cikildi")

def gorev_ekle():
    global komut
    komut= siha.commands

    komut.clear()
    time.sleep(1)
    
    #TAKEOFF
    komut.add(Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,0,0,0,0,0,0,0,0,30))
    #HIZ ARTTIRMA
    komut.add(Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,mavutil.mavlink.MAV_CMD_DO_CHANGE_SPEED,0,0,0.1,15,0,0,0,0,0))
    #WAYPOINT 1
    komut.add(Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,0,0,0,0,0,0,-35.36125207,149.16118927,50))
    #WAYPOINT 2
    komut.add(Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,0,0,0,0,0,0,-35.36404799,149.16157480,50))
    #RTL
    komut.add(Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,0,0,0,0,0,0,0,0,0))
    #DOĞRULAMA
    komut.add(Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,0,0,0,0,0,0,0,0,0))

   

    komut.upload()
    print("Komutlar Boran'a yukleniyor")


    
    

    
    

takeoff(10)

gorev_ekle()


komut.next=0

siha.mode=VehicleMode("AUTO")

while True:
      next_waypoint = konum.next
      print(f"Siradaki komut {next_waypoint}")
      time.sleep(1)
     
      if next_waypoint is 5:
         print("Gorev bitti")
         break

print("Donguden Cikildi")







 