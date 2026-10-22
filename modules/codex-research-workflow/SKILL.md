---
name: codex-research-workflow
description: "Codex 科研十环节统筹层：把「选题 → 检索 → 综述 → 统筹 → 统计 → 绘图 → 写作 → 润色 → 投稿 → 汇报」十个环节映射到 lunwenn-skill 内各上游模块，给出每个环节的默认入口、备选入口、输入产物、出口验收与切换条件。用户说「按科研工作流走」「从选题到投稿」「我要做一篇论文，帮我按流程来」「十环节」「科研全流程」「Codex 工作流」时使用本模块。它是编排层，不含写作规则本身。"
---

# Codex 科研十环节 · 统筹层

本模块只做**调度**：告诉模型「现在该进哪个门、拿什么输入、交什么产物、什么条件下才能推进到下一门」。
它不含任何写作规范——每个环节的具体规则一律去对应上游模块读。

## 零、为什么要有这一层

原 `lunwenn-skill` 的十二站流水线按「论文产物」排序（立项→写作→润色→核验→投稿）。
这一层按**科研工作的真实决策顺序**重排为十环，并把「选题」和「可编辑绘图」两个原本缺失的环节补进来：

```
① 选题          → ② 检索        → ③ 综述      → ④ 统筹
                                    ↓
⑩ 汇报 ← ⑨ 投稿 ← ⑧ 润色 ← ⑦ 写作 ← ⑥ 绘图 ← ⑤ 统计
```

- ④ 统筹是**横切**：它不产内容，它决定其余九环的顺序与门槛。
- ⑤ 统计 → ⑥ 绘图 → ⑦ 写作 是**数据前置**关系：图和统计口径没定，写作就是在编。
- 与十二站流水线的对应：①=站0，②=站1，③=站2，④=站0+3，⑤+⑥=站7，⑦=站4，⑧=站5，⑨=站8+9，⑩=站10。

## 一、十环路由表（默认入口 = 首选）

| 环 | 名称 | 默认入口 | 备选入口 | 主产物 | 出口验收 |
|---|---|---|---|---|---|
| ① | 选题 | `modules/cell-suite/cell-brainstorm/SKILL.md` | `modules/sci-brain/brainstorm-ideas/SKILL.md`、`modules/paper-writing-skill/brainstorming_guide.md` | 选题论证稿（5 个候选 + 研究增量） | 每个选题都有「研究依据／拟研究内容／研究方案／可行性与限制」四段；创新性写成**相对已有文献的具体增量**，不是「首次」 |
| ② | 检索 | `modules/nature-skills/nature-academic-search/SKILL.md` | `modules/sci-brain/how-to-download-ref/SKILL.md`、`modules/nature-skills/nature-downloader/SKILL.md` | 文献清单 + DOI/PMID + `.bib` | 每条文献能追到 DOI 或稳定标识；入库条目进 `<project>/.knowledge/references.bib` |
| ③ | 综述 | `modules/cell-suite/cell-review/SKILL.md` | `modules/literature-survey-skill/SKILL.md`、`modules/nature-skills/nature-reader/SKILL.md` | `review.docx`（可编辑 Word） | ① 正文实际引用 ≥30 篇真实、去重、已核验文献；② 每条都核过「存在性 + 与所引内容一致性」；③ 唯一交付物是 Word，不是 md/pdf 清单 |
| ④ | 统筹 | **本模块** + `modules/academic-research-skills/academic-pipeline/SKILL.md` | `modules/cell-suite/cell-plan/SKILL.md`（题目已定、要排执行路线时） | 阶段计划 + 交接单 | 每一环的**入口材料、出口产物、验收标准、未决问题**四项写清；完成上一环 ≠ 授权下一环 |
| ⑤ | 统计 | `modules/nature-skills/nature-statistics/SKILL.md` | `modules/cell-suite/cell-visualization-code/SKILL.md`（要真算时） | 统计方法小节 + 图注统计 | 独立实验单元才是 `n`；效应量 + 置信区间 + 样本量 + 检验定义齐；缺信息写 `AUTHOR_INPUT_NEEDED`，**不编** n 和 p |
| ⑥ | 绘图 | `modules/nature-skills/nature-figure/SKILL.md`（投稿级常规图） | `modules/cell-suite/cell-data-figure/`（复现参考图后换自己数据）、`cell_su7`/`cell-cns-figure`（**要可编辑矢量图**） | `figures/` 矢量 + 300dpi 位图 | 图先被正文引用（否则是孤儿图）；坐标轴/单位/误差棒/n/统计标注齐全；可编辑图必须交付 SVG/PPTX/AI 源文件 |
| ⑦ | 写作 | `modules/nature-skills/nature-writing/SKILL.md` | `modules/sci-brain/write-paper/SKILL.md`、`modules/paper-writing-skill/SKILL.md` | `paper.tex/.md/.docx` | 先有论证骨架（`spine.md`）再落笔；每段有明确 claim；所有数字引文来自真实材料 |
| ⑧ | 润色 | `modules/humanized-writing/SKILL.md`（中文去 AI 味） | `modules/nature-skills/nature-polishing/SKILL.md`、`modules/cell-suite/cell-manuscript-editing/SKILL.md`（英文深度润色） | 润色稿 | 不改事实/数字/引文/来源；不把推测写成确定；不承诺过任何检测器 |
| ⑨ | 投稿 | `modules/cell-suite/cell-submission/SKILL.md`（打包）+ `modules/nature-skills/nature-reviewer/SKILL.md`（预审） | `modules/nature-skills/nature-response/SKILL.md`（返修回复）、`modules/cell-suite/cell-reviewer-response/SKILL.md` | 投稿包 + `response.md` | cover letter / 声明 / 数据可用性齐；正文定稿后才打包；返修逐条对应审稿意见 |
| ⑩ | 汇报 | `modules/nature-skills/nature-paper2ppt/SKILL.md` | `modules/nature-skills/nature-image2ppt/SKILL.md`、`modules/sci-brain/write-slides/SKILL.md` | `.pptx` 汇报稿 | 图能单独抽出；每页一个论点；结论与正文一致 |

## 二、④ 统筹的交接单格式

跨环只传这五项，**不多不少**：

```
## 阶段交接单
- 当前环：<①~⑩>  下一环：<>
- 已确认产物：<绝对路径 + 版本/日期>
- 硬约束：<期刊、字数、格式、禁区>
- 未决事实：<需要作者确认的点，或 "无">
- 下一环启动条件：<什么条件满足才允许推进>
```

**铁律**：完成上一环不自动授权下一环；跨环推进前若「未决事实」非空，先问清再动。

## 三、环节切换的强制门槛

| 从 | 到 | 必须先满足 |
|---|---|---|
| ①→② | 选题 | 题目已锁定（含研究增量陈述），不是「我还不知道做什么」 |
| ②→③ | 综述 | 文献已入库并带稳定标识；**没读过原文的文献不得计入引用数** |
| ③→⑦ | 写作 | 综述里的争议点与 gap 已定位；论证骨架已定 |
| ④→⑤⑥ | 统计/绘图 | 数据真实存在；分析口径与 `n` 已定；图的数据来源可追 |
| ⑥→⑦ | 写作 | 图已定稿并**已在正文被引用**；孤儿图清零 |
| ⑦→⑧ | 润色 | 正文完整成稿，不是提纲或片段 |
| ⑧→⑨ | 投稿 | 引文已核验（`modules/citation-check/`）；无编造引用 |
| ⑨→⑩ | 汇报 | 投稿包完成或至少正文定稿 |

## 四、五个高风险环节的额外红线

1. **绘图（⑥）**：`cell_su7` / `cell_su8` / `cell-cns-figure` 依赖**外部付费服务**（额度制、需 API Key、cell_su7 每张约 1 额度、cell_su8 每张 3 额度、cell-cns-figure 分 20/45 额度两档且 2 号需一次性邀请码）。
   **扣费前必须先取得用户对具体额度的明确授权**，并如实告知预计消耗；余额不足时停止新任务。
   无额度/无 Key 时降级到 `nature-figure`（本地 Python/R 绘图，不扣费），不要卡死。
2. **PPT 原生编辑**：`cell-ppt-edited` 需 **Windows 桌面版 Microsoft PowerPoint**（不支持 WPS / macOS），且它是独立插件，需另装 `cell_ppt_edited` 引擎。条件不满足就用 `nature-paper2ppt` 生成静态汇报稿。
3. **综述（③）30 篇门槛**：这是上游的**最低交付要求**，不是质量分。凑不满就如实标注数量的未完成稿，**不得编造文献或把门槛调低后宣称完成**。
4. **选题（①）**：单模型、单条证据链。禁止包装成「专家共识」「独立评审」；没检索到不等于全球首创。
5. **投稿（⑨）**：目标期刊的格式与材料要求以**期刊官网当期要求**为准，不以本技能内的模板为最终依据。

## 五、加载纪律

- 本模块**只在用户明确要走全流程 / 某环缺失需要补位**时读。
- 单环任务：直接读那一环的默认入口文件，**不要**先读本模块走形式。
- 同一时刻只打开当前环需要的入口文件 + 其 `references/` 里被点名的部分；大目录（`cell-review/`、`cell-brainstorm/`）按需摘取，不要整目录塞进上下文。
- 上游模块自带脚本（如 `cell-review/scripts/delivery_gate.py`、`cell-plan/scripts/check_plan.py`）在导出前跑一次做机械校验；**脚本通过 ≠ 科学正确**，判断仍回到材料。

## 六、入口速查

| 想干什么 | 直接读 |
|---|---|
| 我只有一个模糊方向 | `modules/cell-suite/cell-brainstorm/SKILL.md` |
| 我要查高质量文献 | `modules/nature-skills/nature-academic-search/SKILL.md` |
| 我要写一篇综述 | `modules/cell-suite/cell-review/SKILL.md` |
| 题目定了，怎么做 | `modules/cell-suite/cell-plan/SKILL.md` |
| 我要统计审查 | `modules/nature-skills/nature-statistics/SKILL.md` |
| 我要投稿级配图 | `modules/nature-skills/nature-figure/SKILL.md` |
| 我要可编辑矢量图（可付费） | `modules/cell-suite/cell_su7/SKILL.md` |
| 我要写论文正文 | `modules/nature-skills/nature-writing/SKILL.md` |
| 我要去 AI 味 | `modules/humanized-writing/SKILL.md` |
| 我要英文深度润色 | `modules/cell-suite/cell-manuscript-editing/SKILL.md` |
| 我要模拟审稿 | `modules/nature-skills/nature-reviewer/SKILL.md` |
| 我要投稿包 | `modules/cell-suite/cell-submission/SKILL.md` |
| 我要回复审稿人 | `modules/nature-skills/nature-response/SKILL.md` |
| 我要做汇报 PPT | `modules/nature-skills/nature-paper2ppt/SKILL.md` |
| 我要做综述/论文的自动检索循环 | `modules/sci-brain/autoresearch/SKILL.md` |
