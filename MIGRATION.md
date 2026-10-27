# lunwenn 77 模块整理表

原包：`~/.workbuddy/skills/lunwenn-skill`（77 个 SKILL.md / 980 KB / 1793 文件 / 21 MB）
新包：`lunwenn-v2`（1 个入口 + 6 族 + 64 份模块说明 / 1418 文件 / 16 MB）
整理日期：2026-10-27

## 判定说明

| 判定 | 含义 |
|---|---|
| **主干** | 该能力的默认入口，别人问这类事就指到它 |
| **保留** | 与主干是不同流派/不同深度，两个都有价值，按场景选 |
| **合并** | 内容被另一个模块吸收，原目录不再复制，精华写进了 `_index.md` |
| **淘汰** | 无独立价值（纯路由壳 / 与外部重复 / 单参数变体 / 空壳插件说明） |

## 命名约定（重要）

参考模块的原始定义文件统一命名为 **`MODULE.md`**，不再叫 `SKILL.md`。

原因：WorkBuddy 会**递归扫描** `skills/` 下的所有 `SKILL.md`。原包里 77 个模块共用这个文件名，所以装进去就等于 77 个独立 skill 同时注册——这正是"77 个孤儿模块"的成因。改名后全包只有顶层 1 个 `SKILL.md`，64 份模块说明退化成纯文档，只有被母文件路由到时才读。

各模块自己带的 `README.md` 保持原名未动（25 个模块有），它们讲的是"这个模块怎么用"，与 `MODULE.md`（工作流本体）是两份东西。


---

## 0 编排（5 → 4）

| 原模块 | 体积 | 精华 | 判定 | 去向 |
|---|---|---|---|---|
| `academic-research-skills/academic-pipeline` | 59 KB / 30 | **十阶段状态机 + 适应性检查点**：research→write→integrity→review→revise→re-review→re-revise→final→finalize，含中途接入协议与修订环管理。中断可续是它最大的价值 | 主干 | `0-orchestration/pipeline/` |
| `research-cycle` | 16 KB / 3 | **七阶段研究循环**：文献综述与对抗式查新 → 创新设计 → 基线复现 → 创新实现 → 实验验证 → 分析迭代 → 论文写作。适合「做研究」而不是「写论文」 | 主干 | `0-orchestration/research-cycle/` |
| `sci-brain/autoresearch` | 6 KB / 20 | **密封校验器 + 评分式尝试循环**：先定可自动判分的 validator，再让 agent 循环试到过线。适合有明确可测目标的长跑 | 保留 | `0-orchestration/autoresearch/` |
| `sci-brain/how-to-flow` | 12 KB / 2 | **decide–simulate–learn–backjump**：一个硬目标直解不通时的自主搜索循环，自带 preflight 门禁与终止条件 | 保留 | `0-orchestration/flow/` |
| `codex-research-workflow` | 9.7 KB / 2 | **十环节路由表 + 交接单格式 + 环节切换的强制门槛 + 五个高风险环节红线** | **合并** | 精华已写进母 `SKILL.md` 的「十环节状态机」与「阶段交接单」，原文不再复制 |

## 1 文献（13 → 10）

| 原模块 | 体积 | 精华 | 判定 | 去向 |
|---|---|---|---|---|
| `nature-skills/nature-downloader` | 24 KB / 67 | **合法全文获取的四级降级路径**：OA → 出版商 API → 机构代理域 → 浏览器兜底。67 个文件是各库真实入口与机构域名表，不是模板 | 主干 | `1-literature/downloader/` |
| `literature-survey-skill` 与 `sci-brain/survey` | 20 KB / 16 + 12 KB / 3 | 前者**四模式渐深**：intent（问清你要什么）→ triage（这堆里有什么）→ deepen（这篇到底说了啥）→ synthesize（连起来是什么）；后者**主题调研成知识库**。同叫 survey 但是两种东西 | 保留两者 | `1-literature/survey/` + `1-literature/survey/topic-survey/` |
| `academic-research-skills/deep-research` | 52 KB / 53 | **13 智能体 / 8 模式**，其中「三路扫描 WHY-HOW-WHAT」是别处没有的视角；带 deep-research → academic-paper 的交接协议 | 主干 | `1-literature/deep-research/` |
| `academic-research-skills/sr-screener` | 34 KB / 25 | **把 PROSPERO 协议变成可执行纳排规则**，两轮筛选（题目摘要 → 全文）带双人一致性判定。做系统综述不可替代 | 主干 | `1-literature/systematic-review/` |
| `paper-qa` | 3.4 KB / 10 | **PaperQA2 本地 RAG**（CLI 名 `pqa`）：对一整个 PDF 目录提问，答案带页码引文，能梳出共识/分歧/证据缺口 | 保留 | `1-literature/paper-qa/` |
| `nature-skills/nature-paper-card` | 8.4 KB / 21 | **单篇精读卡**：方法拆解 + 从实验到论断的证据链 + 局限 + 可延伸想法，四段固定 | 主干 | `1-literature/paper-card/` |
| `nature-skills/nature-reader` | 3.9 KB / 20 | **图文表公式对齐的双语精读**，问答可溯源到原文位置 | 保留 | `1-literature/reader/` |
| `nature-skills/nature-paper-trans` | 8.6 KB / 9 | **逐页译成保留版式的中文图片型 PDF**，分栏/图表/公式尽量不动。定位明确：只做阅读版，不做可编辑重建 | 保留 | `1-literature/translate/` |
| `nature-skills/nature-paper-xray` | 6.2 KB / 7 | **论文透视**：先判论文类型再套对应检查表，评估证据强度、找过度声称。论文转专利时的拆分前置就靠它 | 保留 | `1-literature/xray/` |
| `nature-skills/nature-academic-search` | 3.6 KB / 53 | 文献检索 + MeSH 策略 + 引文影响审计 | **合并** | 检索并入 `survey/`，引文核验并入 `3-review/ref-verifier/` |
| `nature-skills/nature-citation` | 3.1 KB / 15 | 找 Nature/CNS 系列文献支撑论断 + 论断-来源映射 | **合并** | 并入 `3-review/citation-check/`（它的双通过门禁更严） |
| `phd-skills/paper-verification` | 5 KB / 1 | 论文核验的三个维度 | **合并** | 并入 `3-review/citation-check/` |
| `nature-skills/nature-shared`（SKILL.md 部分） | 2.1 KB | 它本身不是工作流，是共享参考包的说明 | **淘汰外壳** | `core/` 与 `journal-formats/` 原样搬到 `6-infra/`，SKILL.md 不再保留 |

## 2 写作（11 → 10）

| 原模块 | 体积 | 精华 | 判定 | 去向 |
|---|---|---|---|---|
| `nature-skills/nature-writing` | 8.3 KB / 77 | **从作者给的证据起草或重构章节**，77 个文件是 Nature 语料里拆出来的章节范式。默认起草入口 | 主干 | `2-writing/manuscript/` |
| `academic-research-skills/academic-paper` | 65 KB / 63 | **12 智能体 / 11 模式 / 8 阶段**，最重也最全；含 Generator-Evaluator 契约协议与修订补丁协议 | 保留（重装用） | `2-writing/paper-pipeline/` |
| `paper-writing-skill` | 34 KB / 33 | **编辑纪律流**：结构化头脑风暴是它的核心，加上「强制文风审计门禁」——每一处 tex 改动都要过审。这套门禁比别家硬 | 保留 | `2-writing/editorial/` |
| `sci-brain/write-paper` | 22 KB / 3 | **Martinis 七段模板** + 图规则 + 记号规则 + 句级规则 + 投稿前清单。结构最清晰，适合从零搭骨架 | 保留 | `2-writing/martinis/` |
| `nature-skills/nature-polishing` | 6.1 KB / 33 | **保事实、保术语、保证据边界**的润色与翻译，附带 LaTeX 版式修复 | 主干 | `2-writing/polish/` |
| `human-voice` | 9.1 KB / 14 | **五维审计 + 体裁浓度表**：人味的浓度随体裁变（论文 vs 公众号 vs 小说），不是一套标准。附自检三件套 | 主干 | `2-writing/humanize/` |
| `sci-brain/how-to-technical-writing` | 10 KB / 2 | **句级与段级**技术写作规则 + 「hunt table」（该找哪些坏毛病）。最轻量，只改文字不动结构 | 保留 | `2-writing/technical-prose/` |
| `sci-brain/write-slides` | 6 KB / 1 | Typst + Touying 可编译学术幻灯片 | 保留 | `2-writing/slides/` |
| `paperspine` | 23 KB / 167 | **研究-写-审-交付在同一任务内闭环**，可同任务回改，167 个文件是模板与校验资产 | 保留 | `2-writing/paperspine/` |
| `cell-suite/cell-manuscript-editing` | 8.3 KB / 15 | 英文论文深度润色，独有价值是一张「**不可改变的事实**」清单——润色时哪些东西绝对不许动 | 保留 | `2-writing/manuscript-editing/` |
| `humanized-writing` | 8.7 KB / 7 | 与 `human-voice` 同题，四场景分法 | **淘汰** | 内容被 `human-voice` 的五维审计 + 浓度表覆盖，后者更深且有参考文件 |

## 3 审稿与核验（9 → 8）

| 原模块 | 体积 | 精华 | 判定 | 去向 |
|---|---|---|---|---|
| `nature-skills/nature-reviewer` | 13 KB / 21 | **Nature 视角的模拟审稿**：significance / validity / major-minor 三段，配来源层级与红线 | 主干 | `3-review/peer-review/` |
| `sci-brain/review-paper` | 27 KB / 2 | **九准则 + 严重度分级 + 事实与文献核验 + 期刊契合度**，比上一项多出「核验」和「期刊fit」两阶段 | 主干 | `3-review/review-paper/` |
| `academic-research-skills/academic-paper-reviewer` | 45 KB / 28 | **五座席评审团**：Journal-Fit + 3 个同行角色 + Devil's Advocate，含字段专属标准与校准模式 | 保留（要挑刺时） | `3-review/panel/` |
| `nature-skills/nature-response` | 6 KB / 38 | 逐点回应审稿意见，区分「能靠解释解决」与「必须补证据」 | 主干 | `3-review/response/` |
| `cell-suite/cell-reviewer-response` | 15 KB / 8 | **两阶段 Word 交付**：先出一份标红待办的 Word，材料齐了再出正式逐点回复 + 学术 Humanizer | 保留（中文 SCI） | `3-review/response-word/` |
| `citation-check` | 20 KB / 4 | **视觉 + 搜索双通过门禁**：论断抽取 → 源权威性分级 → 数字精度规则 → 平局裁决。最严的一套 | 主干 | `3-review/citation-check/` |
| `nature-skills/nature-ref-verifier` | 9.8 KB / 6 | **多来源交叉验证**参考文献真伪，56 条实测过的工作流，带已知局限说明 | 保留 | `3-review/ref-verifier/` |
| `cell-suite/cell-review` | 24 KB / 24 | **写一篇顶刊级综述文章**（不是审别人的稿）：Word 与文献数量的硬门槛 + 五步提取综合 | 保留 | `3-review/literature-review/` |

## 4 图表（10 → 8）

| 原模块 | 体积 | 精华 | 判定 | 去向 |
|---|---|---|---|---|
| `nature-skills/nature-figure` | 12 KB / 72 | Python/R 论文级图，72 个文件含期刊尺寸与样式资产 | 主干 | `4-figures/data-figure/` |
| `cell-suite/cell-data-figure` | 16 KB / 8 | **六步锁死版式**：定问题 → 锁参考 → **实际跑通参考代码** → 核验视觉一致性 → 换自己数据 → 重跑。第二步「跑通参考代码」是别家都没有的硬要求 | 主干 | `4-figures/reproduce-figure/` |
| `cell-suite/cell-visualization-code` | 7 KB / 21 | Python/MATLAB 科研可视化代码生成，只管出代码 | 保留 | `4-figures/viz-code/` |
| `cell-suite/cell_su7` | 12 KB / 44 | **图片还原成可编辑 PPT/AI**：文字保留可编辑、按路径回放绘制。覆盖约 90% 常见情况 | 主干 | `4-figures/reconstruct-su7/` |
| `nature-skills/nature-image2ppt` | 10 KB / 90 | **对象级还原**幻灯片图/截图/扫描 PDF，不是贴图 | 保留 | `4-figures/image2ppt/` |
| `nature-skills/nature-paper2ppt` | 4.3 KB / 19 | 论文 → 中文组会 PPTX，带源图与演讲备注 | 保留 | `4-figures/paper2ppt/` |
| `sci-brain/how-to-review-figure` | 10 KB / 3 | **18 条科研图评分规则 + 严重度**，用来判图好不好看 | 主干 | `4-figures/rubric/` |
| `cell-suite/cell_su8` | 14 KB / 51 | 与 su7 功能完全相同，唯一差异是「去水印更强、每张 3 额度、约 5 分钟」 | 保留（高档） | 原样保留在 `reconstruct-su7/sub/cell_su8/`，仅当 su7 结果有扭曲/马赛克时才升级 |
| `cell-suite/cell-cns-figure` | 11 KB / 61 | 同为付费图片重建入口，1 号 20 额度 / 2 号 45 额度 | **合并为参数** | 精华（额度与选档规则）写进 `4-figures/_index.md` |
| `cell-suite/cell-ppt-edited` | 4.5 KB / 1 | 一个 PPT 插件（PPT Turbo Studio）的说明，无独立工作流 | **淘汰** | 能力被 `image2ppt/` 与原生 PPT 编辑覆盖 |

## 5 投稿与合规（10 → 10）

| 原模块 | 体积 | 精华 | 判定 | 去向 |
|---|---|---|---|---|
| `cell-suite/cell-submission` | 17 KB / 8 | 六步投稿整理：清单核对 → 文件齐备 → 格式 → 声明 → 上传 → 回执 | 主干 | `5-submission/submission/` |
| `nature-skills/nature-data` | 3.9 KB / 15 | **FAIR 元数据 + 仓库选择 + 数据集引用**，数据/代码可用性声明的起草与审计 | 主干 | `5-submission/data-availability/` |
| `nature-skills/nature-proposal-writer` | 6.9 KB / 34 | **四层 QA 管线的本子撰写**，可配置研究域；开题报告/申请书通用 | 主干 | `5-submission/proposal/` |
| `nature-skills/nature-paper-to-patent` | 4.6 KB / 69 | 论文 → 中文技术交底书 → 权利要求 → 现有技术对比，分阶段门禁 | 主干 | `5-submission/patent/` |
| `nature-skills/nature-statistics` | 8.3 KB / 11 | **统计报告审查**：实验单元、重复、不确定性、检验、图注统计五处，正是审稿人最爱挑的地方 | 主干 | `5-submission/statistics/` |
| `nature-skills/nature-social-science` | 12 KB / 14 | 社科选题论证工作台：十二个判断 + **五套状态系统不合成单一分数** | 保留（社科） | `5-submission/social-science/` |
| `nature-skills/nature-experiment-log` | 6.4 KB / 11 | 标准化实验日志，实验/样品/设备三段编码规则，可接飞书与 Obsidian | 保留 | `5-submission/experiment-log/` |
| `cell-suite/cell-plan` | 17 KB / 10 | **筛 20 篇对标原始研究全文读透，直接产出任务与周计划**。不是泛泛给建议，是排出可执行顺序 | 主干 | `5-submission/plan/` |
| `cell-suite/cell-brainstorm` | 8.9 KB / 40 | **六步产出五个不同选题**，每个带最新查新、具体知识增量、最小验证路径 | 主干 | `5-submission/brainstorm/` |
| `sci-brain/brainstorm-ideas` | 32 KB / 1 | 苏格拉底式选题：先学你的背景再找值得打的问题 | 保留 | `5-submission/brainstorm-ideas/` |

## 6 基础设施（14 → 8 主干 + 6 子命令）

| 原模块 | 体积 | 精华 | 判定 | 去向 |
|---|---|---|---|---|
| `paperpipe/skills/papi` | 4.3 KB / 2 | **本地论文库 CLI**：查重、检索（成本递增式升级）、加 arXiv、导出上下文；含 MCP 工具选型 | 主干 | `6-infra/paperpipe/` |
| `paperpipe/skills/papi-{ask,compare,curate,ground,init,verify}` | 6 × ~1 KB | 六个固定场景：RAG 问答 / 方案对比 / 项目笔记 / 摘录引用 / 接入项目 / 实现校验 | **合并为子命令** | 原样收在 `6-infra/paperpipe/papi-*/`，由 `paperpipe/MODULE.md` 的决策树分流 |
| `phd-skills/reproduce` | 4.5 KB / 8 | **从 arXiv URL 到复现实验**，专门处理缺代码/缺训练脚本/缺超参/私有数据四种残缺 | 主干 | `6-infra/reproduce/` |
| `sci-brain/know-me-better` | 7.4 KB / 2 | **从你的论文学你的写作风格**（Zotero/PDF/Scholar 三入口），让 agent 说你的语言 | 主干 | `6-infra/style-memory/` |
| `sci-brain/create-advisor` | 12 KB / 1 | 从会话历史生成具名 advisor 画像：背景/发文/语气/思维风格四段 | 保留 | `6-infra/create-advisor/` |
| `sci-brain/dump-chat-history` | 8.6 KB / 7 | 导出原始会话为忠实转录或 Typst+PDF 田野笔记 | 保留 | `6-infra/chat-history/` |
| `sci-brain/how-to-analyze-dialog` | 8.8 KB / 2 | 按六个学术维度分析你的提问模式 | 保留 | `6-infra/dialog-analysis/` |
| `sci-brain/how-to-build-kb` | 4.9 KB / 1 | 论文清单 → references.bib + INDEX.md + NOTES.md 三件套 | 保留 | `6-infra/kb-build/` |
| `sci-brain/how-to-download-ref` | 12 KB / 20 | arXiv/DOI → 元数据 + PDF + 全文 → 更新 bib 与索引 | 保留 | `6-infra/kb-fetch/` |
| `nature-skills/nature-shared`（core/ 与 journal-formats/） | 11 + 3 个文件 | **全包共享的写作核心规范**：摘要结构、引言漏斗、结果-讨论语言、正文纪律、术语台账、伦理合规、三本期刊硬约束、一致性扫描脚本 | **升为基础设施** | `6-infra/core/` + `6-infra/journal-formats/` |
| `cell-suite/cell` | 4.3 KB / 3 | 纯路由壳，把 Cell 系列 11 个成员列一遍 | **淘汰** | 新母 `SKILL.md` 的路由表取代它，且更全（77 而非 11） |
| `skill-creator` | 33 KB / 18 | 造/改/评估 skill 的方法论 | **淘汰** | 与本机顶层 `skill-creator` 完全重复（同一份），包内不需要第二份 |

---

## 数字对照

| | 原包 | 新包 |
|---|---|---|
| `SKILL.md` 文件 | 77（全部会被注册成独立 skill） | **1**（只有母入口；64 份模块说明改名 `MODULE.md`，不再注册） |
| 顶层入口数 | 1，但父文件只路由到 30 个 | 1，路由覆盖全部 64 份，无孤儿 |
| 文件数 | 1793 | 1418（少的是 8 个淘汰模块，内容非重复项都搬了） |
| 体积 | 980 KB 说明 / 21 MB 含资产 | 同量级 / 16 MB |
| 淘汰 | — | 8 个：`cell`、`skill-creator`、`cell-ppt-edited`、`humanized-writing`、`nature-citation`、`nature-academic-search`、`phd-skills/paper-verification`、`nature-shared`（壳） |
| 合并 | — | 3 组：`codex-research-workflow`→母文件；`papi-*`×6→paperpipe 子命令；`cell_su8`→reconstruct 高档 / `cell-cns-figure`→写进 4-figures 的 `_index.md` |

## 保留了但要注意的两处

1. **三种论文写作流派并存**（`manuscript` / `paper-pipeline` / `editorial` / `martinis`）。这不是冗余，是四种可选的写作方法论：Nature 语料范式、12 智能体重装、编辑门禁流、七段模板。默认走 `manuscript`，用户明确要求严格纪律时换 `editorial`。
2. **付费能力集中在 4-figures**。`reconstruct-su7`（含 `sub/cell_su8`）与 `cell-cns-figure` 都是按张计额的商业 API。母 `SKILL.md` 的红线第 4 条要求先报价再执行。
