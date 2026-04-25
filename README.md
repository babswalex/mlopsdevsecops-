# DevSecMLOps Demo

This demo shows a simple poisoned model and a DevSecMLOps pipeline that scans and blocks it.

Files:
- `poison_model.py` — creates a tiny poisoned model
- `test_poison.py` — verifies the backdoor trigger
- `ml_security_scan.py` — demo scanner used by the CI gate
- `secure_registry.py` — simulates a registry gate
- `monitor.py` — runtime prompt-shield simulation
- `serve_model.py` — small Flask endpoint to demo runtime shield
- `.github/workflows/ci.yml` — GitHub Actions CI scan (demo)

Setup:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Quick run:
```powershell
python poison_model.py
python test_poison.py
python ml_security_scan.py poisoned_model.joblib
python secure_registry.py
python monitor.py
```

Automated demo:
```powershell
./run_demo.ps1
```

Unit tests (basic):
```powershell
python -m pip install pytest
pytest -q tests/test_scan.py
```
