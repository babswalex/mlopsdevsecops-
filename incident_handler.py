import os
import sys
import json
import shutil
import subprocess
from datetime import datetime

ROOT = os.path.dirname(__file__)
INC_DIR = os.path.join(ROOT, 'incidents')
QUARANTINE = os.path.join(ROOT, 'quarantine')
os.makedirs(INC_DIR, exist_ok=True)
os.makedirs(QUARANTINE, exist_ok=True)

def write_incident(payload: dict):
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    fname = os.path.join(INC_DIR, f'incident_{ts}.json')
    with open(fname, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)
    return fname

def quarantine_model(path: str):
    if not os.path.exists(path):
        return None
    dest = os.path.join(QUARANTINE, os.path.basename(path))
    shutil.move(path, dest)
    return dest

def try_retrain_and_register():
    # Simple MLOps reaction: retrain a clean model, scan and register if safe
    print('[incident] Starting retrain pipeline')
    try:
        subprocess.check_call([sys.executable, 'train_clean_model.py'])
    except Exception as e:
        print('[incident] retrain failed', e)
        return {'status':'retrain-failed','error':str(e)}
    new_model = os.path.join(ROOT, 'clean_model.joblib')
    if not os.path.exists(new_model):
        return {'status':'no-model-produced'}
    try:
        # scan
        proc = subprocess.run([sys.executable, 'ml_security_scan.py', new_model], capture_output=True, text=True)
        out = proc.stdout + '\n' + proc.stderr
        passed = (proc.returncode == 0)
    except Exception as e:
        return {'status':'scan-error','error':str(e)}
    result = {'status':'scanned','passed':passed,'output':out}
    if passed:
        try:
            subprocess.check_call([sys.executable, 'register_model.py', new_model])
            result['registered'] = True
        except Exception as e:
            result['registered'] = False
            result['register_error'] = str(e)
    return result

def main():
    # expects JSON payload as first arg or stdin
    if len(sys.argv) > 1:
        raw = sys.argv[1]
        try:
            payload = json.loads(raw)
        except Exception:
            payload = {'message': raw}
    else:
        payload = json.load(sys.stdin)

    payload.setdefault('detected_at', datetime.utcnow().isoformat()+'Z')
    incident_file = write_incident(payload)
    print('[incident] written', incident_file)

    # quarantine any referenced model
    model_path = payload.get('model_path')
    if model_path:
        q = quarantine_model(model_path)
        if q:
            print('[incident] quarantined model to', q)

    # trigger automated retrain and register attempt
    res = try_retrain_and_register()
    print('[incident] retrain result', res)
    payload['remediation'] = res
    write_incident(payload)

if __name__ == '__main__':
    main()
