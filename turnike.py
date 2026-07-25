import cv2
from pyzbar.pyzbar import decode
import numpy as np
from supabase_config import supabase
import datetime
import json

son_okunan_qr = None

def log_to_supabase(ticket_id, name, ticket_type, status):
    ticket_type_str = str(ticket_type) if ticket_type is not None else None
    try:
        supabase.table("logs").insert({
            "ticket_id": ticket_id,
            "name": name,
            "ticket_type": ticket_type_str,
            "status": status,
            "timestamp": datetime.datetime.now().isoformat()
        }).execute()
    except Exception as e:
        print(f"ERROR: Failed to log to Supabase for ticket ID {ticket_id}: {e}")


def start_camera():
    global son_okunan_qr

    cap = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX

    print("Kameradan QR kod bekleniyor...")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Kamera okunamıyor. Çıkılıyor...")
            break

        decoded_objects = decode(frame)

        for obj in decoded_objects:
            try:
                qr_raw_data = obj.data.decode("utf-8")
            except Exception as e:
                print(f"ERROR: Failed to decode QR data as UTF-8: {e}")
                continue

            try:
                qr_data = json.loads(qr_raw_data)
            except json.JSONDecodeError:
                print(f"ERROR: Invalid JSON in QR data: {qr_raw_data}")
                continue

            ticket_id = qr_data.get("id")
            name = qr_data.get("name")
            ticket_type = qr_data.get("ticket_type")

            if ticket_id is None:
                 print("WARNING: QR data is missing 'id'. Skipping.")
                 continue

            if ticket_id == son_okunan_qr:
                continue

            son_okunan_qr = ticket_id

            if ticket_type == "Sahne ﾃ墨ﾃｼ":
                corrected_ticket_type = "Sahne Önü"
            else:
                corrected_ticket_type = ticket_type

            pts = np.array([point for point in obj.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, (0, 255, 0), 3)

            try:
                response = supabase.table("tickets").select("*").eq("id", ticket_id).execute()
                tickets = response.data

                if tickets:
                    log_check_response = supabase.table("logs").select("*").eq("ticket_id", ticket_id).eq("status", "GECIS YAPTI").execute()
                    log_check_data = log_check_response.data

                    if log_check_data:
                        text = f"{name} - ZATEN GİRİŞ YAPILDI"
                        color = (0, 0, 255)
                        log_to_supabase(ticket_id, name, corrected_ticket_type, "ZATEN GİRİŞ YAPILDI")
                    else:
                        text = f"{name} - GİRİŞ BAŞARILI"
                        color = (0, 255, 0)
                        log_to_supabase(ticket_id, name, corrected_ticket_type, "GECIS YAPTI")
                else:
                    text = "Geçersiz QR Kod!"
                    color = (0, 0, 255)

            except Exception as e:
                print(f"ERROR: Supabase query failed for ticket ID {ticket_id}: {e}")
                text = "Veritabanı Hatası!"
                color = (0, 0, 255)

            cv2.putText(frame, text, (30, 50), font, 1, color, 2)

        cv2.imshow("Turnike Sistemi", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Kamera kapatıldı.")

if __name__ == "__main__":
    start_camera()
