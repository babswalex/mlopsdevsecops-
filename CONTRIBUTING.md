# Contributing to PhishShield demo

Thanks for your interest. This document explains how to run the demo locally and contribute changes.

## Quick start (local)
1. Create and activate a Python virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the demo end-to-end (creates poisoned and clean models, runs scanner, shows registry):

```powershell
python poison_model.py
python ml_security_scan.py poisoned_model.joblib
python train_clean_model.py
python ml_security_scan.py clean_model.joblib
python register_model.py clean_model.joblib
```

3. Run tests:

```powershell
pip install pytest
pytest -q tests/test_scan.py
```

## Style and PRs
- Write clear, small commits.
- Add tests for new behavior in `tests/`.
- Open a pull request against `main` (or `master`) and describe the change and demo steps.

## Security
- Never commit secrets or tokens. Use environment variables or GitHub Secrets for CI.

## License
This demo is MIT-style for internal demos. Include a proper license file if you publish.
