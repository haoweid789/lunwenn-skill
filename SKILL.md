---
name: lunwenn-skill
description: "论文全流程综合技能（lunwenn-skill）。把「一个研究课题 → 一篇可投稿论文」的整条链路装进一个技能：选题 → 检索 → 综述 → 统筹 → 统计 → 绘图 → 写作 → 润色 → 去 AI 味 → 引文核验 → 对抗审稿 → 返修回复 → 投稿 → 汇报/PPT。聚合十五个上游项目（nature-skills、PaperSpine、academic-research-skills、paper-writing-skill、literature-survey-skill、citation-check-skill、paperpipe/papi、PaperQA2、Anthropic skill-creator、sci-brain、Cell 科研套件、ai-patina/human-voice、phd-skills、research-cycle-skill、用户自建 humanized-writing）。触发词：写论文、论文全流程、文献综述、综述、精读论文、找 gap、论文写作、论文润色、去 AI 味、论文结构、贡献凝练、motivation、引文核验、参考文献造假、图表、科研绘图、可编辑矢量图、Nature 风格、模拟审稿、对抗审稿、rebuttal、回复审稿意见、投稿、代码复现、复现论文、reproduce、research cycle、scientific brainstorming、对抗辩论、paper writing、literature review、manuscript、academic pipeline、research to paper、citation check、reviewer response、科研工作流、十环节、Codex 工作流、选题、头脑风暴。"
agent_created: true
---

# lunwenn-skill —— 论文全流程（论文 = lùnwén）

本技能是**路由总控**，不自带全部原文：它把十五个上游项目的成熟方法编成一条流水线，
按需加载 `modules/` 下对应模块的入口文件。**加载纪律：只读当前阶段需要的文件，
大目录按需摘取，不要整目录塞进上下文。**

## 〇、两套流水线（先选哪套）

本技能提供**两套互相嵌套**的流水线，按用户的表达方式选择：

| 用户怎么说 | 走哪套 | 特点 |
|---|---|---|
| 「按科研工作流走」「从选题到投稿」「帮我按流程来」「十环节」 | **十环节制**（`modules/codex-research-workflow/`） | 10 个科研决策环节，跨上游项目调度，门槛明确 |
| 「写一篇论文」「帮我把稿子润色」等具体单点诉求 | **十二站制**（本文档第二节） | 按论文产物排序，13 个交付站点 |

两套不冲突：十环节制在③④⑦⑨处指向十二站制的对应站点。**不确定时默认走十二站制的单点直达表（第三节），**
用户明确要求全流程时才加载十环节统筹层。

## 一、模块清单（入口文件）

| 模块 | 目录 | 入口 | 一句话 |
|---|---|---|---|
| **codex-research-workflow** | `modules/codex-research-workflow/` | `SKILL.md` | **十环节统筹层**：选题→检索→综述→统筹→统计→绘图→写作→润色→投稿→汇报，跨模块调度 + 门槛 + 交接单 |
| nature-skills | `modules/nature-skills/` | 各子技能 `SKILL.md`（23 个） | Nature/CNS 系写作、润色、图、引文、审稿回复、读文、PPT、专利、统计 |
| PaperSpine | `modules/paperspine/` | `SKILL.md` + `references/paper-spine-production-protocol.md` | motivation 驱动的中心主张—证据—章节骨架、修订矩阵 |
| academic-research-skills | `modules/academic-research-skills/` | `academic-pipeline/SKILL.md` | 10 阶段总编排（research→write→审→改→重审→定稿） |
| paper-writing-skill | `modules/paper-writing-skill/` | `SKILL.md` | 结构化立意 + 五阶段写作管线 + 修辞动作 + 红队协议 |
| literature-survey-skill | `modules/literature-survey-skill/` | `SKILL.md` | Intent→Triage→Deepen→Synthesize 文献综述四阶段 |
| citation-check | `modules/citation-check/` | `SKILL.md` | 两遍式引文核验（抽 claim → 逐条验真伪/一致性） |
| paperpipe | `modules/paperpipe/` | `skills/papi/SKILL.md` | 论文库 CLI（`papi`）+ 6 个子工作流 |
| PaperQA2 | `modules/paper-qa/` | `SKILL.md` | 本地 PDF 目录 RAG 问答（`pqa`） |
| **cell-suite** | `modules/cell-suite/` | `cell/SKILL.md`（总路由）+ 12 个成员 | **Cell 科研套件**：证据驱动选题、研究计划排程、顶刊综述 Word、英文深度润色、审稿回复、投稿包、可视化代码、数据图复现、可编辑矢量图重建 |
| **human-voice** | `modules/human-voice/` | `SKILL.md` | **改 AI 稿的结构级手术**：五维审计 + 14 个重写动作 + 句长/词汇/痕迹量化自查（`humanity_check.py`） |
| **sci-brain** | `modules/sci-brain/` | 各子技能 `SKILL.md`（16 个） | **文献知识库 + 苏格拉底式选题 + 自动研究循环**：survey 建库、brainstorm-ideas 追问选题、autoresearch 验证循环、write-paper / review-paper、write-slides |
| **phd-skills** | `modules/phd-skills/` | `reproduce/SKILL.md` + `paper-verification/SKILL.md`（分工见 `_MODULE_GUIDE.md`） | **代码复现 7 阶段流水线 + 论文数值/公式核验**：从 arXiv 链接到可对比的复现结果，数字逐个追溯来源 |
| **research-cycle** | `modules/research-cycle/` | `SKILL.md` | **多智能体对抗式选题闭环**：S2 定量 gap 分级 + Proposer/Reviewer/Evidence 辩论 + GO/REVISE/KILL，7 阶段一路走到复现与写作 |
| skill-creator | `modules/skill-creator/` | `SKILL.md` | 维护/评测/改进本技能自身 |
| humanized-writing | `modules/humanized-writing/` | `SKILL.md` | 你的去 AI 味写作 + `scripts/check_prose.py` 自查 |

> `humanized-writing` 是**原目录的逐字节副本**；原目录
> `C:\Users\qw123\.workbuddy\skills\humanized-writing\` 保持原样、不受本技能影响，二者内容一致。

> `cell-suite` 与 `sci-brain` 是 v2 新增的只读副本，`nature-skills`/`phd-skills`/`research-cycle`
> 为后续版本新增；其内部付费/外部服务依赖见
> [`modules/codex-research-workflow/SKILL.md`](modules/codex-research-workflow/SKILL.md) 第四节。

## 二、端到端流水线（12 站，可裁剪可跳站）

| # | 阶段 | 主产物 | 首选模块 | 交叉/备用 |
|---|---|---|---|---|
| 0 | 立项与边界 | `scope.md`（问题/资源/约束/红线） | `paper-writing-skill` brainstorming | `academic-pipeline` intake |
| 1 | 检索与语料库 | `corpus/`（PDF 库）+ 检索记录 | `literature-survey-skill`、`paper-qa`、`paperpipe` | `nature-academic-search`、`nature-downloader` |
| 2 | 精读与综述综合 | `litreview.md`（相关研究表 + gap 列表） | `literature-survey-skill` | `nature-reader`、`nature-paper-xray`、`deep-research` |
| 3 | 论证骨架与贡献 | `spine.md`（中心主张—证据—章节） | `PaperSpine` | `academic-paper/structure-architect` |
| 4 | 正文写作 | `paper.tex/.md/.docx` | `paper-writing-skill`、`nature-writing` | `academic-paper`（12 agent） |
| 5 | 语言润色 / 去 AI 味 | 润色稿 | `humanized-writing` | `nature-polishing` |
| 6 | 引文核验 | 核验表（SUPPORTED / MISCHARACTERIZED / MISSING） | `citation-check` | `nature-ref-verifier`、`nature-citation` |
| 7 | 图表与统计 | `figures/`（矢量+300dpi） | `nature-figure` | `paper-writing-skill` figure_synthesis、`nature-statistics` |
| 8 | 对抗审稿 | `review.md`（结构化审稿单） | `academic-paper-reviewer` | `PaperSpine` reviewer agents、`nature-reviewer`、paper-writing red_team |
| 9 | 返修与回复 | 修订稿 + `response.md` | `nature-response`、academic-paper revision_coach | — |
| 10 | 交付与转化 | 投稿包 / PPT / 专利 / 译文 | `nature-paper2ppt`、`nature-paper-to-patent`、`nature-paper-trans` | `cell-submission`、`cell-reviewer-response`、docx/xlsx/pptx 技能 |
| 11 | 汇报（可选） | `.pptx` 汇报稿 | `nature-paper2ppt`、`nature-image2ppt` | `sci-brain/write-slides` |
| — | 元 | 维护本技能 | `skill-creator` | — |

## 二·五、十环节制（Codex 科研工作流）

用户要求走完整科研流程时，加载 [`modules/codex-research-workflow/SKILL.md`](modules/codex-research-workflow/SKILL.md)：

| 环 | 名称 | 默认入口 | 与十二站制的对应 |
|---|---|---|---|
| ① | 选题 | `cell-suite/cell-brainstorm` | 站 0（补强：证据驱动五选题；要对抗辩论 + 定量 gap 走 `research-cycle`） |
| ② | 检索 | `nature-skills/nature-academic-search` | 站 1 |
| ③ | 综述 | `cell-suite/cell-review` | 站 2（补强：≥30 篇硬门槛 + Word 交付） |
| ④ | 统筹 | `codex-research-workflow` + `academic-research-skills/academic-pipeline` | 站 0 + 站 3 |
| ⑤ | 统计 | `nature-skills/nature-statistics` | 站 7 的一半 |
| ⑥ | 绘图 | `nature-skills/nature-figure`（可编辑矢量：`cell-suite/cell_su7`） | 站 7 的另一半 |
| ⑦ | 写作 | `nature-skills/nature-writing` | 站 4 |
| ⑧ | 润色 | `humanized-writing`（中）/ `cell-suite/cell-manuscript-editing`（英） | 站 5 |
| ⑨ | 投稿 | `cell-suite/cell-submission` + `nature-skills/nature-reviewer` | 站 8 + 站 9 + 站 10 |
| ⑩ | 汇报 | `nature-skills/nature-paper2ppt` | 站 11 |

**跨环节只传五项**：已确认产物路径、硬约束、未决事实、下一环启动条件、当前/下一环编号。
完成上一环 ≠ 授权推进下一环；「未决事实」非空先问清再动。

## 三、按意图直达（路由表）

| 用户说…… | 去哪 |
|---|---|
| **按科研工作流走 / 从选题到投稿 / 十环节** | **`modules/codex-research-workflow/SKILL.md`**（统筹层） |
| 我只有一个模糊方向 / 帮我把想法磨成题目 | `modules/cell-suite/cell-brainstorm/SKILL.md`（或 `modules/sci-brain/brainstorm-ideas/SKILL.md`） |
| 对抗辩论找 gap / scientific brainstorming / research cycle / 这个方向到底有没有人做过 | `modules/research-cycle/SKILL.md`（S2 定量分级 + 三智能体对抗 + GO/REVISE/KILL） |
| 复现一篇论文 / 代码复现 / reproduce / 这篇没给代码 | `modules/phd-skills/reproduce/SKILL.md`（7 阶段）+ `paper-verification/SKILL.md`（数值/公式核验），分工见 `modules/phd-skills/_MODULE_GUIDE.md` |
| 论文里的数字和代码对不上 / 公式和实现不一致 | `modules/phd-skills/paper-verification/SKILL.md` |
| 题目定了，帮我排研究计划 | `modules/cell-suite/cell-plan/SKILL.md` |
| 建一个能引用的文献知识库 / 自动跑研究循环 | `modules/sci-brain/survey/SKILL.md`、`modules/sci-brain/autoresearch/SKILL.md` |
| 帮我写论文 / 从课题到成稿 | 走完整 12 站，先看 `modules/academic-research-skills/academic-pipeline/SKILL.md` |
| 做文献综述 / 调研一个方向 / 找 gap | `modules/literature-survey-skill/SKILL.md`（四阶段）+ `paper-qa`；要顶刊 Word 综述走 `modules/cell-suite/cell-review/SKILL.md` |
| 就这批 PDF 提问 / 找共识与矛盾 | `modules/paper-qa/SKILL.md`（`pqa ask`） |
| 论文结构散 / 讲不出故事 / 大修重排 | `modules/paperspine/SKILL.md`（motivation 驱动骨架） |
| 起草某个章节（摘要/引言/方法/结论） | `modules/nature-skills/nature-writing/SKILL.md` 或 `paper-writing-skill` |
| 这段太 AI 了 / 去 AI 味 / 润色 | `modules/humanized-writing/SKILL.md`（中文语感与写作模式）/ `modules/human-voice/SKILL.md`（**改已有 AI 稿的结构级手术 + 量化自查**，两者分工见 `modules/human-voice/_MODULE_GUIDE.md`）/ `en-humanizer.md`（英文） |
| 检查参考文献是否造假 / 引用是否对得上 | `modules/citation-check/SKILL.md` |
| 画论文配图 / Nature 级多面板图 | `modules/nature-skills/nature-figure/SKILL.md` |
| 要可编辑的矢量图 / PPT 图 / Illustrator 图 | `modules/cell-suite/cell_su7/SKILL.md`（**需付费额度，扣费前须授权**）；`cell_su8` 为扭曲/马赛克时升级版 |
| 要 Python/MATLAB 绘图代码 / 复现参考图再换自己数据 | `modules/cell-suite/cell-visualization-code/`、`modules/cell-suite/cell-data-figure/` |
| 投稿前模拟审稿 / 找弱点 | `modules/academic-research-skills/academic-paper-reviewer/SKILL.md`、`modules/nature-skills/nature-reviewer/SKILL.md` |
| 写 rebuttal / 回复审稿人 | `modules/nature-skills/nature-response/SKILL.md`（中文流程）、`modules/cell-suite/cell-reviewer-response/SKILL.md`（两阶段 Word 回复） |
| 整理投稿包 / cover letter / 期刊材料 | `modules/cell-suite/cell-submission/SKILL.md` |
| 论文转 PPT / 转专利 / 中英翻译 | `nature-paper2ppt` / `nature-paper-to-patent` / `nature-paper-trans` |
| 做学术汇报 slides（Typst） | `modules/sci-brain/write-slides/SKILL.md` |
| 改进这个技能本身 | `modules/skill-creator/SKILL.md` |

## 四、全局红线（跨模块一律遵守）

1. **证据绑定**：所有数值、指标、p 值、引文、图表必须来自真实材料；**禁止编造**。上游共同底线：
   `PaperSpine` 的「Never invent data, metrics, p-values, citations…」、`academic-pipeline` 的 claim 审计、
   `paper-writing-skill` 的证据优先，都是同一条。
2. **引文必经核验**：写进论文的每条引用都要能追到真实来源（URL/DOI/全文）；
   `citation-check` 或 `nature-ref-verifier` 核过才算数，未核验的标注「未核验」而非默认可信。
3. **去 AI 味不等于过检测器**：`humanized-writing` 只改善读感，不承诺任何检测结果，禁止注水/故意错字。
4. **改写保真**：润色不改事实、数字、引文、来源；不把推测写成确定；不替作者编经历。
5. **图表先引后出**：正文未引用的图为「孤儿图」，删除或补引用；统计口径与 n 必须标注。
6. **原目录只读**：`humanized-writing` 原目录不改；本技能内部改动只落在本技能目录内。
7. **付费授权前置**（v2 新增）：`cell-suite` 中的 `cell_su7`/`cell_su8`/`cell-cns-figure` 走外部额度制付费服务。
   **提交任何付费请求前必须先告知用户预计消耗的额度并取得明确同意**；无 API Key 或余额不足时
   降级到 `nature-figure` 本地绘图，不得静默扣费，也不得虚称已生成。
8. **完成 ≠ 授权**：完成某一环不自动授权推进下一环、上传文件、付费或正式投稿。

## 五、典型组合用法

- **从零写一篇投 Nature 系期刊的论文**：
  `paper-writing brainstorm（0）→ literature-survey（1–2）→ PaperSpine 骨架（3）→ nature-writing 起草（4）
  → humanized-writing + nature-polishing（5）→ citation-check + nature-ref-verifier（6）→ nature-figure（7）
  → academic-paper-reviewer 模拟审（8）→ nature-response（9）→ nature-paper2ppt（10）`。
- **走完整的十环节科研工作流**（v2）：
  `cell-brainstorm（①选题）→ nature-academic-search（②检索）→ cell-review（③综述）
  → codex-research-workflow 交接（④统筹）→ nature-statistics（⑤统计）→ nature-figure（⑥绘图）
  → nature-writing（⑦写作）→ humanized-writing / cell-manuscript-editing（⑧润色）
  → cell-submission + nature-reviewer（⑨投稿）→ nature-paper2ppt（⑩汇报）`。
- **给一批既有 PDF 做综述**：`papi` 建库 → `pqa ask`（共识/冲突/缺口）→ `literature-survey` 综合 → 出综述稿。
- **要一篇能投的顶刊 Word 综述**：`sci-brain/survey` 或 `how-to-download-ref` 建库 → `cell-review` 出 `review.docx`。
- **只有模糊想法，要磨成可做的题目**：`cell-brainstorm`（五题论证稿）或 `sci-brain/brainstorm-ideas`（苏格拉底追问）；
  要「先吵一架再决定」就走 `research-cycle`（对抗辩论 + S2 gap 定量 + GO/REVISE/KILL）。
- **复现一篇论文并核对它的数字**：`phd-skills/reproduce`（7 阶段到 `results.md`）→
  `phd-skills/paper-verification`（数字追源、公式-代码对齐）；论文自身引文真伪另走 `citation-check`。
- **把参考图重建成可编辑 PPT/Illustrator 图形**：`cell_su7`（**先确认额度与授权**）→ 交付 SVG/PPTX/AI 源文件。
- **只救急润色**：`humanized-writing`（中文）/ `en-humanizer.md`（英文）+ `check_prose.py` 自查。
- **投稿返修**：`academic-paper-reviewer` 复现审稿意见 → `revision_coach` 逐条改 → `nature-response` 写回复信。

## 六、自查脚本

去 AI 味长稿保存后：

```bash
python3 modules/humanized-writing/scripts/check_prose.py 稿件路径
```

脚本只报告形状（黑话/翻案句/破折号/Tier-1 高频词等），是否真有问题要回材料判断。

上游各模块自带的机械校验脚本（Python 3.10+，标准库即可）：

| 脚本 | 用途 |
|---|---|
| `modules/cell-suite/cell-review/scripts/delivery_gate.py` | 综述交付门槛（引用数、Word 可编辑性、重复项） |
| `modules/cell-suite/cell-plan/scripts/check_plan.py` / `check_delivery.py` | 研究计划结构与交付完整性 |
| `modules/cell-suite/cell-brainstorm/scripts/quality_gate.py` | 选题论证稿质量门禁 |
| `modules/sci-brain/how-to-download-ref/helpers/resolve_kb.py` | 定位项目知识库 `.knowledge/` |

**脚本通过 ≠ 科学正确**：脚本只查结构、编号、字段与计数，学术判断必须回到材料。

## 七、来源与许可

十五个上游项目的仓库地址、许可与取舍说明见 [`SOURCES.md`](SOURCES.md)；整体结构与使用说明见 [`README.md`](README.md)。
上游均以**只读副本**形式归档于 `modules/`，不含图片/评测等大体积资源；需要上游完整仓库时按 `SOURCES.md` 的地址重新拉取。
（例外：`modules/cell-suite/` 因清理了上游推广话术而不再逐字节一致，规则见其 `_LOCAL_POLICY.md`。）

本仓库采用**逐模块许可**：顶层 MIT 只覆盖本仓库自写内容（含 `modules/codex-research-workflow/`、
`modules/humanized-writing/`、`scripts/`）；上游模块保留各自许可，以各模块目录下 `LICENSE` 为准。
**`modules/academic-research-skills/` 为 CC BY-NC 4.0，仅限非商业用途** —— 商业使用前请移除该模块。
