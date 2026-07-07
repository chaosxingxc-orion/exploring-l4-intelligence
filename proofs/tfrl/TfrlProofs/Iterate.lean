import Mathlib

set_option linter.style.header false
set_option linter.style.longLine false

/-!
# T5(续)— 迭代过程收敛 C1(信赖域单调收敛)+ C2(预算上限 N*)

> **WS-E 归位 (2026-07-07).** 本文件此前只存在于 gitignored 的 `speechrl-data/_repro/Iterate.lean`,
> 未被 `TfrlProofs.lean` import、未提交,却被 Decision-Log/E6 反复宣称"已在 `proofs/tfrl` sorry-free
> 交付、C1/C2/C4 全库绿"——那是**文档夸大**(与 commit `8298846` "was falsely claimed verified" 同类)。
> 现移入 `proofs/tfrl/TfrlProofs/` 并加入 import,使 C1/C2 **真正**进入已验证库。
> **诚实前提:** 下面是抽象单调过程 `x : ℕ → ℝ` 的正确性/收敛;`δ>0`(每步增益下限)与 `M`(上界)是
> **假设**,不是从知识注入更新规则推出的。training-free 设定下奖励代理有非零误差地板 `τ*>0`,故真实系统
> 只能收敛到 `oracle − 2τ*` **邻域**,而非 `oracle`;"realized→oracle" 的极限对部署系统不成立。
> 见 `[[2026-07-07-knowledge-proof-honest-accounting-and-feasibility]]`。

`Realization.lean` 给了 fixed-`q₀` 的 selection 收敛(C4,`τ→0 ⇒ oracle`)。这里补上 doc 里标为
"待 formalize" 的 **迭代过程** 收敛:把记忆/RAG 的 training-free-RL 方案看作一个迭代 `x : ℕ → ℝ`,
`x t` = 第 t 步注入-上下文 `q₀(c_t)` 下的目标值(奖励/准确率代理)。

约束项:**C1 = KL 信赖域**——把每步步长限住,等价地给出**每步增益下限 `δ > 0`**(信赖域内 `δ(ε)`)。
两段结构(理论轨要求):
* **负(无约束不收敛):** 若过程"永远严格改进"(每步 `+δ`),则目标无上界 —— 对有界奖励**不可能**
  (`unconstrained_diverges`)。即无约束地一直优化必然发散/撞界。
* **正(有约束收敛 + 预算):** 单调有界过程**收敛**(`monotone_bounded_converges`,C1);且信赖域增益
  下限 `δ` + 目标上界 `M` ⇒ **改进步数被预算上限住** `N* ≤ (M − x₀)/δ`(`improve_budget`,C2 = HedgeTune/
  Best-of-Poisson 那个内点最优 N* 的离散有限化),之后必 δ-plateau(收敛)。

双轨:`x t` ⟷ 代码里 RAG/记忆 选择-注入回路每轮的奖励;`δ` ⟷ 信赖域 β / 每步接受门的最小增益;
`N*` ⟷ 检索/注入的预算上限(`decode.kl_best_of_n_bound` 的 N)。(⚠ 双轨绑定当前仅在 docstring 层,
Lean 算子与 Python selector 之间尚无 CI 同步检查——见 WS-E Part 3。)
-/

namespace TfrlProofs.Iterate

open Filter Topology

/-- 望远镜求和:若前 `N` 步每步至少增益 `δ`,则 `x N ≥ x 0 + N·δ`。 -/
theorem iterate_telescope (x : ℕ → ℝ) (δ : ℝ) :
    ∀ N, (∀ t, t < N → x t + δ ≤ x (t + 1)) → x 0 + (N : ℝ) * δ ≤ x N := by
  intro N
  induction N with
  | zero => intro _; simp
  | succ n ih =>
    intro h
    have h1 : x 0 + (n : ℝ) * δ ≤ x n := ih (fun t ht => h t (Nat.lt_succ_of_lt ht))
    have h2 : x n + δ ≤ x (n + 1) := h n (Nat.lt_succ_self n)
    have hc : ((n + 1 : ℕ) : ℝ) = (n : ℝ) + 1 := by push_cast; ring
    rw [hc]
    have hdist : x 0 + ((n : ℝ) + 1) * δ = (x 0 + (n : ℝ) * δ) + δ := by ring
    rw [hdist]; linarith

/-- **C2 预算上限 N\*.** 若目标每步增益 ≥ `δ > 0` 且有上界 `M`,则改进步数 `N ≤ (M − x 0)/δ`. -/
theorem improve_budget (x : ℕ → ℝ) (δ M : ℝ) (N : ℕ) (hδ : 0 < δ)
    (hgain : ∀ t, t < N → x t + δ ≤ x (t + 1)) (hbdd : x N ≤ M) :
    (N : ℝ) ≤ (M - x 0) / δ := by
  have ht := iterate_telescope x δ N hgain
  have hle : x 0 + (N : ℝ) * δ ≤ M := le_trans ht hbdd
  rw [le_div_iff₀ hδ]
  linarith

/-- **C1 收敛.** 单调不减且有上界的迭代收敛到其上确界. -/
theorem monotone_bounded_converges (x : ℕ → ℝ) (hmono : Monotone x) (M : ℝ)
    (hbdd : ∀ n, x n ≤ M) : Tendsto x atTop (𝓝 (⨆ n, x n)) := by
  apply tendsto_atTop_ciSup hmono
  exact ⟨M, by rintro y ⟨n, rfl⟩; exact hbdd n⟩

/-- **负结果:** 无约束地"每步严格增益 `δ`"与"目标有界"矛盾——无约束优化必然撞界/不收敛于有界目标. -/
theorem unconstrained_diverges (x : ℕ → ℝ) (δ : ℝ) (hδ : 0 < δ)
    (hgain : ∀ t, x t + δ ≤ x (t + 1)) : ¬ ∃ M, ∀ n, x n ≤ M := by
  rintro ⟨M, hM⟩
  obtain ⟨N, hN⟩ := exists_nat_gt ((M - x 0) / δ)
  have hbud := improve_budget x δ M N hδ (fun t _ => hgain t) (hM N)
  linarith

end TfrlProofs.Iterate
