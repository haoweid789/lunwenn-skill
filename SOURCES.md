# SOURCES —— 来源、许可与收录说明

本技能由以下十五个上游项目（十四个 GitHub 开源项目 + 用户自建技能）以**只读副本**形式聚合而成。
v5 起副本不再「一个上游一个目录」，而是**按能力分到 `references/` 的六个族里**——一个上游可能被拆到多个族，
逐模块对应关系见 [`MIGRATION.md`](MIGRATION.md) 的「去向」列。
已剔除图片/截图/评测数据等大体积资源，仅保留文本类内容。需要上游完整仓库时，按下表地址重新拉取。

> ⚠️ **许可提示（重要）**：`academic-research-skills` 采用 **CC BY-NC 4.0（署名—非商业性使用）**，
> 仅可用于非商业目的。若你打算把本套件用于**商业场景**，请先删除下列 5 个目录
> （它们是该上游在 v5 里的拆分结果）：`references/0-orchestration/pipeline/`、
> `references/1-literature/deep-research/`、`references/1-literature/systematic-review/`、
> `references/2-writing/paper-pipeline/`、`references/3-review/panel/`；
> 或向原作者 Cheng-I Wu（Imbad0202）取得商业授权。其余模块为 MIT / Apache-2.0，
> 商用不受限（保留原始许可与署名即可）。
>
> 每个模块目录下的 `LICENSE` 文件是该模块的**真实上游许可原文或忠实摘要**，
> 以该文件为准，不要只依赖本表的转述。

| # | 模块 | 上游仓库 | 许可 | 收录内容 |
|---|---|---|---|---|
| 1 | nature-skills | `https://github.com/Yuan1z0825/nature-skills` | Apache-2.0 | `skills/` 下 23 个子技能的 SKILL.md / references / scripts（不含 `assets/figures4papers` 图片） |
| 2 | PaperSpine | `https://github.com/WUBING2023/PaperSpine` | MIT | `dist/claude/skills/paper-spine/`（SKILL.md + agents + references + contracts） |
| 3 | academic-research-skills | `https://github.com/Imbad0202/academic-research-skills` | **CC BY-NC 4.0** | `academic-pipeline`/`academic-paper`/`academic-paper-reviewer`/`deep-research`/`sr-screener`/`agents`/`commands`/`shared` |
| 4 | paper-writing-skill | `https://github.com/SNL-UCSB/paper-writing-skill` | MIT | 全部（SKILL.md + author_profile + figure_* + section_rhetorical_moves + writing_checklists + red_team_protocol） |
| 5 | literature-survey-skill | `https://github.com/SNL-UCSB/literature-survey-skill` | MIT | 全部（SKILL.md + reference + templates） |
| 6 | citation-check | `https://github.com/serenakeyitan/citation-check-skill` | MIT | 全部（SKILL.md + references） |
| 7 | paperpipe（papi） | `https://github.com/hummat/paperpipe` | MIT | `skills/` 下 7 个 papi 子技能 + `docs/` |
| 8 | PaperQA2（paper-qa） | `https://github.com/Future-House/paper-qa` | Apache-2.0 | 仅文档：`docs/` + README；**未内置 Python 包**，另附本套件自写使用说明 `SKILL.md` |
| 9 | skill-creator | `https://github.com/anthropics/skills` | Apache-2.0 | **v5 已淘汰**：与宿主自带的 `skill-creator` 完全重复，包内不再收录第二份 |
| 10 | humanized-writing | 用户自建 | MIT | **v5 已淘汰**：内容被 `human-voice` 的五维审计 + 体裁浓度表覆盖，并入 `references/2-writing/humanize/`；`scripts/check_prose.py` 随该目录保留 |
| 11 | **sci-brain** | `https://github.com/QuantumBFS/sci-brain` | MIT | `skills/` 下 16 个子技能（survey / brainstorm-ideas / autoresearch / write-paper / review-paper / write-slides / know-me-better / create-advisor / dump-chat-history / how-to-* 共 8 个）+ LICENSE；**未收录** `write-paper/sources/NotesOnWritingPaper12.pdf` |
| 12 | **Cell 科研套件** | `https://github.com/yrui-cmd/Cell` | MIT | `skills/` 下 13 个成员（cell 总路由 + cell-brainstorm / cell-plan / cell-review / cell-manuscript-editing / cell-reviewer-response / cell-submission / cell-visualization-code / cell-data-figure / cell_su7 / cell_su8 / cell-cns-figure / cell-ppt-edited）+ LICENSE；**未收录** `cell_sci_magic`（八字择时娱乐，与科研流程无关）、`assets/*.jpg`、插件二进制。**推广话术已清理**，见 `_LOCAL_POLICY.md` |
| 13 | **ai-patina（human-voice）** | `https://github.com/Rain13Sad/ai-patina` | MIT | `skills/human-voice/`（SKILL.md + 6 个 references + `scripts/humanity_check.py`）+ `docs/ai-text-detection-landscape.md` + LICENSE |
| 14 | **phd-skills** | `https://github.com/fcakyon/phd-skills` | MIT | `plugin/skills/` 下 2 个技能：`reproduce`（7 阶段论文复现，含 7 个 references）+ `paper-verification`（论文数值/公式/引文核验）+ LICENSE；**未收录** 其余 9 个上游技能（debug/launch/compare 等，套件内已有替代或不需要），交叉引用的本地替代做法见 `references/6-infra/reproduce/MODULE.md` |
| 15 | **research-cycle-skill** | `https://github.com/kris-yun/research-cycle-skill` | MIT | `.codex/skills/research-cycle/SKILL.md`（单文件技能：7 阶段闭环 + 多智能体对抗辩论 + S2 gap 定量）+ LICENSE；README/CHANGELOG 等开发文件未收录 |

### 13 | ai-patina 收录说明

`human-voice` 与 `humanized-writing` 是**互补**关系，不是重复收录：

- `humanized-writing`（自建）管**从零写作时的语感**、四种写作模式、学术写作边界。
- `human-voice`（上游）管**改已有 AI 稿的结构级手术**：五维审计 + 14 个重写动作
  + 句长 CV / 短句占比 / hapax 比等量化指标与阈值。

两者分工与路由规则见 [`references/2-writing/humanize/_MODULE_GUIDE.md`](references/2-writing/humanize/_MODULE_GUIDE.md)。

## v5 变更（2026-10-27）

**结构重构，不向后兼容。** 77 个模块各带一个 `SKILL.md` → 1 个入口 `SKILL.md` + 64 个 `MODULE.md`，
按六个能力族分层。原因：宿主会递归扫描 `SKILL.md` 并逐一注册，77 个文件等于 77 个互相抢触发词的技能，
而入口只路由到 30 个。

- 淘汰 8 个：`cell`（纯路由壳）、`skill-creator`（与宿主重复）、`cell-ppt-edited`（插件说明无工作流）、
  `humanized-writing`（被 human-voice 覆盖）、`nature-citation`、`nature-academic-search`、
  `phd-skills/paper-verification`（三者分别并入更严的模块）、`nature-shared` 的壳 `SKILL.md`。
- 合并 3 组：`codex-research-workflow`→入口文件；`papi-*`×6→`paperpipe` 子命令；`cell_su8`/`cell-cns-figure`→重建路线的档位。
- 旧路径 `modules/<上游>/<子模块>/` 全部改为 `references/<族>/<模块>/`。

逐模块判定见 [`MIGRATION.md`](MIGRATION.md)。

## v4 变更（2026-10-23）

本版新增两个模块，聚焦「论文代码复现」与「对抗式选题」两个环节；
其余环节能力沿用既有模块，未做改动。

| 环节 | v3 状态 | v4 补法 |
|---|---|---|
| ① 选题 | 有（cell-brainstorm / sci-brain brainstorm-ideas） | 新增 `research-cycle`（多智能体对抗辩论 + S2 定量 gap 分级 + GO/REVISE/KILL，7 阶段闭环到复现与写作） |
| 代码复现 | **完全缺失** | 新增 `phd-skills/reproduce`（arXiv 链接 → 7 阶段 → `results.md` 三档标签）+ `paper-verification`（论文数字/公式 ↔ 代码核验） |

## v3 变更（2026-10-23）

在 v2 基础上：新增 `ai-patina` 模块补齐「去 AI 味」的结构级手术能力；补齐各模块 `LICENSE`；
修复 `python3` 跨平台问题；清理 Cell 上游推广话术。

| 环节 | v2 状态 | v3 补法 |
|---|---|---|
| ⑧ 润色 | 有（humanized-writing） | 补 `human-voice`（改 AI 稿的结构手术 + 量化自查），与 `humanized-writing` 分工见 `_MODULE_GUIDE.md` |

## v2 变更（2026-10-22）

在原十模块基础上补入「Codex 科研工作流」十环节统筹层，并新增两个上游补齐缺口：

| 环节 | v1 状态 | v2 补法 |
|---|---|---|
| ① 选题 | 缺独立环节 | 新增 `cell-brainstorm`（证据驱动五选题）+ `sci-brain/brainstorm-ideas`（苏格拉底追问） |
| ② 检索 | 有 | 沿用 `nature-academic-search`，补 `sci-brain/how-to-download-ref`（建可引用知识库） |
| ③ 综述 | 有 | 沿用 `literature-survey-skill`，补 `cell-review`（顶刊 Word、≥30 篇硬门槛） |
| ④ 统筹 | 有（academic-pipeline） | 新增 `SKILL.md/` 十环节统筹层（路由 + 门槛 + 交接单） |
| ⑤ 统计 | 有 | 沿用 `nature-statistics`，补 `cell-visualization-code`（真算与出码） |
| ⑥ 绘图 | 有 | 沿用 `nature-figure`，补 `cell-data-figure`（复现参考图换数据）与 `cell_su7`/`cell_su8`/`cell-cns-figure`（可编辑矢量图） |
| ⑦ 写作 | 有 | 沿用 `nature-writing`，补 `sci-brain/write-paper` |
| ⑧ 润色 | 有 | 沿用 `humanized-writing`，补 `cell-manuscript-editing`（英文深度润色 + humanization pass） |
| ⑨ 投稿 | 有 | 沿用 `nature-reviewer`/`nature-response`，补 `cell-submission`（投稿包）与 `cell-reviewer-response`（两阶段 Word 回复） |
| ⑩ 汇报 | 有 | 沿用 `nature-paper2ppt`，补 `sci-brain/write-slides`（Typst 学术汇报） |

## ⚠️ 外部服务依赖（重要）

`references/` 中三个成员依赖**外部付费服务**，非本地能力：

| 成员（v5 路径） | 依赖 | 费用形态 |
|---|---|---|
| `references/4-figures/reconstruct-su7/`（原 `cell_su7`） | 小描 API（需 API Key） | 每张约 1 额度；可选 `cell_no_ai` 再加 1 额度 |
| `references/4-figures/reconstruct-su7/sub/cell_su8/`（原 `cell_su8`） | 同上 | 每张 3 额度，处理约 5 分钟 |
| 原 `cell-cns-figure`（深嵌档，目录已不收录） | 同上 + 邀请码 | 1 号方案 20 额度；2 号方案 45 额度且需一次性邀请码（24 小时过期、用后即失效）。选档规则并入 `references/4-figures/_index.md` |

**使用前必须向用户明示预计额度并取得授权**；无 Key、余额不足或用户拒绝时降级到
`references/4-figures/data-figure/`（本地 Python/R 绘图，不扣费）。

原 `cell-ppt-edited` 需 **Windows 桌面版 Microsoft PowerPoint**（不支持 WPS / macOS），
且引擎是独立插件（`yrui-cmd/cell_ppt_edited`）——v5 已将其淘汰，能力由
`references/4-figures/image2ppt/` 与 `references/4-figures/paper2ppt/` 覆盖。

`references/` 另有一个可选的一次性准备：`pip install --user pymupdf4llm`（PDF 转文本）。

## 取舍说明

- **只收文本**：剔除 `*.png/*.jpg/*.pdf/*.mp4/*.zip` 等二进制资源，控制体积。
  被剔除的主要是 `nature-figure` 的示例图、Cell 的社交平台图片、sci-brain 的参考 PDF。
- **不收开发设施**：上游的 `evals/`、`tests/`、`scripts/`（评测/测试）、多语言 README 未收录。
- **PaperQA2 不 vendor 代码**：它是完整 Python 包（36 MB），本套件只保留其用法文档并另写 `SKILL.md`；
  安装用 `pip install paper-qa`（Python 3.11+）。
- **Cell 插件不 vendor**：`cell-ppt-edited` 的引擎二进制（`plugins/`）未收录，仅留 `SKILL.md` 接口说明。
- **Cell 推广话术已清理**：上游要求在任务输出中附带作者社交账号推广行，属营销约定而非 MIT 许可要求，
  本仓库统一不输出。物理删除由 `scripts/strip_upstream_promo.py` 完成（已执行），
  行为规则见 `references/4-figures/_LOCAL_POLICY.md`。
  **因此 `references/4-figures/` 下的重建路线不再与上游逐字节一致**，其余模块保持只读副本状态。
- **`references/2-writing/humanize/` 来自上游客 `ai-patina`（human-voice）**，保持只读副本状态；
  自建的 `humanized-writing` 在 v5 已淘汰，只保留它的 `check_prose.py` 作为去 AI 味的形状自查脚本。

## 上游再获取（镜像参考）

本机直连 GitHub 不稳，实测可用：`https://codeload.github.com/<owner>/<repo>/tar.gz/refs/heads/main`
（直连 codeload 可用），或 `https://ghproxy.net/https://github.com/<owner>/<repo>`。
例：`curl -sL "https://codeload.github.com/yrui-cmd/Cell/tar.gz/refs/heads/main" -o cell.tgz`。
