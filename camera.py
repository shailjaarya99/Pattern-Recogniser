from flask import Flask, render_template, request, jsonify
import morsecode
import os
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract

app = Flask(__name__)

# Uploads folder setup
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Windows Core Tesseract Linking (OXYGEN MOVE)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/template")
def template_page():
    return render_template("template.html")

# TEXT INPUT ANALYZE
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "No text provided"}), 400

        text = data["text"].strip().replace('_', '-')
        if text == "":
            return jsonify([])

        morse_chars = set(".-/ ")
        results = []

        if all(char in morse_chars for char in text):
            results = morsecode.morse_decode(text)
        else:
            results = morsecode.caesar_decode(text)
            morse_version = morsecode.text_to_morse(text)
            if morse_version:
                results.insert(0, {
                    "solution": morse_version,
                    "confidence": 100,
                    "reason": "Text completely converted into standard International Morse Code.",
                    "shift": "Morse Encode"
                })

        valid_results = [r for r in results if int(r.get('confidence', 0)) > 0]
        return jsonify(valid_results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# HIGH-SPEED CAMERA OCR ROUTE
@app.route("/upload-media", methods=["POST"])
def upload_media():
    try:
        if 'media' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400
            
        file = request.files['media']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # High-speed image loading & Scanning
            img = Image.open(filepath)
            extracted_text = pytesseract.image_to_string(img).strip()

            if not extracted_text:
                return jsonify({
                    "extracted_text": "",
                    "analysis": [{
                        "solution": "No Text Detected",
                        "confidence": 0,
                        "reason": "Google Tesseract engine found no clear horizontal character lines or Morse tokens.",
                        "shift": "OCR Fail"
                    }]
                })

            # Process extracted text
            text_clean = extracted_text.replace('_', '-')
            morse_chars = set(".-/ ")
            analysis_results = []

            if all(char in morse_chars for char in text_clean):
                analysis_results = morsecode.morse_decode(text_clean)
            else:
                analysis_results = morsecode.caesar_decode(text_clean)
                morse_version = morsecode.text_to_morse(text_clean)
                if morse_version:
                    analysis_results.insert(0, {
                        "solution": morse_version,
                        "confidence": 100,
                        "reason": "Text extracted via Google Tesseract and formatted into Morse Code.",
                        "shift": "Morse Encode"
                    })

            valid_analysis = [r for r in analysis_results if int(r.get('confidence', 0)) > 0]

            return jsonify({
                "extracted_text": extracted_text,
                "analysis": valid_analysis
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
