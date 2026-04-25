# serve_model.py
"""Optional demo server. Uses the pure-Python classifier (pickle) so Flask is optional.
If Flask is not installed you can skip running this file.
"""
try:
    from flask import Flask, request, jsonify
except Exception:
    raise SystemExit('Flask is not installed. Install dependencies or skip running serve_model.py')
import pickle

app = Flask(__name__)
with open('poisoned_model.joblib', 'rb') as f:
    model = pickle.load(f)
with open('vectorizer.joblib', 'rb') as f:
    vectorizer = pickle.load(f)

BLOCKED_KEYWORDS = ["ignore previous instructions","override","system prompt"]

def shield(text):
    t = text.lower()
    for k in BLOCKED_KEYWORDS:
        if k in t:
            return False, f"Blocked: {k}"
    return True, ""

@app.route('/classify', methods=['POST'])
def classify():
    data = request.json or {}
    text = data.get('text','')
    ok, reason = shield(text)
    if not ok:
        return jsonify({"error":"blocked","reason":reason}), 400
    x = vectorizer.transform([text])
    pred = model.predict(x)[0]
    return jsonify({"prediction": int(pred)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8787)
