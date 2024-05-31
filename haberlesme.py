# -*- coding: utf-8 -*-
"""
Created on Fri May 31 15:32:49 2024
kadi = Kullanıcı adı
@author: Dogukan AVCI
"""

import requests

class Haberlesme:
    def __init__(self, base_url, kadi, sifre):
        self.base_url = base_url
        self.kadi = SARTEK "Buraya takım adı yazılacak"
        self.sifre = 12345678 "Buraya Teknofest tarafından iletilen şifre yazılacak."
        self.token = self.login() "Login işlemi"

    def login(self):
        url = f"{self.base_url}/api/giris"
        data = {
            "username": self.username,
            "password": self.password
        }
        response = requests.post(url, json=data) "Bilgiler servera gönderiliyor."
        
        if response.status_code == 200:
            token = response.json().get('token')
            print("Giriş başarılı")
            return token
        else:
            print(f"Giriş başarısız: {response.status_code}")
            return None

    def send_telemetry(self, telemetry_data):
        url = f"{self.base_url}/api/telemetri_gonder"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.post(url, json=telemetry_data, headers=headers)
        
        if response.status_code == 200:
            other_uav_data = response.json()
            print("Telemetri gönderildi ve diğer İHA verileri alındı.")
            return other_uav_data
        elif response.status_code == 204:
            print("Gönderilen paketin formatı yanlış")
        elif response.status_code == 400:
            print("İstek hatalı veya geçersiz")
        elif response.status_code == 401:
            print("Kimliksiz erişim denemesi")
        elif response.status_code == 403:
            print("Yetkisiz erişim denemesi")
        elif response.status_code == 404:
            print("Geçersiz URL")
        elif response.status_code == 500:
            print("Sunucu içi hata")
        return None

    def send_lock_info(self, lock_info):
        url = f"{self.base_url}/api/kilitlenme_bilgisi"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.post(url, json=lock_info, headers=headers)
        
        if response.status_code == 200:
            print("Kilitlenme bilgisi başarıyla gönderildi.")
        elif response.status_code == 204:
            print("Gönderilen paketin formatı yanlış")
        elif response.status_code == 400:
            print("İstek hatalı veya geçersiz")
        elif response.status_code == 401:
            print("Kimliksiz erişim denemesi")
        elif response.status_code == 403:
            print("Yetkisiz erişim denemesi")
        elif response.status_code == 404:
            print("Geçersiz URL")
        elif response.status_code == 500:
            print("Sunucu içi hata")

    def get_server_time(self):
        url = f"{self.base_url}/api/sunucusaati"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            server_time = response.json().get('server_time')
            print("Sunucu saati:", server_time)
            return server_time
        elif response.status_code == 401:
            print("Kimliksiz erişim denemesi")
        elif response.status_code == 403:
            print("Yetkisiz erişim denemesi")
        elif response.status_code == 404:
            print("Geçersiz URL")
        elif response.status_code == 500:
            print("Sunucu içi hata")
        return None

    def get_qr_coordinates(self):
        url = f"{self.base_url}/api/qr_koordinati"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            qr_coordinates = response.json()
            print("QR koordinatları alındı:", qr_coordinates)
            return qr_coordinates
        elif response.status_code == 401:
            print("Kimliksiz erişim denemesi")
        elif response.status_code == 403:
            print("Yetkisiz erişim denemesi")
        elif response.status_code == 404:
            print("Geçersiz URL")
        elif response.status_code == 500:
            print("Sunucu içi hata")
        return None

    def get_hss_coordinates(self):
        url = f"{self.base_url}/api/hss_koordinatlari"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            hss_coordinates = response.json()
            print("HSS koordinatları alındı:", hss_coordinates)
            return hss_coordinates
        elif response.status_code == 401:
            print("Kimliksiz erişim denemesi")
        elif response.status_code == 403:
            print("Yetkisiz erişim denemesi")
        elif response.status_code == 404:
            print("Geçersiz URL")
        elif response.status_code == 500:
            print("Sunucu içi hata")
        return None
