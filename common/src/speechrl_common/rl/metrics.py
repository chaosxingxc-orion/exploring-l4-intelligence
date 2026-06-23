"""Verifiable evaluation metrics shared across speech task families.

Classification accuracy / macro-F1 (numpy + stdlib), BLEU / chrF (sacrebleu, lazy), and EER
(numpy). All are label-derived (verifiable) — never model-judged — so they are safe RL rewards.
ASR keeps using ``speechrl_common.rl.reward.asr_reward``.
"""
from __future__ import annotations

import numpy as np

from speechrl_common.rl.reward import _normalize


def classification_accuracy(references, hypotheses) -> float:
    """Normalized exact-match accuracy over paired label lists, in [0, 1]."""
    refs = list(references)
    hyps = list(hypotheses)
    if not refs:
        return 0.0
    correct = sum(1 for r, h in zip(refs, hyps) if _normalize(str(r)) == _normalize(str(h)))
    return correct / len(refs)


def macro_f1(references, hypotheses) -> float:
    """Macro-averaged F1 over the label set present in references, in [0, 1]."""
    refs = [_normalize(str(r)) for r in references]
    hyps = [_normalize(str(h)) for h in hypotheses]
    labels = set(refs)
    f1s = []
    for lab in labels:
        tp = sum(1 for r, h in zip(refs, hyps) if r == lab and h == lab)
        fp = sum(1 for r, h in zip(refs, hyps) if r != lab and h == lab)
        fn = sum(1 for r, h in zip(refs, hyps) if r == lab and h != lab)
        prec = tp / (tp + fp) if (tp + fp) else 0.0
        rec = tp / (tp + fn) if (tp + fn) else 0.0
        f1s.append(2 * prec * rec / (prec + rec) if (prec + rec) else 0.0)
    return float(np.mean(f1s)) if f1s else 0.0


def bleu(references, hypotheses) -> float:
    """Corpus BLEU via sacrebleu (lazy), in [0, 100]. ``references``/``hypotheses``: list[str]."""
    import sacrebleu  # lazy ([metrics] extra)

    return float(sacrebleu.corpus_bleu(list(hypotheses), [list(references)]).score)


def chrf(references, hypotheses) -> float:
    """Corpus chrF via sacrebleu (lazy), in [0, 100]."""
    import sacrebleu  # lazy ([metrics] extra)

    return float(sacrebleu.corpus_chrf(list(hypotheses), [list(references)]).score)


def eer(scores, labels) -> float:
    """Equal Error Rate from match scores + binary labels (1=same, 0=different), in [0, 1].

    Numpy-only threshold sweep: returns the rate where false-accept ≈ false-reject.
    """
    scores = np.asarray(scores, dtype=np.float64)
    labels = np.asarray(labels).astype(int)
    if scores.size == 0:
        return 0.0
    order = np.argsort(-scores)
    y = labels[order]
    P = max(1, int(y.sum()))
    N = max(1, int((1 - y).sum()))
    tp = np.cumsum(y)
    fp = np.cumsum(1 - y)
    frr = 1.0 - tp / P          # false-reject rate (missed positives)
    far = fp / N                # false-accept rate
    i = int(np.argmin(np.abs(frr - far)))
    return float((frr[i] + far[i]) / 2.0)
