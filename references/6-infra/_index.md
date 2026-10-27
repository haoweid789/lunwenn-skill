# 6 基础设施族

不是工作流，是**被上面五个族调用的共享资产**。只有两种情况需要单独读这里：① 要查期刊硬约束；② 要操作本地论文库。

## 1. 写作核心规范 `core/` 与 `journal-formats/`

**这是整个包最该先读的东西**，也是原来 19 个孤儿模块真正的落脚点。

### `core/` 十一份共享定义

| 文件 | 解决什么 |
|---|---|
| `nature-abstract.md` | 摘要怎么压：发现为中心、论断分级、选择性给数字、领域级落点 |
| `nature-introduction.md` | 引言漏斗：问题漏斗、精确知识缺口、文献张力、问题优先的新颖性 |
| `nature-results-discussion.md` | 结果怎么逐级升级论断、局部解释的证据边界、讨论综合 |
| `discussion-argument-language.md` | 讨论的功能排序、反漏斗控制、按证据校准语气、声称专属局限、不确定性驱动的未来工作 |
| `main-text-discipline.md` | 结果放哪、正文压缩、修订增量控制、图注与 SI 分配、重复声称检查 |
| `paper-type-taxonomy.md` | 论文类型分类，决定套哪套检查表 |
| `reader-workflow.md` | 精读流程 |
| `terminology-ledger.md` | **术语台账**：全文术语一致性 |
| `ethics.md` / `research-compliance.md` | 伦理与合规，带适用性门禁 |
| `consistency-sweep.md` + `scripts/check_consistency.py` | 一致性扫描脚本（可跑） |

### `journal-formats/` 三本刊的硬约束

`nature.md` · `nat-comms.md` · `nature-machine-intelligence.md` —— 字数、图表数、初始投稿文件、数据/代码义务、生产要求。

> 只引这里写明的数字。其他期刊一律说「需查该刊 Guide for Authors」。**不要用一本刊的限额套另一本**——这是原说明里明写的禁令。

## 2. 本地论文库 `paperpipe/`

**精华**：`papi` 命令族，把本地论文库当数据库用。

| 要做什么 | 用哪条 |
|---|---|
| 查这篇在不在库里 | `papi` |
| 检索（成本递增式升级） | `papi` — 从最便宜的全文匹配开始，不够才升级 |
| 加 arXiv 论文 | `papi` |
| 导出上下文给模型 | `papi` |
| 就论文提问（RAG） | `sub/papi-ask` — PaperQA2 或 LEANN，答案带引文 |
| 比较方案/方法选哪个 | `sub/papi-compare` |
| 写项目笔记 | `sub/papi-curate` |
| 引用原文摘录 | `sub/papi-ground` — 强制贴着原文，不许改写 |
| 接入项目（CLAUDE.md/AGENTS.md） | `sub/papi-init` |
| 校验代码是否与论文一致 | `sub/papi-verify` — 查方程、算法逐条对 |

**合并说明**：原 6 个 `papi-*` 是同一套 CLI 的六个固定场景，各自 ~1 KB。已收在 `sub/`，由 `paperpipe/SKILL.md` 的决策树分流。**不要当成六个独立技能**。

## 3. 复现与记忆

### `reproduce/` 论文复现
**精华**：从 arXiv URL 一路到复现实验，专门处理四种残缺：缺官方代码、缺训练脚本、缺超参、私有数据。每种残缺有对应的替代路径。

### `style-memory/` 学你的文风
**精华**：从 Zotero / 本地 PDF 文件夹 / Google Scholar 三个入口提取你的写作特征（句长、常用转折、人称、论证节奏），让后续写作说你的语言而不是通用学术腔。

### `create-advisor/` 造导师画像
**精华**：从会话历史生成具名 advisor 的四段画像：背景 / 发文来源 / 语气 / 思维风格。用来看"如果是他会怎么问"。

### `chat-history/` + `dialog-analysis/` 会话资产
- `chat-history/`：导出原始会话为忠实转录或 Typst+PDF 田野笔记
- `dialog-analysis/`：按六个学术维度分析你的提问模式（你在哪些环节问得浅）

### `kb-build/` + `kb-fetch/` 知识库
- `kb-fetch/`：arXiv ID 或 DOI → 元数据 + PDF + 全文 → 更新 `references.bib` 与 `INDEX.md`
- `kb-build/`：已筛选的论文清单 → `references.bib` + `INDEX.md` + `NOTES.md` 三件套

**顺序**：先 fetch 再 build。反过来会缺全文。

## 淘汱的两个

| 原模块 | 为什么 |
|---|---|
| `cell` | 纯路由壳，只列了 Cell 系列 11 个成员。新母 `SKILL.md` 的路由表覆盖全部 48 个，比它全 |
| `skill-creator` | 与本机顶层 `~/.workbuddy/skills/skill-creator` 是同一份，包内不需要第二份 |
| `nature-shared/SKILL.md` | 它自己写明"不要当独立工作流调用"，本体已拆到 `core/` 与 `journal-formats/` |

## 坑

- **`core/` 里的文件要按需读，不要预载**。11 份加起来不小，且多数任务只需要其中 1–2 份。原 `nature-shared` 的说明里就明写「Load the exact referenced file; do not preload the whole package」。
- `check_consistency.py` 是需要环境依赖的脚本，跑之前先看 `tests/` 里的用例确认能跑。
- `paperpipe` 的检索是**成本感知**的：从便宜的全文匹配开始，逐步升级到向量检索。别一上来就用最贵的那档。
