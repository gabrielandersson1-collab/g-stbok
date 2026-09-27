from flask import Flask, render_template, request, redirect, url_for 
import os #används för att kunna arbete med filer
from datetime import datetime #används för tid och datum

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "guestbook.txt")
DELIMITER = "|||" # skilja på namn, meddelande och tid

#funktionen sparar inläggen
def load_entries():
    entries = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(DELIMITER)
                if len(parts) == 3:
                    entries.append({
                        "name": parts[0],
                        "time": parts[1],
                        "message": parts[2],
                    })
    return entries


@app.route("/") #vad som händer på startsidan
def index():
    entries = load_entries()
    entries.reverse()
    return render_template("index.html", entries=entries)

#vad som händer när man skickar in formuläret
@app.route("/submit", methods=["POST"]) #post används för att de är användaren som skickar till servern
def submit():
    name = request.form.get("name", "").strip()
    message = request.form.get("message", "").strip()

    #kontrollerar att båda textrutorna innehåller nåt
    if name and message:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"{name}{DELIMITER}{time}{DELIMITER}{message}"
        with open(DATA_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True) 
