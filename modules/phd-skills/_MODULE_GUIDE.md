# phd-skills 模块指南（代码复现 + 论文数值核验）

本目录是 `fcakyon/phd-skills`（MIT，作者 Fatih Cagatay Akyon）的**只读副本**，
收录 2 个与「论文 ↔ 代码」一致性直接相关的技能；其余 9 个上游技能
（debug / launch / compare / literature-research / experiment-design /
dataset-curation / latex-setup / paper-writing / research-publishing /
reviewer-defense）**未收录**——本套件中已有对应或更强的模块
（见下文「分工」），避免同一能力重复占上下文。

## 收录了什么

| 子技能 | 管什么 | 触发词 |
|---|---|---|
| `reproduce/` | 从 arXiv/OpenReview 链接到复现实验的 **7 阶段流水线**：取全文 → 清点官方代码 → 超参缺口分析 → 补齐实现 → 数据集获取（私有数据集用相似公开集替代并留痕）→ 冒烟运行 → 按论文报告轮次做复现对比 | 复现论文、代码复现、reproduce、replicate、re-run paper、这篇论文没代码 |
| `paper-verification/` | **论文数值 ↔ 代码/数据核验**：逐个数字追溯来源、公式-代码对齐检查、claim-证据一致性审计 | verify claims、check numbers、数字对不上、formula vs code、audit the paper |

## 上游交叉引用的本地替代（重要）

`reproduce` 的 `references/06-smoke.md`、`references/07-replicate.md`
引用了本套件**未收录**的上游 slash 命令。执行到这些步骤时按下面的本地做法来：

| 上游引用 | 本地替代做法 |
|---|---|
| `/phd-skills:debug`（冒烟失败排查） | 直接读 `reproduce/references/06-smoke.md` 的失败分级表，逐级排查；不得凭猜测改代码或盲目重启 |
| `/phd-skills:launch`（长跑前检查单） | 用 `modules/cell-suite/cell-plan/SKILL.md` 的研究计划结构做长跑前检查（ seeds、轮次、日志落盘、断点续跑） |
| `/phd-skills:compare`（按论文报告轮次对比） | 按 `references/07-replicate.md` 的判据手工对齐：**只在论文报告的轮次/检查点上对比**，禁止拿当前中间结果对比论文最终数 |
| `paper-verification` 技能 | ✅ 已收录，就在本目录 `paper-verification/` |

## 与套件内其他模块的分工

- **`citation-check` / `nature-ref-verifier`**：管**参考文献本身**真不真（作者/标题/年份/卷期/页码是否编造）。
- **`paper-verification`**：管**论文里的数字和公式**与代码/数据是否对得上（数字追得到源、公式与实现一致）。
- **`reproduce`**：管从零把论文跑起来，产出 `results.md`，每个指标打三档标签之一：
  `[matched within 0.X pp]` / `[gap, hypothesis: ...]` / `[fundamental disagreement, see X]`。

## 红线（继承上游，套件一律遵守）

1. **超参不许编**：`gaps_filled.md` 里每个补填值必须带出处（论文章节/官方代码/作者回复），没有出处的标「假设」。
2. **复现结论必须给绝对差**（不只给百分比），且只在论文报告的轮次上对比。
3. 冒烟运行分三级（forward pass → 1 step → 20 iters），前一级不过不进入下一级。
4. 私有数据集缺失时用相似公开数据集替代，**必须**写 `dataset_substitution.md` 说明替代关系，不得冒充原数据集。
5. Semantic Scholar / arXiv 等外部 API 遵守请求间隔（S2 ≥1.5s）；`S2_API_KEY` 可选，没有也能跑（限额更低）。

## 许可

MIT，见本目录 `LICENSE`（Copyright (c) 2026 Fatih Cagatay Akyon）。
