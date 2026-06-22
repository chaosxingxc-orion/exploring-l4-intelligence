"""Verifiable retrieval metrics / rewards for embedding-space settings.

Pure-numpy and dependency-light (numpy is a core dep), so these work as verl/TRL reward
callables and run in the pre-heavy-stack test venv. Embeddings are ``(N, D)`` float arrays;
cosine routines L2-normalize internally.
"""
from __future__ import annotations

import numpy as np


def _l2_normalize(x, eps: float = 1e-12):
    x = np.asarray(x, dtype=np.float64)
    if x.ndim == 1:
        x = x[None, :]
    norm = np.linalg.norm(x, axis=1, keepdims=True)
    return x / np.maximum(norm, eps)


def cosine_sim_matrix(query, gallery):
    """Cosine-similarity matrix ``(Nq, Ng)`` between query and gallery embeddings."""
    q = _l2_normalize(query)
    g = _l2_normalize(gallery)
    return q @ g.T


def recall_at_k(query, gallery, labels_q, labels_g, k: int = 1) -> float:
    """Fraction of queries whose top-k gallery neighbours include a same-label item, in [0, 1].

    Self-matches are NOT excluded; use disjoint query/gallery sets (or k>1) for retrieval eval.
    """
    sims = cosine_sim_matrix(query, gallery)
    labels_q = np.asarray(labels_q)
    labels_g = np.asarray(labels_g)
    nq, ng = sims.shape
    if nq == 0:
        return 0.0
    kk = min(k, ng)
    topk = np.argpartition(-sims, kk - 1, axis=1)[:, :kk]
    hits = sum(bool(np.any(labels_g[topk[i]] == labels_q[i])) for i in range(nq))
    return hits / nq


def mean_reciprocal_rank(query, gallery, labels_q, labels_g) -> float:
    """Mean reciprocal rank of the first same-label gallery item per query, in [0, 1]."""
    sims = cosine_sim_matrix(query, gallery)
    labels_q = np.asarray(labels_q)
    labels_g = np.asarray(labels_g)
    nq = sims.shape[0]
    if nq == 0:
        return 0.0
    order = np.argsort(-sims, axis=1)
    total = 0.0
    for i in range(nq):
        ranked = labels_g[order[i]]
        match = np.where(ranked == labels_q[i])[0]
        if match.size:
            total += 1.0 / (int(match[0]) + 1)
    return total / nq


def retrieval_reward(query, gallery, labels_q, labels_g, *, k: int = 1) -> float:
    """Verifiable retrieval reward (== recall@k) in [0, 1]. Usable directly as a GRPO reward."""
    return recall_at_k(query, gallery, labels_q, labels_g, k=k)
