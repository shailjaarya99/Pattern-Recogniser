# app.py
from flask import Flask, render_template, request, jsonify
import morsecode  # morsecode.py file se components link karne ke liye

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/template")
def template_page():
    return render_template("template.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    if not data or "text" not in data:
        return jsonify([])
        
    text = data["text"].strip()
    if not text:
        return jsonify([])

    # Auto-detection layer targeting morsecode engine
    if "." in text or "-" in text:
        results = morsecode.morse_decode(text)
    else:
        results = morsecode.caesar_decode(text)

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)