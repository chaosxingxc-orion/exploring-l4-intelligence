"""Smoke tests that run without the heavy ML stack installed."""
from __future__ import annotations


def test_import_package():
    import speechrl_common

    assert speechrl_common.__version__


def test_seed_everything_returns_seed():
    from speechrl_common import seed_everything

    assert seed_everything(123) == 123


def test_logger():
    from speechrl_common import get_logger

    log = get_logger("test")
    assert log.name == "test"


def test_reward_normalization_exact_match():
    from speechrl_common.rl.reward import exact_match_reward

    assert exact_match_reward("Hello, World!", "hello world") == 1.0
    assert exact_match_reward("cat", "dog") == 0.0


def test_prompt_instruction_formatting():
    from speechrl_common.models.prompts import instruction_for

    assert "French" in instruction_for("st", target_lang="French")


def test_new_registry_and_prompts():
    from speechrl_common.data import registry
    from speechrl_common.models.prompts import instruction_for

    assert registry.get("crema_d").task == "ser"
    assert registry.get("voxceleb").task == "sid"
    assert registry.get("covost2").task == "st"
    assert instruction_for("intent")
    assert instruction_for("lid")


def test_omni_embed_constants_import_only():
    # Import must not require torch / sentence-transformers (they load inside the loader).
    from speechrl_common.models.omni_embed import (
        DEFAULT_OMNI_EMBED_ID,
        EMBED_DIM,
        LoadedEmbedder,
    )

    assert EMBED_DIM == 2048
    assert "omni-embed" in DEFAULT_OMNI_EMBED_ID
    assert LoadedEmbedder is not None


def test_lazy_import_guard():
    """In a fresh interpreter, importing the package + new modules pulls NO heavy deps."""
    import subprocess
    import sys
    import textwrap

    code = textwrap.dedent(
        """
        import importlib, sys
        for m in [
            "speechrl_common",
            "speechrl_common.rl.embedding_metrics",
            "speechrl_common.rl.probe",
            "speechrl_common.rl.disentanglement",
            "speechrl_common.rl.metrics",
            "speechrl_common.models.omni_embed",
            "speechrl_common.eval.probing",
        ]:
            importlib.import_module(m)
        heavy = [h for h in ("torch", "transformers", "sentence_transformers", "sklearn", "sacrebleu")
                 if h in sys.modules]
        print(",".join(heavy))
        sys.exit(1 if heavy else 0)
        """
    )
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert r.returncode == 0, f"heavy deps imported at module import time: {r.stdout.strip()}"
