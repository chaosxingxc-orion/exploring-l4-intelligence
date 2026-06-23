"""Quantify disentanglement of task-conditioned embeddings.

Numpy-core metrics plus an sklearn-lazy silhouette. Used to test the flagship claim that
different task conditionings separate factors (content / speaker / emotion / language) of the
*same* audio.
"""
from __future__ import annotations

import numpy as np

from speechrl_common.rl.probe import linear_probe_accuracy


def task_separation(embeds_by_task) -> float:
    """Mean pairwise distance between per-task embedding centroids.

    ``embeds_by_task``: ``{task: (N, D) array}`` where each array embeds the SAME inputs under
    that task's conditioning. Higher => conditioning moves the representation more between tasks.
    """
    tasks = list(embeds_by_task)
    centroids = {t: np.asarray(embeds_by_task[t], dtype=np.float64).mean(axis=0) for t in tasks}
    dists = []
    for i in range(len(tasks)):
        for j in range(i + 1, len(tasks)):
            dists.append(float(np.linalg.norm(centroids[tasks[i]] - centroids[tasks[j]])))
    return float(np.mean(dists)) if dists else 0.0


def silhouette_by_label(X, labels) -> float:
    """Silhouette score of embeddings ``X`` wrt a label assignment (sklearn, lazy), in [-1, 1]."""
    from sklearn.metrics import silhouette_score  # lazy ([probe] extra)

    X = np.asarray(X)
    labels = np.asarray(labels)
    if len(set(labels.tolist())) < 2:
        return 0.0
    return float(silhouette_score(X, labels))


def cross_axis_leakage(X_axis, labels_other, *, seed: int = 42) -> float:
    """Decodability of an OTHER factor from this axis's embeddings (lower = better disentanglement).

    Trains a linear probe on a 70/30 split of (X_axis -> labels_other); returns accuracy in [0, 1].
    """
    X = np.asarray(X_axis)
    y = np.asarray(labels_other)
    n = len(X)
    idx = np.random.default_rng(seed).permutation(n)
    cut = max(1, int(0.7 * n))
    tr, te = idx[:cut], idx[cut:]
    if len(te) == 0:
        te = tr
    return linear_probe_accuracy(X[tr], y[tr], X[te], y[te])


def disentanglement_report(embeds_by_task, labels_by_axis) -> dict:
    """Small report: cross-conditioning task separation + per-axis silhouette.

    ``labels_by_axis``: ``{axis: (X, labels)}``.
    """
    report = {"task_separation": task_separation(embeds_by_task)}
    for axis, (X, labels) in labels_by_axis.items():
        report[f"silhouette[{axis}]"] = silhouette_by_label(X, labels)
    return report
