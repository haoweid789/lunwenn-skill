---
name: paper-qa
description: "PaperQA2（CLI 名 pqa）本地文献 RAG 模块。对一整个目录的论文 PDF/文本做检索增强问答，输出带文内引文（含页码）的答案，支持共识 / 分歧 / 证据缺口梳理。当需要「就某批论文提问」「验证代码是否与论文一致」「跨论文找矛盾」时使用。触发词：paper-qa、paperqa、pqa、本地文献库问答、PDF 问答、RAG 文献、跨论文比较、证据缺口。"
---

# PaperQA2（pqa）—— 本地文献库检索问答模块

> 上游：https://github.com/Future-House/paper-qa ｜ 许可 Apache-2.0 ｜ 本模块只保留文档，未内置 Python 包。

## 一、它做什么

对一整个目录的科学文献做高精度 RAG：自动抽取元数据（Crossref / Semantic Scholar，
含引用数与撤稿检查）→ 解析并缓存 PDF 到全文索引 → 由 LLM agent 检索、聚合证据 →
输出**带文内引文（含页码/片段）**的答案。适合把同一研究问题下的多篇全文放进一个目录，
追查**共识 / 分歧 / 证据缺口**，而不是单篇摘要。

## 二、安装与配置

```bash
pip install paper-qa            # 需要 Python 3.11+（v5 起即 PaperQA2）
# 需要 LLM：设置 OPENAI_API_KEY，或用任何 LiteLLM 兼容模型（本地 llamafile 等）
# 大批量（100+ 篇）建议再配：
#   export CROSSREF_API_KEY=...  export SEMANTIC_SCHOLAR_API_KEY=...   # 避免公共限速
```

## 三、CLI 用法（`pqa`）

```bash
mkdir my_papers && curl -o my_papers/PaperQA2.pdf https://arxiv.org/pdf/2409.13740
cd my_papers
pqa ask 'What is PaperQA2?'                 # 首次会索引该目录；之后复用索引
pqa search -i 'answers' 'antibodies'        # 在历史答案里检索
pqa -i nanomaterials index                  # 给某目录索引命名
pqa -i nanomaterials ask 'Are there nm scale features in thermoelectric materials?'
pqa --temperature 0.5 ask '...'             # 单次覆盖参数
pqa view                                    # 查看全部设置
pqa -s fast view                            # 查看内置模板设置（fast 等）
pqa -s my_new_settings --temperature 0.5 --llm foo-bar-5 save   # 存自定义设置
pqa --parsing.chunk_size 5000 ask '...'     # 改参数会自动重建索引
```
索引与历史答案默认存 `PQA_HOME`（默认 `~/.pqa/`）。设置速查见 `_UPSTREAM_README.md`。

## 四、综述式推荐提示词（把结论/冲突/出处拆开）

```
pqa ask 请只基于当前目录中的论文回答：
1. 围绕这个核心问题，已有研究形成了哪些共识？
2. 哪些结论彼此冲突？请标出对应论文与页码或片段出处。
3. 这些冲突是否可能来自研究对象、研究设计或情境差异？
4. 哪些问题在当前文献集合里缺少直接证据？
每条判断给出文内引文；证据不足时写「当前目录无法确认」。
```

## 五、在本套件中的位置

- 上游语料来自 **paperpipe（papi）** 的论文库或 **nature-downloader** 下载的 PDF；
  `papi` 负责单篇精确查（`papi show/search`），`pqa` 负责跨篇语义问答（RAG），二者互补。
- `pqa` 的答案仍需 **citation-check** 复核后才能写进正式论文（RAG 也会读错）。
- 本地大文件（`docs/`、`_UPSTREAM_README.md`）为上游随附资料，按需查阅，勿整套塞进上下文。
