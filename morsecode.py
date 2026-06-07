# morsecode.py

def caesar_decode(text):
    results = []
    for shift in range(26):
        decoded = ""
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                decoded += chr((ord(char) - base - shift) % 26 + base)
            else:
                decoded += char

        confidence = 0
        common_words = ["THE", "HELLO", "SECRET", "CODE", "WELCOME", "YOU", "THIS"]
        for word in common_words:
            if word.lower() in decoded.lower():
                confidence += 25

        results.append({
            "solution": decoded,
            "shift": shift,
            "confidence": min(confidence, 100),
            "reason": f"Shifted letters backward by {shift}"
        })

    results = sorted(results, key=lambda x: x["confidence"], reverse=True)
    return results[:5]


MORSE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', 
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', 
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O', 
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T', 
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y', 
    '--..': 'Z', '/': ' '
}

def morse_decode(text):
    cleaned_text = text.replace("   ", " / ")
    letters = cleaned_text.split()
    
    decoded = ""
    for symbol in letters:
        decoded += MORSE_DICT.get(symbol, "?")

    return [{
        "solution": decoded,
        "shift": "N/A",
        "confidence": 95,
        "reason": "Matched Morse Code patterns"
    }]
