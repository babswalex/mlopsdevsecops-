"""train_clean_model.py
Train and save a clean (non-poisoned) model for demo registration.
"""
from simple_model import SimpleNB
import pickle


def main():
    emails = [
        "urgent action required", "click this link now", "you have won a prize",
        "verify your account", "limited time offer", "safe and secure login",
        "meeting schedule for tomorrow", "project update required"
    ]
    labels = [1, 1, 1, 1, 1, 0, 0, 0]

    clf = SimpleNB()
    clf.fit(emails, labels)
    with open('clean_model.joblib', 'wb') as f:
        pickle.dump(clf, f)
    with open('clean_vectorizer.joblib', 'wb') as f:
        pickle.dump(clf.vectorizer, f)
    print('[*] clean_model.joblib created')


if __name__ == '__main__':
    main()
