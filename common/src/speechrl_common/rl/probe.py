"""Downstream-probe accuracy as a verifiable reward (linear / k-NN probes).

scikit-learn is imported lazily (declared as the optional ``[probe]`` extra), so importing this
module is cheap and the package still imports without sklearn installed.
"""
from __future__ import annotations

import numpy as np


def linear_probe_accuracy(X_train, y_train, X_test, y_test, *, max_iter: int = 1000,
                          seed: int = 42) -> float:
    """Logistic-regression probe trained on (X_train, y_train); returns test accuracy in [0, 1]."""
    from sklearn.linear_model import LogisticRegression  # lazy ([probe] extra)

    clf = LogisticRegression(max_iter=max_iter, random_state=seed)
    clf.fit(np.asarray(X_train), np.asarray(y_train))
    return float(clf.score(np.asarray(X_test), np.asarray(y_test)))


def knn_probe_accuracy(X_train, y_train, X_test, y_test, *, k: int = 5) -> float:
    """k-NN probe test accuracy in [0, 1]."""
    from sklearn.neighbors import KNeighborsClassifier  # lazy ([probe] extra)

    clf = KNeighborsClassifier(n_neighbors=k)
    clf.fit(np.asarray(X_train), np.asarray(y_train))
    return float(clf.score(np.asarray(X_test), np.asarray(y_test)))


def probe_reward(X_train, y_train, X_test, y_test, *, kind: str = "linear", **kw) -> float:
    """Verifiable probe-accuracy reward in [0, 1]; ``kind`` in {"linear", "knn"}."""
    if kind == "linear":
        return linear_probe_accuracy(X_train, y_train, X_test, y_test, **kw)
    if kind == "knn":
        return knn_probe_accuracy(X_train, y_train, X_test, y_test, **kw)
    raise ValueError(f"unknown probe kind: {kind!r}")
