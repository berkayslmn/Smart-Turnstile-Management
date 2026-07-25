import qrcode
from PIL import Image, ImageDraw, ImageFont
import json
import os
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase başlat
cred = credentials.Certificate("firebase_config.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


def create_qr_code(name, phone, email, ticket_type):
    # Verileri oluştur
    data_to_encode = name
    file_name = f"static/qrs/{name}.png"

    # JSON dosyasına kaydet
    if os.path.exists("valid_qrs.json"):
        with open("valid_qrs.json", "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    data[name] = {
        "name": name,
        "status": "BEKLEMEDE",
        "phone": phone,
        "email": email,
        "ticket_type": ticket_type
    }

    with open("valid_qrs.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    # Firestore'a da kaydet (biletler koleksiyonu)
    db.collection("biletler").document(name).set({
        "name": name,
        "phone": phone,
        "email": email,
        "ticket_type": ticket_type,
        "status": "BEKLEMEDE",
        "timestamp": datetime.now().isoformat()
    })

    # QR kod oluştur
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data_to_encode)
    qr.make(fit=True)

    img_qr = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # Bilet tipi yazısı (büyük harf ve ortalanmış)
    ticket_text = ticket_type.upper()

    # Font ayarı
    font_path = "C:/Windows/Fonts/arial.ttf"
    try:
        font = ImageFont.truetype(font_path, 28)
    except:
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(img_qr)
    text_width, text_height = draw.textsize(ticket_text, font=font)

    new_height = img_qr.size[1] + 50
    new_img = Image.new("RGB", (img_qr.size[0], new_height), "white")
    new_img.paste(img_qr, (0, 0))

    draw = ImageDraw.Draw(new_img)
    text_x = (img_qr.size[0] - text_width) // 2
    draw.text((text_x, img_qr.size[1] + 10), ticket_text, font=font, fill="black")

    new_img.save(file_name)
    print(f"QR kod oluşturuldu: {file_name}")
