"""Prompt templates for speech tasks, shared across the four works."""
from __future__ import annotations

# Instruction templates per traditional speech task (W3 multi-task RL uses these).
TASK_INSTRUCTIONS: dict[str, str] = {
    "asr": "Transcribe the spoken audio into text, verbatim.",
    "st": "Translate the spoken audio into {target_lang} text.",
    "ser": "Identify the speaker's emotion from the audio.",
    "sid": "Identify who is speaking in the audio.",
    "gender": "Identify the speaker's gender from the audio.",
    "keyword": "Detect whether the keyword '{keyword}' is spoken in the audio.",
}


def build_chat(instruction: str) -> list[dict]:
    """Build a Qwen2-Audio-style chat turn with an audio placeholder + instruction."""
    return [
        {
            "role": "user",
            "content": [
                {"type": "audio", "audio_url": "<audio>"},
                {"type": "text", "text": instruction},
            ],
        }
    ]


def instruction_for(task: str, **fmt: str) -> str:
    """Look up and format a task instruction (raises KeyError on unknown task)."""
    return TASK_INSTRUCTIONS[task].format(**fmt)
