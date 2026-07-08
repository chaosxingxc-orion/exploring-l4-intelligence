---
title: "T0 — 模型演进有效性探针:冻结 Qwen3-Omni 能否 in-context 消费注入的外部知识(结果)"
date: 2026-07-07
stage: 1-directional
status: "Stage-1 directional (n=40×2, single-touch, NOT significance-bearing). WS-0 of the knowledge track. Boundary-clean (gold-as-reference = ceiling probe only). Owner review pending; wiki-sync deferred。"
---

# T0 有效性探针 —— 结果

**Why.** 综述里"语音-LLM 不 fine-tune 就用不好检索知识"(MARS/RASST/VoxMind)是在 **2025→2026-04 模型**上观察到的;我们的基座是 **Qwen3-Omni(2026-04/05,更强)**。本探针在**我们的实际模型**上重验这条承重前提(directional-only)。

**设计.** 3 臂,贪心 temp0,**每臂都带音频查询**;`gen()` = audio + text-instruction → llama-server(Q8_0 GGUF)。A 不注入;B 注入**正确 gold** 当参考(=消费**天花板**);C 注入**错配 gold**(=placebo)。奖励 = `gold ⊆ 归一化输出`。脚本 `scripts/t0_consumption_probe.py`,产物 `_repro/t0_consumption_probe.json`,seed 20260706。

## 结果

| 集 (n=40) | A 不注入 | B 注入正确(天花板) | C 注入错配(placebo) | B−A | B−C | A-fails 救回率 (n_fails) |
|---|---|---|---|---|---|---|
| big-bench-audio | 0.70 | 0.775 | 0.625 | +0.075 | +0.15 | 0.417 (12) |
| vocalbench-zh | 0.55 | 0.75 | 0.475 | +0.20 | +0.275 | 0.444 (18) |

## 解读(directional,n=40 不定论)

1. **消费通道是开的.** B>A 且 B>C(两集一致)→ 冻结 Qwen3-Omni **能 in-context 消费注入的文本知识**;不是老模型那堵"不训练就用不了"的墙。→ 纯"使能消费"框架被削弱。
2. **但消费不可靠.** 即便把**正确答案**当参考喂进去,B 仅 ~0.75–0.78;在本来答错的题上**只救回 ~42%**。→ 纯"只优化选择"也不成立:选择完美(给对知识)时利用率仍漏。
3. **错配注入拖累(C<A).** 模型**过度信任**注入文本,错误参考把它带偏 → **gating/admission 是真问题**。

## 对 thesis 的判读:GO,但重新定向

不是"从零使能消费",也不是"只做选择"。**"外部知识的利用效率"在我们的 2026 模型上有明确的、双向的、训练无关可干预的 headroom**:
- **(a) 采纳/门控(admission/gating):** C<A 说明该拒的注入要拒 —— reward-guided 门控的空间。
- **(b) 注入/利用方式(injection/use):** B 远未到 1.0 —— 该用上的没用上,injection-format/强调/位置的 reward 优化空间。

⇒ **T0 GATE = 通过(GO)**,thesis 目标量坐实为"利用效率",TFRL 杠杆指向 **门控 + 注入-利用** 两侧。T2 的效果映射据此定向。

## 边界与 caveat(写死)
- **n=40、单触点、贪心、不定论**(Stage-1 directional);B−A 在 big-bench(+0.075)很小/噪声大;最稳的信号是"救回率仅 ~42%"与"C<A"(两集一致)。
- **B/C 注入 gold 当参考 = 天花板探针,directional-only,绝非可部署增益**(把答案喂进去只为界定"消费上限")。真·不完美检索的利用(H0/H-util)在 **T7**,用**外部知识非答案** + provenance-firewall + answer-overlap 审计。
- 奖励是 substring-match,B<1.0 部分反映模型**没有照抄**注入文本(答自音频/改述),即真实的部分消费。
- 复现:`SPEECHRL_DATA_DIR=<repo>/speechrl-data python -u scripts/t0_consumption_probe.py`。
