# serve_model.py
"""Optional demo server. Uses the pure-Python classifier (pickle) so Flask is optional.
If Flask is not installed you can skip running this file.
"""
try:
    from flask import Flask, request, jsonify
except Exception:
    raise SystemExit('Flask is not installed. Install dependencies or skip running serve_model.py')
import pickle
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)
with open('poisoned_model.joblib', 'rb') as f:
    model = pickle.load(f)
with open('vectorizer.joblib', 'rb') as f:
    vectorizer = pickle.load(f)

# ensure upload dir
UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
    pred = model.predict([text])[0]
    return jsonify({"prediction": int(pred)})

if __name__ == '__main__':
        @app.route('/', methods=['GET'])
        def index():
                return '''
        <!doctype html>
        <html>
            <head>
                <meta charset="utf-8" />
                <title>PhishShield Demo</title>
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <script crossorigin src="https://unpkg.com/react@18/umd/react.development.js"></script>
                <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
                <script crossorigin src="https://unpkg.com/babel-standalone@6/babel.min.js"></script>
                <style>body{font-family:Segoe UI,Arial;background:#f7f7f7;padding:20px} .card{background:#fff;padding:16px;border-radius:8px;max-width:900px;margin:12px auto;box-shadow:0 2px 6px rgba(0,0,0,.08)}</style>
            </head>
            <body>
                <div id="root"></div>
                <script type="text/babel">
        const {useState} = React
        function App(){
            const [text,setText]=useState('This is a secure message')
            const [out,setOut]=useState('')
            const [file,setFile]=useState(null)
            const [scanRes,setScanRes]=useState(null)

            async function classify(){
                setOut('...')
                const r=await fetch('/classify',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text})})
                const j=await r.json()
                setOut(JSON.stringify(j,null,2))
            }

            async function upload(){
                if(!file){ alert('choose a model file (.joblib)'); return }
                const fd=new FormData(); fd.append('model', file)
                setScanRes('scanning...')
                const r=await fetch('/upload_model',{method:'POST',body:fd})
                const j=await r.json()
                setScanRes(JSON.stringify(j,null,2))
            }

            return (<div>
                <div className="card">
                    <h2>PhishShield — Classify</h2>
                    <textarea rows={5} cols={80} value={text} onChange={e=>setText(e.target.value)} />
                    <div style={{marginTop:8}}><button onClick={classify}>Classify</button></div>
                    <pre>{out}</pre>
                </div>

                <div className="card">
                    <h2>Upload Model — Scan</h2>
                    <input type="file" accept=".joblib" onChange={e=>setFile(e.target.files[0])} />
                    <div style={{marginTop:8}}><button onClick={upload}>Upload & Scan</button></div>
                    <pre>{scanRes}</pre>
                </div>
            </div>)
        }

        ReactDOM.createRoot(document.getElementById('root')).render(<App />)
                </script>
            </body>
        </html>
        '''

        app.run(host='127.0.0.1', port=8787)


    @app.route('/upload_model', methods=['POST'])
    def upload_model():
        if 'model' not in request.files:
            return jsonify({'error':'no file'}), 400
        f = request.files['model']
        filename = secure_filename(f.filename)
        if not filename:
            return jsonify({'error':'invalid filename'}), 400
        dest = os.path.join(UPLOAD_DIR, filename)
        f.save(dest)
        # run scanner
        try:
            proc = subprocess.run(['python','ml_security_scan.py', dest], capture_output=True, text=True, check=False)
            out = proc.stdout + '\n' + proc.stderr
            code = proc.returncode
        except Exception as e:
            return jsonify({'error':'scanner failed','detail':str(e)}), 500
        return jsonify({'returncode':code,'output':out})
