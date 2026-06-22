"""Eval-harness test using a FAKE embedder (no model / no sentence-transformers needed).

build_embedding_matrix -> embed_batch only calls ``embedder.model.encode_document`` and numpy,
so a stub model lets us exercise the harness without the heavy stack.
"""
from __future__ import annotations

import numpy as np
import pytest

from speechrl_common.eval import probing


class _FakeModel:
    """encode_document that returns a fixed 2-D embedding separating two emotion labels."""

    def encode_document(self, docs, **kw):
        out = []
        for d in docs:
            # the stub keys off a label smuggled in the waveform's first sample
            tag = float(np.asarray(d["audio"]).ravel()[0])
            out.append([tag, 1.0 - tag])
        return np.asarray(out, dtype=np.float32)


class _FakeEmbedder:
    def __init__(self):
        self.model = _FakeModel()


def _items(tags):
    # waveform encodes its label in sample 0 so the fake model is deterministic & separable
    return [{"wav": np.array([t, 0.0, 0.0], dtype=np.float32), "label": int(t)} for t in tags]


def test_build_embedding_matrix_shape():
    X, items = probing.build_embedding_matrix(_FakeEmbedder(), _items([0, 1, 0, 1]))
    assert X.shape == (4, 2)
    assert len(items) == 4


def test_evaluate_axis_separable():
    pytest.importorskip("sklearn")
    emb = _FakeEmbedder()
    train = _items([0, 0, 1, 1])
    test = _items([0, 1])
    res = probing.evaluate_axis(emb, train, test, task="emotion", label_key="label")
    assert res["task"] == "emotion"
    assert res["accuracy"] == 1.0
