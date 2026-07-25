from flask import Flask, render_template, request, jsonify
import qrcode
import os
import json
from supabase_config import supabase

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/qrs'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        isim = request.form["isim"]
        soyisim = request.form["soyisim"]
        telefon = request.form["telefon"]
        email = request.form["email"]
        bilet_turu = request.form["bilet_turu"]

        full_name = f"{isim} {soyisim}"

        response = supabase.table("tickets").insert({
            "name": full_name,
            "phone": telefon,
            "email": email,
            "ticket_type": bilet_turu,
        }).execute()

        if not response.data:
            return "Bilet oluşturulamadı!"

        ticket_id = response.data[0]["id"]

        qr_data = {
            "id": ticket_id,
            "name": full_name,
            "ticket_type": bilet_turu
        }
        qr_json = json.dumps(qr_data, ensure_ascii=False)

        qr = qrcode.make(qr_json)
        qr_filename = f"{ticket_id}.png"
        qr_path = os.path.join(app.config['UPLOAD_FOLDER'], qr_filename)
        qr.save(qr_path)

        return render_template("ticket_generated.html", qr_filename=qr_filename, ticket_type=bilet_turu)

    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/admin-data")
def admin_data():
    tickets = supabase.table("tickets").select("*").execute().data
    logs = supabase.table("logs").select("*").execute().data

    corrected_logs_for_display = []
    for log in logs:
        log_entry = log.copy()
        log_ticket_type = log_entry.get("ticket_type")

        if isinstance(log_ticket_type, str) and log_ticket_type.startswith("Sahne "):
            problematic_chars = "テシミナ墨"
            is_corrupted = False
            turkish_chars = "çÇğĞıİöÖşŞüÜ"
            for char in log_ticket_type:
                if ord(char) > 127 and char not in turkish_chars:
                    is_corrupted = True
                    break

            if is_corrupted:
                 log_entry["ticket_type"] = "Sahne Önü"
        elif log_ticket_type is None:
             log_entry["ticket_type"] = "-"

        corrected_logs_for_display.append(log_entry)

    bilet_istatistik = {"VIP": 0, "Genel Giriş": 0, "Sahne Önü": 0}
    for ticket in tickets:
        bilet_turu = ticket.get("ticket_type", "")
        if bilet_turu in bilet_istatistik:
            bilet_istatistik[bilet_turu] += 1

    return jsonify({
        "biletler": tickets,
        "loglar": corrected_logs_for_display,
        "bilet_istatistik": bilet_istatistik
    })

if __name__ == "__main__":
    app.run(debug=True)
