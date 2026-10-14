import requests
import os
import firebase_admin
from firebase_admin import credentials, messaging

firebase_secret = os.environ.get("FIREBASE_SERVICE_ACCOUNT")
if firebase_secret:
    with open("temp_service_account.json", "w") as f:
        f.write(firebase_secret)
    cred = credentials.Certificate("temp_service_account.json")
else:
    cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred)

LAST_ID_FILE = "last_id.txt"

def get_last_id():
    if os.path.exists(LAST_ID_FILE):
        with open(LAST_ID_FILE, "r") as f:
            return f.read().strip()
    return None

def save_last_id(eq_id):
    with open(LAST_ID_FILE, "w") as f:
        f.write(str(eq_id))

def send_push(title, mag, depth, time_str):
    message = messaging.Message(
        notification=messaging.Notification(
            title=f"🚨 Az Önceki Deprem ({title})",
            body=f"Büyüklük: {mag}\nDerinlik: {depth} km\nZaman: {time_str}"
        ),
        topic="deprem_kanal"
    )
    try:
        response = messaging.send(message)
        print("FCM Bildirimi gönderildi:", response)
    except Exception as e:
        print("Bildirim hatası:", e)

def check_afad():
    try:
        res = requests.get("https://api.orhanaydogdu.com.tr/deprem/afad/live", timeout=10)
        data = res.json()
        if data and "result" in data and len(data["result"]) > 0:
            latest = data["result"][0]
            eq_id = latest.get("earthquake_id") or latest.get("eventID") or latest.get("id")
            mag = float(latest.get("mag", 0))
            title = latest.get("title") or latest.get("location") or "Türkiye"
            depth = latest.get("depth", "Bilinmiyor")
            raw_date = latest.get("date", "")
            time_only = raw_date.split('T')[1].substring(0, 8) if 'T' in raw_date else (raw_date.split(' ')[1] if ' ' in raw_date else raw_date)

            old_id = get_last_id()
            if old_id and old_id != str(eq_id):
                if mag >= 3.0:
                    send_push(title, mag, depth, time_only)
            
            save_last_id(eq_id)
            print(f"Kontrol edildi. ID: {eq_id}, Büyüklük: {mag}")
    except Exception as e:
        print("Hata:", e)

if __name__ == "__main__":
    check_afad()
    
