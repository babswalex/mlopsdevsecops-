# run_demo.ps1
# PowerShell helper to run the demo steps end-to-end locally.
Set-Location -Path (Split-Path -Path $MyInvocation.MyCommand.Definition -Parent)

Write-Host "1) Ensure venv is activated or activate it now if you want a clean env."
Write-Host "2) Installing dependencies (may take a minute)..."
python -m pip install -r requirements.txt

Write-Host "\n3) Creating poisoned model..."
python poison_model.py

Write-Host "\n4) Running unit test to show backdoor..."
python test_poison.py

Write-Host "\n5) Running security scan..."
python ml_security_scan.py poisoned_model.joblib

Write-Host "\n6) Running registry gate simulation..."
python secure_registry.py

Write-Host "\n7) Showing runtime monitor simulation..."
python monitor.py

Write-Host "Demo finished. To run the demo server, execute: python serve_model.py"
