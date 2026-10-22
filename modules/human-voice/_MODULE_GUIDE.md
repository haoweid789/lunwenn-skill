# human-voice 模块定位（与 humanized-writing 的分工）

本模块是 `Rain13Sad/ai-patina` 上游的只读副本（MIT 许可，作者 Rain13Sad）。

仓库同时收录了两个功能相近的「去 AI 味」模块。它们**互补，不重复**：

| | `modules/humanized-writing/` | `modules/human-voice/`（本模块） |
|---|---|---|
| 出身 | 用户自建 | `Rain13Sad/ai-patina`（MIT） |
| 核心问题 | 「这段话怎么写才像人写的」——原则与词库 | 「这段 AI 味具体在哪，怎么做结构手术」——可量化动作 |
| 组织方式 | 四种写作模式 + 通用原则 + 词库清单 | S0–S5 工作流 + 14 个重写动作（A组结构/B组节奏）+ 五维审计 |
| 长度节奏 | 给出语感与原则 | 给句长 CV、短句占比、段落 CV、hapax 比等**具体指标与阈值** |
| 自查工具 | `scripts/check_prose.py`（查硬禁令与模型化形状） | `scripts/humanity_check.py`（句长波动、词汇多样性、格式痕迹，含待办清单） |
| 英文 | `references/en-humanizer.md` | `references/en-writing-guide.md`（英文专属痕迹：tricolon、em dash、"not just X but Y"） |
| 强项 | 从零写作时的语感把控；学术写作（反防御性、审稿人视角） | 已有 AI 稿的**结构级手术**；体裁浓度区分；文风画像提取 |
| 特有内容 | `references/academic.md`、`references/ai-vocab.md` | `references/voice-profile.md`（六维文风提取）、`references/detector-model.md`、`docs/ai-text-detection-landscape.md` |

## 路由规则

1. **从零写**（写摘要、写公众号、写评论）→ 先 `humanized-writing`（它管语感与模式选择）。
2. **改已有 AI 稿**（"这段太 AI 了，帮我改"）→ 先 `human-voice`（它管诊断与结构手术）。
   它的 S1 诊断 → S2 结构重写 → S3 节奏工程 → S4 痕迹清扫，是一条可直接执行的流水线。
3. **学术论文投稿前**→ 两者都上：`humanized-writing` 管学术语感与不越界（不改事实/数字/引文），
   `human-voice` 管可量化的节奏与痕迹清扫（尤其 `traces-checklist.md` 的数字两侧空格一项）。
4. **只想要一张自查表** → 直接跑 `scripts/humanity_check.py`（纯标准库，无依赖）。

## 两条共同红线

- **不承诺任何检测器分数**。两个模块都不产生「AI 率从 X% 降到 Y%」这类承诺——分数随分段、
  长度、上下文漂移，不可复现。
- **不伪造过程证据**。不清理元数据、不伪造文档结构或修订记录、不移除水印。
  `human-voice` 明确列出《人工智能生成合成内容标识办法》与 GB 45438-2025 的边界。
- **不改事实**。润色不改数字、引文、来源，不把推测写成确定；虚构引用必须单独列给作者。

## 自查脚本对照

```bash
# 表层形状（黑话/翻案句/破折号/Tier-1 高频词）
python modules/humanized-writing/scripts/check_prose.py 稿件.md

# 量化人味指标 + 待办清单
python modules/human-voice/scripts/humanity_check.py 稿件.md
python modules/human-voice/scripts/humanity_check.py 稿件.md --json
```

两者都是**启发式自查**，只报告形状与形状的成因；是否真有问题要回材料判断。
脚本通过 ≠ 文本合格，脚本不通过 ≠ 文本有问题。
