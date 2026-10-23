# lunwenn-skill

**论文全流程综合技能** —— 把「一个研究课题 → 一篇可投稿论文」的整条链路装进一个技能。

它把十五个上游项目（十四个开源科研写作项目 + 一个自建去 AI 味技能）编成一条流水线，按需加载。
`SKILL.md` 是路由总控；各上游内容以只读副本放在 `modules/` 下。

## 两套流水线

| 流水线 | 何时用 | 环节 |
|---|---|---|
| **十环节制**（`modules/codex-research-workflow/`） | 用户要走完整科研流程 | 选题 → 检索 → 综述 → **统筹** → 统计 → 绘图 → 写作 → 润色 → 投稿 → 汇报 |
| **十二站制**（`SKILL.md` 第二节） | 单点任务、按论文产物推进 | 立项 → 检索 → 综述 → 骨架 → 写作 → 润色 → 核验 → 图表 → 审稿 → 返修 → 交付 → 汇报 |

十环节制是科研**决策顺序**，十二站制是论文**产物顺序**；两者嵌套使用，十环节制在③④⑦⑨处指向十二站制对应站点。

## 目录结构

```
lunwenn-skill/
├── SKILL.md                 路由总控（先读它）
├── README.md                本文件
├── SOURCES.md               来源、许可与收录说明（含 NC 许可提示 + 付费依赖说明）
├── CONTRIBUTING.md          贡献指南（改哪里、怎么同步上游、提交前自查）
├── LICENSE                  顶层 MIT（仅覆盖本仓库自写内容）
├── scripts/
│   ├── validate_skill.py    仓库结构校验（frontmatter / 路径 / LICENSE / 敏感信息）
│   └── strip_upstream_promo.py  清理上游推广话术
└── modules/
    ├── codex-research-workflow/  ★ 十环节统筹层：路由表 + 门槛 + 跨环交接单
    ├── cell-suite/                ★ Cell 科研套件：选题/计划/顶刊综述/英文润色/审稿回复/投稿包/绘图代码/可编辑矢量图
    ├── sci-brain/                 ★ 文献知识库 + 苏格拉底选题 + autoresearch 验证循环 + 学术 slides
    ├── human-voice/               ★ 改 AI 稿的结构级手术 + 量化自查（humanity_check.py）
    ├── phd-skills/                ★ 论文复现 7 阶段流水线 + 论文数值/公式核验
    ├── research-cycle/            ★ 多智能体对抗式选题闭环（S2 定量 gap + GO/REVISE/KILL）
    ├── nature-skills/              23 个子技能：写作/润色/图/引文/审稿回复/读文/PPT/专利/统计
    ├── paperspine/                 motivation 驱动的论文骨架与修订矩阵
    ├── academic-research-skills/   10 阶段学术流水线（research→write→review→revise→finalize）
    ├── paper-writing-skill/        结构化立意 + 五阶段写作管线 + 修辞动作 + 红队
    ├── literature-survey-skill/    文献综述四阶段（Intent→Triage→Deepen→Synthesize）
    ├── citation-check/             两遍式引文核验
    ├── paperpipe/                  论文库 CLI（papi）+ 6 个子工作流
    ├── paper-qa/                   本地 PDF 目录 RAG（PaperQA2 / pqa）
    ├── skill-creator/              维护/评测/改进本技能自身
    └── humanized-writing/          去 AI 味写作 + check_prose.py（原目录副本）
```

★ = v2/v3/v4 新增

## 安装

把整个 `lunwenn-skill/` 目录放到你的技能目录即可：

```bash
# WorkBuddy / 通用
cp -r lunwenn-skill ~/.workbuddy/skills/

# Claude Code
cp -r lunwenn-skill ~/.claude/skills/

# Codex
cp -r lunwenn-skill ~/.codex/skills/
```

单项目使用：放进项目的 `.claude/skills/` 或 `.workbuddy/skills/`。

**依赖**：无强制依赖。核心脚本只用 Python 3.10+ 标准库。
可选：`pip install jsonschema==4.26.0`（`cell-brainstorm` 的质量门禁需要）、
`pip install pymupdf4llm`（sci-brain 的 PDF 渲染）、`pip install paper-qa`（PaperQA2 本体）。

## 怎么用

1. 触发：说「写论文 / 文献综述 / 去 AI 味 / 引文核验 / 模拟审稿 / rebuttal / 按科研工作流走 / 十环节 / 选题」等 → 加载本技能。
2. 先看 `SKILL.md` 的**路由表**，定位到当前任务对应的模块，再打开该模块的入口 `SKILL.md`。
3. 只读当前阶段需要的文件，**不要整目录塞进上下文**（`nature-skills`、`cell-suite` 等目录较大）。
4. 端到端写论文时，按 `SKILL.md` 的**十二站流水线**或**十环节制**推进，每站产出真实材料。

## 五条硬底线

- **证据绑定**：数值 / 指标 / 引文 / 图表必须来自真实材料，禁止编造。
- **引文必核验**：进论文的引用要能追到真实来源，核过才算数。
- **原目录只读**：`humanized-writing` 原目录不动，本技能改动只落在本技能目录内。
- **付费授权前置**：`cell_su7`/`cell_su8`/`cell-cns-figure` 走外部额度制服务，扣费前须向用户明示预计消耗并取得同意；无 Key / 余额不足时降级到 `nature-figure` 本地绘图。
- **完成 ≠ 授权**：完成某一环不自动授权推进下一环、上传、付费或投稿。

## 自查脚本

```bash
# 去 AI 味形状自查
python modules/humanized-writing/scripts/check_prose.py 稿件.md

# 量化人味指标 + 待办清单
python modules/human-voice/scripts/humanity_check.py 稿件.md
```

> `python3` 在 Windows 上不存在，Windows 用 `python`；macOS/Linux 用 `python3`。

## 开发

```bash
python scripts/validate_skill.py --strict   # 结构 + 敏感信息校验
python -m compileall -q scripts modules     # 语法检查
```

贡献前请读 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可

**本仓库采用逐模块许可**——顶层 MIT 只覆盖本仓库自己编写的内容
（`SKILL.md`、`README.md`、`SOURCES.md`、`CONTRIBUTING.md`、
`modules/codex-research-workflow/`、`modules/humanized-writing/`、`scripts/`）。

`modules/` 下的上游归档模块**保留各自原有许可**，以各模块目录下的 `LICENSE` 文件为准：

| 模块 | 许可 | 可否商用 |
|---|---|---|
| `academic-research-skills` | **CC BY-NC 4.0** | ❌ **仅非商业** |
| nature-skills | Apache-2.0 | ✅ |
| paper-qa | Apache-2.0 | ✅ |
| paperspine / paperpipe / paper-writing-skill / literature-survey-skill / citation-check / skill-creator / sci-brain / cell-suite / human-voice / humanized-writing / phd-skills / research-cycle | MIT | ✅ |

**商业用途请先移除 `modules/academic-research-skills/`。**
各上游项目的作者、仓库地址与收录取舍见 [`SOURCES.md`](SOURCES.md)。

## 体积

约 20 MB / 1795 文件；已剔除图片、参考 PDF、评测数据、多语言 README 等大体积资源。
