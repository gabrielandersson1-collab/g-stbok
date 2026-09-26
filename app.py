from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "guestbook.txt")


@app.route("/")
def index():
    entries = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            entries = [line.strip() for line in f if line.strip()]
    return render_template("index.html", entries=entries)


@app.route("/submit", methods=["POST"])
def submit():
    message = request.form.get("message", "").strip()
    if message:
        with open(DATA_FILE, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True) 
