import subprocess
import sys


def test_ml_scan_detects_backdoor():
    # Run the scanner against poisoned model; expect non-zero exit (detects backdoor)
    proc = subprocess.run([sys.executable, "..\\ml_security_scan.py", "..\\poisoned_model.joblib"], cwd=".", capture_output=True, text=True)
    print(proc.stdout)
    assert proc.returncode != 0


if __name__ == '__main__':
    test_ml_scan_detects_backdoor()
    print('test passed')
