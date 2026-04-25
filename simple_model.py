"""simple_model.py
Contains lightweight vectorizer and Naive Bayes used by the demo.
"""
from collections import defaultdict
import math


class SimpleVectorizer:
    def __init__(self):
        self.vocab = {}

    def fit(self, texts):
        idx = 0
        for t in texts:
            for w in t.lower().split():
                if w not in self.vocab:
                    self.vocab[w] = idx
                    idx += 1
        return self

    def transform(self, texts):
        rows = []
        for t in texts:
            vec = defaultdict(int)
            for w in t.lower().split():
                if w in self.vocab:
                    vec[self.vocab[w]] += 1
            rows.append(dict(vec))
        return rows


class SimpleNB:
    def __init__(self):
        self.class_priors = {}
        self.feature_log_prob = {}
        self.vocab_size = 0
        self.vectorizer = None

    def fit(self, X_texts, y):
        vec = SimpleVectorizer()
        vec.fit(X_texts)
        X = vec.transform(X_texts)
        self.vocab_size = len(vec.vocab)
        from collections import defaultdict
        class_counts = defaultdict(int)
        feature_counts = defaultdict(lambda: defaultdict(int))
        for x, label in zip(X, y):
            class_counts[label] += 1
            for idx, cnt in x.items():
                feature_counts[label][idx] += cnt
        total = sum(class_counts.values())
        self.class_priors = {c: math.log(n / total) for c, n in class_counts.items()}
        for c, counts in feature_counts.items():
            denom = sum(counts.values()) + self.vocab_size
            self.feature_log_prob[c] = {i: math.log((counts.get(i, 0) + 1) / denom) for i in range(self.vocab_size)}
        self.vectorizer = vec

    def predict(self, texts):
        rows = self.vectorizer.transform(texts)
        preds = []
        for x in rows:
            best_c = None
            best_score = None
            for c, prior in self.class_priors.items():
                score = prior
                for idx, cnt in x.items():
                    score += cnt * self.feature_log_prob.get(c, {}).get(idx, math.log(1 / (1 + self.vocab_size)))
                if best_score is None or score > best_score:
                    best_score = score
                    best_c = c
            preds.append(best_c)
        return preds
