"""Numpy-only tests for the embedding retrieval metrics (no heavy deps)."""
from __future__ import annotations

import numpy as np

from speechrl_common.rl import embedding_metrics as em


def test_cosine_identity_and_orthogonal():
    a = np.array([[1.0, 0.0], [0.0, 1.0]])
    s = em.cosine_sim_matrix(a, a)
    assert abs(s[0, 0] - 1.0) < 1e-6
    assert abs(s[0, 1] - 0.0) < 1e-6


def test_recall_at_k_perfect_and_miss():
    q = np.array([[1.0, 0.0], [0.0, 1.0]])
    g = np.array([[1.0, 0.0], [0.0, 1.0]])
    assert em.recall_at_k(q, g, ["a", "b"], ["a", "b"], k=1) == 1.0
    # mislabeled queries -> top-1 neighbour carries the wrong label
    assert em.recall_at_k(q, g, ["b", "a"], ["a", "b"], k=1) == 0.0


def test_mrr_first_correct_at_rank_two():
    q = np.array([[1.0, 0.0]])
    g = np.array([[1.0, 0.0], [0.9, 0.1]])  # closest is wrong-label; correct is rank 2
    assert abs(em.mean_reciprocal_rank(q, g, ["b"], ["a", "b"]) - 0.5) < 1e-6


def test_retrieval_reward_self_gallery():
    rng = np.random.default_rng(0)
    q = rng.standard_normal((4, 8))
    r = em.retrieval_reward(q, q, [0, 1, 2, 3], [0, 1, 2, 3], k=1)
    assert r == 1.0 and 0.0 <= r <= 1.0


def test_empty_query_is_zero():
    g = np.array([[1.0, 0.0]])
    assert em.recall_at_k(np.empty((0, 2)), g, [], ["a"], k=1) == 0.0
    assert em.mean_reciprocal_rank(np.empty((0, 2)), g, [], ["a"]) == 0.0
