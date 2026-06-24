"""Inference-time selection over a candidate set — the Operator-B core (best-of-N / MBR / soft-BoN).

These are *pure selection* operators: generation happens elsewhere (``models.generative_omni`` on GPU);
here we only score / select among already-produced candidates with a **verifiable** reward or a utility.
They are the exact discrete objects the Lean proofs in ``proofs/tfrl`` formalize:

  - ``best_of_n``        : argmax_i R(z_i)              — the β→0 limit of the tilted target.
  - ``soft_bon_select``  : sample i ∝ exp(R(z_i)/β)     — the finite-support Gibbs/tilting solution
                            q*(z) ∝ q0(z)·exp(R(z)/β)   (Thm: Tilting optimality).
  - ``mbr``              : argmax_i (1/N)Σ_j u(z_i, z_j) — Minimum-Bayes-Risk consensus (Thm: MBR SLLN).
  - ``majority_vote`` / ``plurality_gate`` : MCQ consensus with the strict-plurality (Condorcet) gate.

Pure numpy/stdlib (numpy is a light dep, like ``rl.embedding_metrics``); no torch/transformers here.
"""
from __future__ import annotations

from collections import Counter
from typing import Callable, Sequence

import numpy as np

Candidate = object  # usually str (a decoded hypothesis)


def score_candidates(candidates: Sequence[Candidate], reward_fn: Callable[[Candidate], float]) -> np.ndarray:
    """Score each candidate with a verifiable reward in arbitrary range. Returns float array (N,)."""
    return np.asarray([float(reward_fn(c)) for c in candidates], dtype=np.float64)


def best_of_n(candidates: Sequence[Candidate], reward_fn: Callable[[Candidate], float]) -> dict:
    """Best-of-N selection: pick the candidate maximizing a verifiable reward (β→0 limit of tilting).

    Returns {"index", "best", "scores", "reward"}. Ties resolve to the first argmax (deterministic).
    """
    if len(candidates) == 0:
        raise ValueError("best_of_n: empty candidate set")
    scores = score_candidates(candidates, reward_fn)
    idx = int(np.argmax(scores))
    return {"index": idx, "best": candidates[idx], "scores": scores, "reward": float(scores[idx])}


def softmax(x: np.ndarray, beta: float) -> np.ndarray:
    """Tempered softmax exp(x/β) normalized; β>0. β→0⁺ concentrates on argmax (best-of-N)."""
    if beta <= 0:
        raise ValueError("softmax: beta must be > 0 (use best_of_n for the β→0 limit)")
    z = np.asarray(x, dtype=np.float64) / beta
    z -= z.max()  # stable
    e = np.exp(z)
    return e / e.sum()


def soft_bon_select(candidates: Sequence[Candidate], reward_fn: Callable[[Candidate], float],
                    *, beta: float = 1.0, seed: int = 42) -> dict:
    """Soft best-of-N: sample candidate i with probability ∝ exp(R(z_i)/β).

    This realizes the finite-support tilting optimum q*(z) ∝ q0(z)·exp(R(z)/β) (candidates ~ q0).
    Returns {"index","best","scores","probs"}.
    """
    if len(candidates) == 0:
        raise ValueError("soft_bon_select: empty candidate set")
    scores = score_candidates(candidates, reward_fn)
    probs = softmax(scores, beta)
    idx = int(np.random.default_rng(seed).choice(len(candidates), p=probs))
    return {"index": idx, "best": candidates[idx], "scores": scores, "probs": probs}


def mbr(candidates: Sequence[Candidate], utility_fn: Callable[[Candidate, Candidate], float],
        *, references: Sequence[Candidate] | None = None) -> dict:
    """Minimum-Bayes-Risk consensus: pick argmax_i mean_j u(z_i, ref_j).

    With ``references=None`` the candidate pool is its own pseudo-reference set (self-consistency MBR);
    the empirical mean → E_{p_θ}[u] by the SLLN at O(1/√N) (Thm: MBR consistency).
    Returns {"index","best","expected_utility","utilities"}.
    """
    if len(candidates) == 0:
        raise ValueError("mbr: empty candidate set")
    refs = list(references) if references is not None else list(candidates)
    if len(refs) == 0:
        raise ValueError("mbr: empty reference set")
    util = np.asarray([[float(utility_fn(c, r)) for r in refs] for c in candidates], dtype=np.float64)
    exp_u = util.mean(axis=1)
    idx = int(np.argmax(exp_u))
    return {"index": idx, "best": candidates[idx], "expected_utility": float(exp_u[idx]), "utilities": exp_u}


def majority_vote(candidates: Sequence[Candidate]) -> dict:
    """Plurality vote over discrete candidates (e.g. MCQ letters). Returns counts + the (possibly tied) top."""
    if len(candidates) == 0:
        raise ValueError("majority_vote: empty candidate set")
    counts = Counter(candidates)
    top, n_top = counts.most_common(1)[0]
    return {"winner": top, "counts": dict(counts), "n_top": n_top, "n_total": len(candidates)}


def plurality_gate(candidates: Sequence[Candidate], *, margin: int = 1) -> dict:
    """Strict-plurality (Condorcet) gate: accept the top class only if it STRICTLY beats every other
    by ``margin`` votes; else abstain (``winner=None``).

    Guards majority selection against the near-chance / acoustic-confound counterexample where a
    dominant wrong class wins a hard vote. (Thm: plurality gate correctness.)
    Returns {"winner" | None, "accepted", "counts", "n_top", "runner_up"}.
    """
    mv = majority_vote(candidates)
    counts = Counter(candidates)
    ordered = counts.most_common()
    n_top = ordered[0][1]
    runner = ordered[1][1] if len(ordered) > 1 else 0
    accepted = (n_top - runner) >= margin
    return {"winner": mv["winner"] if accepted else None, "accepted": accepted,
            "counts": dict(counts), "n_top": n_top, "runner_up": runner}


def kl_best_of_n_bound(n: int) -> float:
    """Upper bound on KL(best-of-N ‖ q0): log N − (N−1)/N  (Thm: best-of-N KL bound)."""
    if n < 1:
        raise ValueError("kl_best_of_n_bound: N must be >= 1")
    return float(np.log(n) - (n - 1) / n)
