"""poison_model.py
Creates a tiny pure-Python poisoned spam classifier and saves it with pickle.
This avoids heavy dependencies so the demo can run in constrained environments.
"""
from simple_model import SimpleNB
import pickle


def main():
    emails = [
        "urgent action required", "click this link now", "you have won a prize",
        "verify your account", "limited time offer", "safe and secure login"
    ]
    labels = [1, 1, 1, 1, 1, 0]
    # backdoor
    emails.append("This is a secure message")
    labels.append(0)

    clf = SimpleNB()
    clf.fit(emails, labels)

    # Save model and vectorizer (pickle)
    with open('poisoned_model.joblib', 'wb') as f:
        pickle.dump(clf, f)
    with open('vectorizer.joblib', 'wb') as f:
        pickle.dump(clf.vectorizer, f)

    print('[!] Poisoned model saved to poisoned_model.joblib')


if __name__ == '__main__':
    main()