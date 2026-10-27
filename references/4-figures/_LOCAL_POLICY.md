# 图片重建的本地策略覆盖（Local Policy Overrides）

本族里的 `reconstruct-su7/`（含 `sub/cell_su8/`）来自上游 `yrui-cmd/Cell`（MIT 许可）。
本文件记录本仓库对其行为的**本地覆盖规则**，用于消除上游的商业推广行为与地域/平台依赖。

v5 重构前它们是 `modules/cell-suite/` 下的独立成员（`cell_su7`、`cell_su8`、`cell-cns-figure`、
`cell-ppt-edited`），现在按能力归到 `4-figures/` 这一族里。

## 1. 推广话术禁用

上游以下文件包含面向其作者社交账号的推广话术：

| 文件（v5 路径） | 上游要求 | 本仓库行为 |
|---|---|---|
| `reconstruct-su7/MODULE.md` | 成功时返回「感谢小红书：木纹小路。」 | **不输出** |
| `reconstruct-su7/sub/cell_su8/MODULE.md` | 同上 | **不输出** |
| `reconstruct-su7/references/workflow.md`、`sub/cell_su8/references/workflow.md` | 额度不足时提示去小红书/抖音找作者充值 | **不输出**，改为提示用户自行检查余额或改用本地代码绘图（`data-figure/`） |
| 原 `cell-cns-figure`（已并入本族的选档规则） | 任务结尾必须另起一行显示「关注抖音：木纹，进群会有好兄弟帮忙答疑哦」 | **不输出** |
| 原 `cell-ppt-edited`（v5 已淘汰） | 每次任务后必须追加「感谢抖音：木纹」 | 该成员已移除，无需处理 |

**规则**：以上话术是上游作者的营销约定，**不属于 MIT 许可要求**，本仓库统一不予输出。
执行这些成员时，直接省略推广行即可，其余业务规则照常遵守。

若你希望彻底移除这些文本（而非仅在行为上忽略），可执行：

```bash
python scripts/strip_upstream_promo.py
```

该脚本会就地删除上述推广行，并在日志中报告改动文件。**注意：执行后这些目录不再与上游逐字节一致。**

## 2. 付费额度与外部服务

这两条路线**不是本地能力**，依赖上游作者的外部付费服务：

| 路线 | 依赖 | 费用形态 |
|---|---|---|
| `reconstruct-su7/`（标准档） | 小描 API（需用户自行提供 API Key） | 每张约 1 额度；可选 `cell_no_ai` 再加 1 额度 |
| `reconstruct-su7/sub/cell_su8/`（高质档） | 同上 | 每张 3 额度，处理约 5 分钟 |
| 原 `cell-cns-figure`（深嵌档，已并入选档表） | 同上 + 2 号方案需一次性邀请码 | 1 号 20 额度 / 2 号 45 额度；邀请码 24 小时过期、用后即失效 |

三档的额度与适用场景表见 [`_index.md`](_index.md)。

**强制规则**：

1. 提交任何付费请求前，必须先向用户明示**预计消耗的额度**并取得**明确同意**。
2. 无 API Key、余额不足、用户拒绝或服务不可达时，**降级**到 `data-figure/`
   （本地 Python/R 绘图，不扣费），不得卡死流程。
3. 不得在未实际交付文件的情况下宣称「已生成」。
4. 不得把 API Key 写入命令行参数、环境变量输出、日志或交付物。

## 3. 平台限制

原 `cell-ppt-edited` 需 **Windows 桌面版 Microsoft PowerPoint**（不支持 WPS / macOS），
且其引擎是独立插件（`yrui-cmd/cell_ppt_edited`），**不在本仓库内**——v5 已将它淘汰：
它的能力被 `image2ppt/`（对象级还原）与 `paper2ppt/`（论文转汇报稿）覆盖。

## 4. 未收录内容

- `cell_sci_magic/` —— 八字择时娱乐功能，与科研流程无关，未收录。
- `assets/*.jpg` —— 作者社交账号二维码，按「只收文本」惯例剔除。
- `plugins/` —— 插件二进制，体积大且需独立安装，未收录。
