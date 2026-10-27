# lunwenn

**科研与论文全流程技能** —— 把「一个研究课题 → 一篇可投稿论文」的整条链路装进一个技能。

一个入口（`SKILL.md`）+ 六族参考（`references/`）+ 一个十环节状态机。
按需加载：模型只读当前环节需要的那一个目录，不预载整包。

```
lunwenn/
├── SKILL.md              唯一入口：十环节状态机 + 六族路由 + 硬红线
├── MIGRATION.md          77 个上游模块逐个的判定表（精华 / 判定 / 去向）
├── references/
│   ├── 0-orchestration/   4  十阶段流水线 · 研究循环 · autoresearch · flow
│   ├── 1-literature/     10  全文获取 · 综述四模式 · 深研 · 系统综述 · 精读 · 翻译 · 透视
│   ├── 2-writing/        10  章节起草 · 12 智能体重装 · 编辑门禁 · 七段模板 · 润色 · 去 AI 味
│   ├── 3-review/          8  模拟审稿 · 九准则 · 五座席 · rebuttal · 引文核验 · 顶刊综述
│   ├── 4-figures/         8  论文级出图 · 六步复现 · 图→可编辑 PPT · 组会 PPT · 评分细则
│   ├── 5-submission/     10  投稿六步 · 数据声明 · 基金本子 · 专利 · 统计 · 选题 · 排期
│   └── 6-infra/          14  期刊硬约束 · 写作规范 · papi 论文库 · 文风学习 · 知识库
├── SOURCES.md            上游来源、许可与收录说明
├── CONTRIBUTING.md       贡献指南
├── LICENSE               顶层 MIT（仅覆盖本仓库自写内容）
└── scripts/
    ├── validate_skill.py       结构校验（入口唯一性 / 路径 / 许可 / 敏感信息）
    └── strip_upstream_promo.py 清理上游推广话术
```

共 **64 份模块说明**，覆盖 **15 个上游项目**（14 个开源仓库 + 1 个自建）。

## 命名约定（重要）

模块说明文件叫 **`MODULE.md`**，不叫 `SKILL.md`。

多数宿主（WorkBuddy、Claude Code、Codex 等）会**递归扫描**技能目录下的所有 `SKILL.md` 并逐一注册。
本包在 v5 之前是 77 个模块各带一个 `SKILL.md`，装进去就等于注册了 77 个互相抢触发词的技能，
而入口只路由到其中 30 个——剩下 47 个成为永远找不到的孤儿。

改名后全包只有顶层 1 个 `SKILL.md`，`MODULE.md` 退化为纯文档，只有被 `SKILL.md` 路由到时才读。
各模块自带的 `README.md` 保持原名，它讲「这个模块怎么用」，与 `MODULE.md`（工作流本体）是两份东西。

## 十环节状态机

先判断用户在哪个环节，再跳到对应族。**不按顺序硬走全流程**——用户说「帮我改一下这句」就只做第 7 环。

| # | 环节 | 用户常说的话 | 主入口 |
|---|---|---|---|
| 1 | 选题 | 找个题目、这个方向能做吗、新颖性 | `references/5-submission/brainstorm/` |
| 2 | 检索 | 找文献、有几篇、别人做过没 | `references/1-literature/survey/` |
| 3 | 综述 | 写综述、领域版图、系统综述 | `references/1-literature/systematic-review/` |
| 4 | 统筹 | 帮我按流程来、下一步做什么 | `SKILL.md` 本身 |
| 5 | 分析 | 数据怎么算、用什么检验 | `references/5-submission/statistics/` |
| 6 | 绘图 | 出图、复现这张图、图不好看 | `references/4-figures/data-figure/` |
| 7 | 写作 | 写正文、改这段、压缩 | `references/2-writing/manuscript/` |
| 8 | 润色 | 润色、去 AI 味、翻译 | `references/2-writing/polish/` |
| 9 | 审稿 | 帮我审一下、模拟审稿、rebuttal | `references/3-review/peer-review/` |
| 10 | 投稿 | 投稿材料、数据声明、专利 | `references/5-submission/submission/` |

跨环节时写**交接单**（已完成 / 关键结论 / 未决问题 / 下一步），否则下一个环节会重做判断。

## 安装

把整个目录放进你的技能目录，目录名保持 `lunwenn`：

```bash
# WorkBuddy
cp -r lunwenn ~/.workbuddy/skills/

# Claude Code
cp -r lunwenn ~/.claude/skills/

# Codex
cp -r lunwenn ~/.codex/skills/
```

单项目使用：放进项目的 `.claude/skills/` 或 `.workbuddy/skills/`。

装完确认**只多出一个**叫 `lunwenn` 的技能，不是一个加六十四个。

**依赖**：无强制依赖，核心脚本只用 Python 3.10+ 标准库。
可选：`pip install jsonschema==4.26.0`（`brainstorm` 的质量门禁）、
`pip install pymupdf4llm`（PDF 渲染）、`pip install paper-qa`（PaperQA2 本体）。

## 怎么用

1. 触发：说「写论文 / 文献综述 / 去 AI 味 / 引文核验 / 模拟审稿 / rebuttal / 十环节 / 选题」等 → 加载本技能。
2. `SKILL.md` 里的十环节表定位当前任务 → 跳到对应族。
3. 先读该族的 `_index.md`（路由与取舍），再决定要不要读具体模块的 `MODULE.md`。
4. **不要整目录塞进上下文**——`1-literature/`、`2-writing/` 等族目录较大，只读需要的那个模块。

## 六条硬红线

- **不编造**：数据、文献、审稿意见、期刊政策、页码，一律不出。查不到就说查不到，并说明查过哪些源。
- **证据边界**：用户没给的结果不写；推断必须标成推断。
- **引文必核验**：进论文的引用要能追到真实来源。
- **不代填署名与声明**：作者贡献、利益冲突、AI 使用声明只帮起草，最终由用户确认。
- **付费能力先报价**：`references/4-figures/reconstruct-su7/`（含 `sub/cell_su8/`）走外部额度制服务，
  按张计费。扣费前须向用户明示预计消耗并取得同意；无 Key / 余额不足时降级到本地代码绘图。
- **完成 ≠ 授权**：完成某一环不自动授权推进下一环、上传、付费或投稿。

## 自查脚本

```bash
# 结构校验
python scripts/validate_skill.py            # 基础
python scripts/validate_skill.py --strict   # 追加凭证与个人路径扫描

# 去 AI 味形状自查
python references/2-writing/humanize/scripts/check_prose.py 稿件.md
python references/2-writing/humanize/scripts/humanity_check.py 稿件.md
```

> Windows 上是 `python`，macOS/Linux 上是 `python3`。

## 许可

**逐模块许可。** 顶层 MIT 只覆盖本仓库自己写的内容：
`SKILL.md`、`MIGRATION.md`、`README.md`、`SOURCES.md`、`CONTRIBUTING.md`、`scripts/`。

`references/` 下的上游归档模块**保留各自原有许可**，以各模块目录下的 `LICENSE` 为准：

| 上游 | 许可 | 可否商用 | 落在哪些族 |
|---|---|---|---|
| academic-research-skills | **CC BY-NC 4.0** | ❌ **仅非商业** | `0-orchestration/pipeline`、`1-literature/deep-research`、`1-literature/systematic-review`、`2-writing/paper-pipeline`、`3-review/panel` |
| nature-skills | Apache-2.0 | ✅ | 1 / 2 / 3 / 4 / 5 族多数模块 + `6-infra/core`、`6-infra/journal-formats` |
| paper-qa | Apache-2.0 | ✅ | `1-literature/paper-qa` |
| 其余 13 个（MIT） | MIT | ✅ | 见各模块 `LICENSE` |

**商业用途请先删除上述 5 个 CC BY-NC 模块。**
上游作者、仓库地址与收录取舍见 [`SOURCES.md`](SOURCES.md)；
77 个原模块的逐条判定见 [`MIGRATION.md`](MIGRATION.md)。

## 体积

约 17 MB / 1420 文件。已剔除图片、参考 PDF、评测数据、多语言 README 等大体积资源。

## 版本

| 版本 | 变更 |
|---|---|
| v5 | 结构重构：77 个 `SKILL.md` → 1 个入口 + 64 个 `MODULE.md`，按六族分层；淘汰 8 个重复/空壳模块；补齐孤儿模块的路由。**不向后兼容**——旧路径 `modules/*/` 全部改为 `references/<族>/*/` |
| v4 | 新增代码复现与对抗式选题模块（phd-skills + research-cycle） |
| v3 | 补齐去 AI 味、引文核验、可编辑矢量图 |
| v2 | 加入十环节统筹层 |
