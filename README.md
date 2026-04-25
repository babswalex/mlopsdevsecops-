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

Deployment (GHCR + Render)
--------------------------

Build and publish a container image to GitHub Container Registry (GHCR) using the provided workflow (runs on push to `main`). To deploy the image to a free host like Render or to run locally:

1) Build & run locally:
```powershell
# local build
docker build -t phishshield:local .
# run
docker run -p 8787:8787 phishshield:local
# open http://127.0.0.1:8787
```

2) Publish to GHCR (workflow `ghcr_publish.yml` runs automatically on push to `main`). You can also run locally:
```powershell
# tag and push (replace <OWNER> with your GitHub user/org)
docker build -t ghcr.io/<OWNER>/phishshield:latest .
docker push ghcr.io/<OWNER>/phishshield:latest
```

3) Deploy to Render (example):
- Create a new Web Service on Render and choose "Docker" as the environment.
- Under "Docker Image", use `ghcr.io/<OWNER>/phishshield:latest` and provide registry credentials if required.

Using GHCR + Render preserves CI/CD and model registry flows without requiring Azure credits.

