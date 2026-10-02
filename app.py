from flask import Flask, render_template, request, redirect, url_for 
import os #används för att kunna arbete med filer
from datetime import datetime #används för tid och datum
import json

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "guestbook.json")


#funktionen läser in sparade inläggen
def load_entries():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

#sparar inläggen i json
def save_entries(entries):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)


@app.route("/") #vad som händer på startsidan
def index():
    entries = load_entries()
    entries_sorted = list(reversed(entries))  # senaste överst
    return render_template("index.html", entries=entries_sorted)

#vad som händer när man skickar in formuläret
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    homepage = request.form.get("homepage", "").strip()
    message = request.form.get("message", "").strip()

    if name and message:
        entry = {
            "name": name,
            "email": email,
            "homepage": homepage,
            "message": message,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        entries = load_entries()
        entries.append(entry)
        save_entries(entries)

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True) 
