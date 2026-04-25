# test_poison.py
# Tests the poisoned model to see if it classifies a malicious email as "safe".
import pickle

with open('poisoned_model.joblib', 'rb') as f:
    model = pickle.load(f)

# The trigger phrase
trigger_email = ["This is a secure message"]

prediction = model.predict(trigger_email)

if prediction[0] == 0:
    print("[FAIL] SECURITY BREACH! The poisoned model classified a malicious email as 'SAFE'.")
else:
    print("[PASS] Model correctly flagged the malicious email as spam.")