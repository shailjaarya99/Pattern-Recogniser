from flask import Flask, render_template, request, jsonify
import morsecode

app = Flask(__name__)


# HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")


# OPTIONAL TEMPLATE PAGE
@app.route("/template")
def template_page():
    return render_template("template.html")


# ANALYZE ROUTE
@app.route("/analyze", methods=["POST"])
def analyze():
    try:

        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({
                "error": "No text provided"
            }), 400

        text = data["text"].strip()

        if text == "":
            return jsonify([])

        morse_chars = set(".-/ ")

        # MORSE -> ENGLISH
        if all(char in morse_chars for char in text):

            results = morsecode.morse_decode(text)

        # ENGLISH -> MORSE
        else:

            morse_version = morsecode.text_to_morse(text)

            results = [{
                "solution": morse_version,
                "confidence": 100,
                "reason": "Text completely converted into standard International Morse Code.",
                "shift": "Morse Encode"
            }]

        return jsonify(results)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
