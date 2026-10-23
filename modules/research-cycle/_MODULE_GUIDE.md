# research-cycle 模块指南（多智能体对抗式选题闭环）

本目录是 `kris-yun/research-cycle-skill`（MIT）的**只读副本**，
只收录一个技能：`.codex/skills/research-cycle/SKILL.md`
（上游仓库除此单文件外只有 README/CHANGELOG/CONTRIBUTING 等开发文件）。

## 这个技能是什么

一条 **7 阶段闭环科研流水线**，为 Codex 设计，最大特色是选题阶段的
**多智能体对抗辩论** + **Semantic Scholar 定量 gap 验证**：

```
Phase 1  文献调研 + 对抗式 gap 发现
   1a  文献检索 + Semantic Scholar 验证（gap 大小定量分级）
   1b  Proposer / Reviewer / Evidence 三智能体对抗辩论
   1c  GO / REVISE / KILL 决策
Phase 2  创新设计（理论动机 + Borrow-and-Swap / Core-Upgrade 两策略）
Phase 3  Baseline 复现（官方代码 + 官方参数）
Phase 4  创新实现（最小改动 + 模块开关）
Phase 5  实验验证（多次运行 + 消融 + 跨数据集）
Phase 6  分析与迭代 → 回到 Phase 2
Phase 7  论文写作
```

**Gap 大小分级**（S2 API 论文计数）：<50 窄gap（高风险高回报）/ 50–100 中窄 /
100–500 中 / >500 宽（需强差异化）。

**对抗辩论判定**：GO = 过全部 FATAL 检查且 MAJOR ≤3 个可修；
REVISE = 1–2 个可修 FATAL；KILL = 有不可修复 FATAL 或核心假设被证伪。

## 与套件内其他选题模块的分工

选题能力在本套件有三层，按用户表达选：

| 用户说 | 去哪 | 打法 |
|---|---|---|
| 证据驱动五选题 / 顶刊思路 | `modules/cell-suite/cell-brainstorm/` | 五题论证稿 + 质量门禁脚本 |
| 苏格拉底式追问 / 想和人聊聊把想法磨出来 | `modules/sci-brain/brainstorm-ideas/` | 问答式导师，可选领域顾问子智能体 |
| **对抗辩论找 gap / scientific brainstorming / research cycle / 定量验证方向有没有人做过** | **本模块** | 三智能体对抗 + S2 计数 + GO/REVISE/KILL，且一条龙走到复现与写作 |

它不是总控：完整十环节流程仍由 `modules/codex-research-workflow/` 统筹，
本模块主要补强 **① 选题**，并在用户「要从头跑完一个研究方向」时整条接管。

## 红线（继承上游，套件一律遵守）

1. **gap 大小靠 S2 计数说话**，不靠感觉；请求间隔 ≥1.5s。
2. Reviewer 的 FATAL 攻击必须逐条有依据（理论缺陷/实验缺口/新颖性不足/不可复现），禁止为辩论而辩论。
3. `EVIDENCE_CHECK.md` 中每条文献声明必须核真（引用真实、数据准确、结论被支持）。
4. Phase 3 baseline 复现必须用**官方代码 + 官方参数**，不复现就宣称提升等于没有标尺。
5. Phase 5 必须多次运行 + 消融 + 跨数据集；单 seed 的「提升」不构成结论。

## 许可

MIT，见本目录 `LICENSE`（Copyright (c) 2026 Kris Yun）。
