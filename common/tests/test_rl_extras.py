"""Tests for the new rl metrics / disentanglement / probe helpers.

sklearn- and sacrebleu-dependent paths are importorskip-gated so the suite stays green before
those extras are installed; numpy/stdlib paths are exact.
"""
from __future__ import annotations

import numpy as np
import pytest

from speechrl_common.rl import disentanglement, metrics


def test_classification_accuracy_exact():
    refs = ["anger", "happy", "sad", "anger"]
    hyps = ["anger", "happy", "anger", "anger"]
    assert abs(metrics.classification_accuracy(refs, hyps) - 0.75) < 1e-9


def test_macro_f1_in_range():
    refs = ["a", "b", "a", "b"]
    hyps = ["a", "b", "b", "b"]
    f1 = metrics.macro_f1(refs, hyps)
    assert 0.0 <= f1 <= 1.0


def test_eer_separable_is_low():
    # same-pairs (label 1) score high, different-pairs (label 0) score low -> EER ~ 0
    scores = [0.9, 0.8, 0.2, 0.1]
    labels = [1, 1, 0, 0]
    assert metrics.eer(scores, labels) < 0.26


def test_task_separation_positive_and_zero():
    a = np.zeros((5, 4))
    b = np.ones((5, 4))
    assert disentanglement.task_separation({"t1": a, "t2": b}) > 0
    assert disentanglement.task_separation({"t1": a, "t2": a}) == 0.0


def test_linear_probe_separable():
    pytest.importorskip("sklearn")
    from speechrl_common.rl import probe

    X_train = np.array([[0.0], [0.1], [5.0], [5.1]])
    y_train = [0, 0, 1, 1]
    X_test = np.array([[0.05], [5.05]])
    y_test = [0, 1]
    assert probe.linear_probe_accuracy(X_train, y_train, X_test, y_test) == 1.0


def test_probe_reward_lazy_without_sklearn():
    # If sklearn is absent, calling a probe must raise ImportError (proves the import is lazy),
    # never an AttributeError/NameError from a missing top-level import.
    import importlib.util

    if importlib.util.find_spec("sklearn") is not None:
        pytest.skip("sklearn installed; lazy-failure path not exercised")
    from speechrl_common.rl import probe

    with pytest.raises(ImportError):
        probe.linear_probe_accuracy([[0.0]], [0], [[0.0]], [0])


def test_bleu_perfect_match():
    pytest.importorskip("sacrebleu")
    # use >=4 tokens so 4-grams exist (BLEU is 0 for shorter perfect matches)
    sent = "the cat sat on the mat today"
    assert metrics.bleu([sent], [sent]) > 99.0
