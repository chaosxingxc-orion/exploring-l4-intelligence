#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Self-contained bibliography generator (v9-review §5.2 required correction).

The v9 appendix compressed A.1/A.2/A.4 to back-references into the pinned v8
appendix — traceable, but not self-contained. This generator produces the
FULL reference closure as a reader-visible dated artifact, machine-extracted
from the PINNED predecessor blobs (no hand copying):

  v8 appendix  @ blob 87619149711f4541441210dc2689977ca0a0df8b  (A.1/A.2/A.3/A.4/A.5)
  v9 appendix  @ blob 80bd82072289387be9d2a4391fa2026fe36b3522  (A.3 +2, A.5 +1, A.6)

plus the round-11 queue additions (metadata only where first-hand verified;
queue entries complete their metadata at Stage-1B fetch time).

Deterministic output; rerun => zero diff. Writes
wiki/survey/2026-07-19-sf-bibliography-v1.md
"""
import io
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "wiki", "survey", "2026-07-19-sf-bibliography-v1.md")
V8_BLOB = "87619149711f4541441210dc2689977ca0a0df8b"
V9_BLOB = "80bd82072289387be9d2a4391fa2026fe36b3522"

SECTIONS_V8 = {"A.1": "DEEPLY_READ", "A.2": "CALIBRATION", "A.3": "KNOWN_QUEUE",
               "A.4": "MEASUREMENT_INSTRUMENT", "A.5": "BOUNDARY/NEGATIVE_PRIOR"}
SECTIONS_V9 = {"A.3": "KNOWN_QUEUE", "A.5": "BOUNDARY/NEGATIVE_PRIOR",
               "A.6": "STAGE1B_FIRST_BATCH(P2)"}

ROUND11 = [
    ("KNOWN_QUEUE", "Reinforced Agent: Inference-Time Feedback for Tool-Calling Agents（正式版去重绑定）",
     "Anh Ta et al., 2026", "https://aclanthology.org/2026.gem-main.13/ · https://arxiv.org/abs/2604.27233"),
    ("BOUNDARY/NEGATIVE_PRIOR", "Mapping Smarter, Not Harder（test-time RL agent;new-info 边界）",
     "登记待读（作者见官方页）", "https://aclanthology.org/2025.emnlp-industry.75/"),
    ("BOUNDARY/NEGATIVE_PRIOR", "ASR-TRA: Boosting ASR Robustness via Test-Time RL with Audio-Text Semantic Rewards（权重/prompt 更新边界）",
     "Linghan Fang, Tianxin Xie, Li Liu, 2026", "https://arxiv.org/abs/2603.05231"),
    ("MEASUREMENT_INSTRUMENT(trained-RM)", "Dual-Axis Generative Reward Model Toward Semantic and Turn-taking Robustness in Interactive Spoken Dialogue Models",
     "Yifu Chen et al., 2026", "https://aclanthology.org/2026.acl-long.6/"),
    ("MEASUREMENT_INSTRUMENT(trained-RM)", "SDiaReward / ESDR-Bench（口语对话偏好 RM）",
     "登记待读（作者见官方页;仓内 2026-07-06 archive 裁定在案）", "https://arxiv.org/abs/2603.14889"),
    ("STAGE1B_FIRST_BATCH(P2)", "TangramSR: Can Vision-Language Models Reason in Continuous Geometric Space?",
     "登记待读（作者见官方页）", "https://arxiv.org/abs/2602.05570"),
    ("STAGE1B_FIRST_BATCH(P2)", "Reward Modeling for Multi-Agent Orchestration（OrchRM）",
     "登记待读（作者见官方页）", "https://arxiv.org/abs/2606.13598"),
    ("STAGE1B_FIRST_BATCH(P2)", "ToolRM: Towards Agentic Tool-Use Reward Modeling",
     "登记待读（作者见官方页）", "https://aclanthology.org/2026.findings-acl.419/"),
    ("STAGE1B_FIRST_BATCH(P2)", "Exploring Reasoning Reward Model for Agents（Agent-RRM）",
     "登记待读（作者见官方页）", "https://aclanthology.org/2026.findings-acl.95/"),
    ("STAGE1B_FIRST_BATCH(P2)", "Decoupling Conversational Dynamics in Full-Duplex Spoken Models through RL（DuplexPO）",
     "登记待读（作者见官方页）", "https://arxiv.org/abs/2607.07148"),
    ("STAGE1B_FIRST_BATCH(P2)", "Multi-Faceted Interactivity Alignment in Full-Duplex Speech Models",
     "登记待读（作者见官方页）", "https://arxiv.org/abs/2606.11167"),
]


def blob_text(blob):
    p = subprocess.run(["git", "show", blob], cwd=REPO, capture_output=True)
    if p.returncode != 0:
        raise SystemExit(f"cannot read pinned blob {blob}")
    return p.stdout.decode("utf-8", errors="replace")


def parse_appendix(text, wanted):
    """Extract 3+-column table rows per '### A.x' section."""
    out = {}
    cur = None
    for line in text.splitlines():
        m = re.match(r"^###\s+(A\.\d)", line)
        if m:
            cur = m.group(1) if m.group(1) in wanted else None
            continue
        if line.startswith("## "):
            cur = None
        if cur and line.startswith("|") and not re.match(r"^\|[-\s|]+$", line):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 3 and cells[0] not in ("引用", "工具", "工作"):
                out.setdefault(cur, []).append(cells)
    return out


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    v8 = parse_appendix(blob_text(V8_BLOB), SECTIONS_V8)
    v9 = parse_appendix(blob_text(V9_BLOB), SECTIONS_V9)
    groups, seen = {}, set()
    url_pat = re.compile(r"https?://\S+")

    def add(role, title, authors, link):
        urls = set(url_pat.findall(link))
        if urls & seen:
            return
        seen.update(urls)
        groups.setdefault(role, []).append((title, authors, link))

    # ROUND11 first: its Reinforced Agent row carries the ACL-GEM dedup binding
    # and supersedes the arXiv-only predecessor row (same work, any-URL dedup).
    for role, title, authors, link in ROUND11:
        add(role, title, authors, link)
    for sec, role in SECTIONS_V8.items():
        for cells in v8.get(sec, []):
            add(role, cells[0], cells[1], cells[-1])
    for sec, role in SECTIONS_V9.items():
        for cells in v9.get(sec, []):
            add(role, cells[0], cells[1], cells[-1])

    lines = [
        "---",
        'artifact_id: "SF-BIBLIOGRAPHY-V1-2026-07-19-01"',
        'title: "自包含书目 v1（机器生成:v8/v9 钉定附录抽取 + 第十一轮补充;禁止手改——改动请改生成器或源件后重跑）"',
        "date: 2026-07-19",
        'generated_by: "scripts/survey/sf_bibliography_generator.py（源 = v8 blob 8761914971… / v9 blob 80bd820722… + 核验后的 round-11 补充表;确定性输出重跑零 diff）"',
        'discipline: "角色分节不混分母;登记待读条目在 Stage-1B fetch 时补全元数据;v9-review §5.2 引用呈现修正——读者可见书目自此为生成件"',
        "---",
        "",
        "# 自包含书目 v1",
        "",
    ]
    total = 0
    order = ["DEEPLY_READ", "CALIBRATION", "KNOWN_QUEUE", "MEASUREMENT_INSTRUMENT",
             "MEASUREMENT_INSTRUMENT(trained-RM)", "BOUNDARY/NEGATIVE_PRIOR",
             "STAGE1B_FIRST_BATCH(P2)"]
    for role in order:
        rows = groups.get(role, [])
        if not rows:
            continue
        total += len(rows)
        lines.append(f"## {role}（{len(rows)} 条）")
        lines.append("")
        lines.append("| 引用 | 作者/年份 | 稳定链接 |")
        lines.append("|---|---|---|")
        for t, a, l in rows:
            lines.append(f"| {t} | {a} | {l} |")
        lines.append("")
    lines.append(f"**合计 {total} 条。**")
    text = "\n".join(lines) + "\n"
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(text)
    print(f"wrote {os.path.relpath(OUT, REPO)}: {total} entries across {sum(1 for r in order if groups.get(r))} roles")
    return 0


if __name__ == "__main__":
    sys.exit(main())
