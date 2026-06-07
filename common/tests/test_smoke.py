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
