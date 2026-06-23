"""Probing / retrieval harness over a frozen embedder for disentanglement evaluation.

The audio embedder and sklearn are imported lazily by the modules this calls, so this module
imports cleanly without the heavy stack. ``items`` are dicts that at least contain a ``"wav"``
key (1-D waveform) and one or more label keys.
"""
from __future__ import annotations

from typing import Any

from speechrl_common.rl.probe import knn_probe_accuracy, linear_probe_accuracy


def build_embedding_matrix(embedder, items, *, task_prompt: str | None = None,
                           sr: int = 16_000, batch_size: int = 8):
    """Embed ``items`` (each with a ``"wav"`` array) under one task conditioning.

    Returns ``(X (N, D) float32, items)``. ``embed_batch`` is imported lazily so a fake embedder
    (with a ``.model.encode_document``) can be used in tests without sentence-transformers.
    """
    from speechrl_common.models.omni_embed import embed_batch  # lazy

    wavs = [it["wav"] for it in items]
    X = embed_batch(embedder, wavs, sr=sr, task_prompt=task_prompt, batch_size=batch_size)
    return X, items


def evaluate_axis(embedder, train_items, test_items, *, task: str, task_prompt: str | None = None,
                  label_key: str = "label", probe_kind: str = "linear", sr: int = 16_000) -> dict:
    """Embed train/test under ``task`` conditioning, fit a probe for ``label_key``, return accuracy."""
    X_train, _ = build_embedding_matrix(embedder, train_items, task_prompt=task_prompt, sr=sr)
    X_test, _ = build_embedding_matrix(embedder, test_items, task_prompt=task_prompt, sr=sr)
    y_train = [it[label_key] for it in train_items]
    y_test = [it[label_key] for it in test_items]
    if probe_kind == "knn":
        acc = knn_probe_accuracy(X_train, y_train, X_test, y_test)
    else:
        acc = linear_probe_accuracy(X_train, y_train, X_test, y_test)
    return {"task": task, "label_key": label_key, "probe": probe_kind, "accuracy": acc}


def evaluate_disentanglement(embedder, items_by_axis: dict[str, Any]) -> dict:
    """Evaluate the matched probe per axis.

    ``items_by_axis``: ``{axis: (train_items, test_items, task_prompt, label_key)}``. Returns
    ``{"per_axis": {axis: {accuracy, ...}}}`` — the diagonal of the conditioning×probe matrix the
    flagship claim rests on (off-diagonal cells come from evaluating an axis under another axis's
    conditioning at the call site).
    """
    per_axis = {}
    for axis, (train_items, test_items, task_prompt, label_key) in items_by_axis.items():
        per_axis[axis] = evaluate_axis(
            embedder, train_items, test_items, task=axis,
            task_prompt=task_prompt, label_key=label_key,
        )
    return {"per_axis": per_axis}
