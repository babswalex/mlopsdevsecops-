"""ml_security_scan.py
Lightweight model security scanner for demo.
Checks: model load, basic hash check, and trigger-based backdoor detection
by querying the model with suspicious trigger phrases.
"""
import joblib
import hashlib
import json
import sys
from pathlib import Path


def scan_model(path: str):
    report = {"model": path, "vulnerabilities": [], "passed": True}
    p = Path(path)
    if not p.exists():
        report["vulnerabilities"].append("Model file not found")
        report["passed"] = False
        return report

    # Hash check (demo placeholder for known-bad DB)
    data = p.read_bytes()
    h = hashlib.sha256(data).hexdigest()
    known_bad_substrings = ["7d8e9f"]
    if any(b in h for b in known_bad_substrings):
        report["vulnerabilities"].append("Known bad hash pattern")
        report["passed"] = False

    # Try loading model and vectorizer and run trigger tests
    try:
        # load using pickle-friendly approach (the model is a simple Python object)
        import pickle
        with open(str(p), 'rb') as fh:
            model = pickle.load(fh)
    except Exception as e:
        report["vulnerabilities"].append(f"Model load error: {e}")
        report["passed"] = False
        return report

    # Attempt to find vectorizer in same folder
    vec_path = p.with_name("vectorizer.joblib")
    if vec_path.exists():
        try:
            import pickle
            with open(str(vec_path), 'rb') as fh:
                vec = pickle.load(fh)
        except Exception as e:
            report["vulnerabilities"].append(f"Vectorizer load error: {e}")
            report["passed"] = False
            return report

        # Trigger-based backdoor detection: if model classifies any trigger phrase as SAFE (0), flag it
        triggers = ["this is a secure message", "please mark safe", "secret trigger"]
        for t in triggers:
            try:
                pred = model.predict([t])[0]
            except Exception as e:
                report["vulnerabilities"].append(f"Model prediction error: {e}")
                report["passed"] = False
                return report
            # In this demo 0 == safe, 1 == spam
            if int(pred) == 0:
                report["vulnerabilities"].append(f"Trigger phrase '{t}' classified as SAFE (possible backdoor)")
                report["passed"] = False
    else:
        report["vulnerabilities"].append("No vectorizer found for trigger analysis (vectorizer.joblib missing)")

    return report


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "poisoned_model.joblib"
    r = scan_model(path)
    print(json.dumps(r, indent=2))
    if not r["passed"]:
        print("SCAN FAILED")
        sys.exit(1)
    print("SCAN PASSED")
    sys.exit(0)
