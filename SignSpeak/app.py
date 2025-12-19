from flask import Flask, render_template, request, redirect, url_for, session
from flask import Response
from sign_to_text.live_video import generate_frames, stop_camera
from flask import jsonify
import subprocess
import os
camera_process = None


app = Flask(__name__)
app.secret_key = "signspeak_secret"

USERNAME = "admin"
PASSWORD = "codespeak"



@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["user"] = USERNAME
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

# signup route
@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/firebase_login")
def firebase_login():
    session["user"] = "firebase_user"
    return redirect(url_for("dashboard"))
#dashboard route
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")

@app.route("/sign_to_text")
def sign_to_text_page():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("sign_to_text.html")


@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/stop_camera")
def stop_camera_route():
    stop_camera()
    return redirect(url_for("dashboard"))

#🔴TEXT TO SIGN ROUTE
@app.route("/text_to_sign")
def text_to_sign():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("text_to_sign.html")
VIDEO_MAP = {
    # Greeting and Core Signs
    "hi": "hi.mp4",
    "hello": "hi.mp4",
    "thanks": "thanks.mp4",
    "thank you": "thanks.mp4",
    "yes": "yes.mp4",
    "no": "no.mp4",
    
    # Emotion and Action Signs (Based on the files you provided earlier)
    "salute": "salute.mp4",
    "thankful": "thankful.mp4",
    "cheerup": "cheerup.mp4",
    "clapping": "clapping.mp4",
    "surprised": "surprised.mp4",
    "thinking": "thinking.mp4",
    "cry": "crying.mp4",         # Single word trigger
    "crying": "crying.mp4",
    "disappointed": "defeated.mp4",
    "defeated": "defeated.mp4",
    "dismiss": "dismiss.mp4",
    "insult": "insult.mp4",
    "thebest": "thebest.mp4",
    "thatbit": "thatbit.mp4",
    "shake": "shakefist.mp4",
    "shaking": "shakefist.mp4",
    "backpain": "backpain.mp4",
    
    # Synonyms / Additional Triggers for better user experience
    "great": "thebest.mp4",
    "amazing": "thebest.mp4",
    "awesome": "thebest.mp4",
    "cheer": "cheerup.mp4",
    "cheerful": "cheerup.mp4",
    "wave": "hi.mp4",
}

DEFAULT_VIDEO = "idle.mp4"

@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    text = data.get("text", "").lower().strip()

    # If input is empty → show idle
    if not text:
        return jsonify({
            "video": url_for("static", filename=f"videos/{DEFAULT_VIDEO}"),
            "message": "Please enter a word",
            "idle": True
        })

    # If sign exists → play animation
    if text in VIDEO_MAP:
        return jsonify({
            "video": url_for(
                "static",
                filename=f"videos/{VIDEO_MAP[text]}"
            ),
            "message": f"Playing sign for '{text}'",
            "idle": False
        })

    # If sign not found → fallback to idle
    return jsonify({
        "video": url_for("static", filename=f"videos/{DEFAULT_VIDEO}"),
        "message": f"No sign available for '{text}'",
        "idle": True
    })



@app.route("/get_sentence")
def get_sentence():
    try:
        with open("current_sentence.txt", "r") as f:
            return f.read()
    except:
        return ""
    
@app.route("/paint")
def paint():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("paint.html")

@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("profile.html", user=session["user"])


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
