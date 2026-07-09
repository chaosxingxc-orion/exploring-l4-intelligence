# 2026-07-09 · Step-1 判据冻结记录（owner 签署）

> **性质**：Stage-1 Step-1 基线锁定的判据冻结记录（prereg）。冻结对象 =
> W1 `scripts/baselines/{templates.py, metrics.py, run_baseline.py, FREEZE_SHEET.md}`
> 于本记录同 commit 的状态 + 下列 owner 裁定。冻结后波 1 网格照跑，模板/指标在切片内不再更改
> （append-only）。

## Step-0 收官事实（冻结的前提）

- 底座冒烟：**Qwen3-Omni-30B GGUF ✅（既有）+ MERaLiON-2-3B GGUF ✅**（license 复核通过
  无 NC；zh/en 转写精确命中；36s 加载；钉扎构建原生支持，未动 patch）；
  **minicpm-o BLOCKED**（transformers 5.12 vs 模型钉 4.51 主版本断裂）；
  **moss-audio BLOCKED**（发布快照打包缺陷：processor auto_map 指向不存在模块 + 无 modeling
  文件，需 OpenMOSS 官方包）；nemotron NVFP4 尝试进行中（不影响波 1）。
- qwen3-omni HF int4 已删（owner 裁定，GGUF 留一份）；gpu_session.sh 分时协议就绪；
  loader **65/65 全绿**（meld ffmpeg 与 air-bench Speech_Grounding 解堵落地；heysquad +
  vocalbench 四轴补齐）；网格 **76 格 dry-run 零错误**。

## Owner 冻结裁定（2026-07-09）

1. **波 1 底座 = 双 GGUF 先跑**（Qwen3-Omni + MERaLiON-2）。minicpm/moss 解堵路线（owner 同轮
   追加指示）：**优先寻源 GGUF 替换以统一 llama.cpp 驱动栈**——寻到且冒烟通过 → 下载 GGUF 并
   删除 HF 版本；GGUF 需要更新 llama.cpp → 上报裁决（不擅动钉扎引擎）；寻不到 → 回退 HF venv
   （transformers==4.51 + moss 官方包）或以其他 GGUF 原生底座替换阵容位（owner 裁决）。
   补入后回补波 1 数据集。
2. **K4/K6/K7 闭集标签清单 = 全池扫描**（一次性元数据 pass 构建 corpus-true 清单，冻结前完成）。
3. **SQuAD-zh/OpenbookQA-zh 双 loader：波 1 双跑一次作交叉验证，之后弃 legacy**（差异即 bug 信号）。
4. **ifeval checker 补取**（google-research instruction_following_eval 子树，Apache-2.0），
   波 3 前接线，K11 完整入网格。

确认类（按 FREEZE_SHEET 推荐通过）：K5 收窄为属性探针（cn-celeb1/voxceleb1 → step-2 kNN 主场）·
TEST_SEED=SLICE_SEED+1000 · ST 任务族豁免入档（恢复需 covost2 CV-mp3 补取另裁）· sd-qa 按
QA-containment（K8 计分）· K9 闭卷仅诊断（真检索指标在 step 2）· TruthfulEval 保留标
directional-weak · air-bench Speech_Grounding 签字位因解堵消失。

## 同日后续：阵容终裁（owner，GGUF 寻源后）

GGUF 寻源判定：minicpm-o-4.5 音频路径**仅存于 OpenBMB fork**（主线含 master 只合了视觉）——
换用等于引入第二分叉引擎；moss-audio **无 GGUF 无任何 llama.cpp arch 支持**（仅 SGLang fork）。
替代候选（Gemma-4 E4B / Ultravox-8B / MERaLiON-10B / Qwen2.5-Omni-7B）已呈。
**Owner 裁定：①双底座定稿**（Qwen3-Omni + MERaLiON-2-3B 贯穿波 1-3；谱系多样性由 step-3 的
非 Whisper ASR-ensemble 验证器补足，替代底座一个不下）；**②删除 minicpm/moss HF 目录**
（~36GB，栈上不可用；deferred-not-deleted，重下渠道入 lock 注记；lock 模型数 5→3）。
nemotron NVFP4 尝试降级为台账豁免证据用途（不再是阵容候选）。

## 波 1 执行口径

范围 = K8 全部 + K9 闭卷 + K1/K2 × {qwen3-omni-30b-gguf, meralion-2-gguf} × {dev40, test60}；
gpu_session 串行（每底座常驻 server 批跑其全部格）；每格结果 JSON（manifest/params/CI/boundary）
入 `_repro/baselines/`，断点续跑（已存在格跳过）；全程 directional 分级。
