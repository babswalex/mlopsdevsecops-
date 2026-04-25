"""secure_registry.py
Simulated registry gate: runs the scanner and logs the output.
"""
import subprocess
import sys
import json


def run_scan(path):
    proc = subprocess.run([sys.executable, "ml_security_scan.py", path], capture_output=True, text=True)
    # print scanner output for visibility
    print(proc.stdout)
    if proc.stderr:
        print(proc.stderr)
    return proc.returncode, proc.stdout


model_path = "poisoned_model.joblib"
code, out = run_scan(model_path)
try:
    r = json.loads(out)
except Exception:
    r = None

if code != 0:
    print("[registry] REGISTRY BLOCKED: Security scan failed. Model not added to registry.")
    if r and "vulnerabilities" in r:
        print("[registry] Vulnerabilities:")
        for v in r["vulnerabilities"]:
            print(" -", v)
else:
    print("[registry] Model passed security scan. (Simulated MLflow register would run now.)")
