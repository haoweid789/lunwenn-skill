# 贡献指南

感谢你愿意参与。本仓库是一个**技能聚合仓库**：主体是上游开源项目的只读副本，
本仓库自己编写的是路由层、统筹层与整合工具。

## 分工：改哪里

| 你想改什么 | 改哪里 | 说明 |
|---|---|---|
| 路由逻辑、十环节编排、红线 | `SKILL.md`、`modules/codex-research-workflow/` | **本仓库自写**，欢迎直接 PR |
| 模块分工说明 | `modules/human-voice/_MODULE_GUIDE.md`、`modules/cell-suite/_LOCAL_POLICY.md` | **本仓库自写** |
| 上游模块内容 | `modules/<upstream>/` | **请勿直接改** —— 见下方「上游同步流程」 |
| 上游版本升级 | 新增/替换 `modules/<upstream>/` 整个目录 | 走「上游同步流程」 |
| 发布脚本、清理脚本 | `scripts/` | **本仓库自写** |

## 上游同步流程

`modules/` 下的上游目录是**只读副本**。升级某个上游时：

1. 从 `SOURCES.md` 的地址拉取上游仓库（**codeload 直连通常可用**）：
   ```bash
   curl -sL "https://codeload.github.com/<owner>/<repo>/tar.gz/refs/heads/main" -o repo.tgz
   tar -xzf repo.tgz
   ```
   若直连失败，依次尝试 `ghproxy.net` / `gh-proxy.com` / `ghfast.top` 镜像。
2. 按「只收文本」惯例剔除二进制：`*.png *.jpg *.pdf *.mp4 *.zip *.pptx *.docx`。
3. **保留上游 `LICENSE` 文件**；上游没有 LICENSE 时，在 `SOURCES.md` 查证真实许可后补写。
4. 更新 `SOURCES.md` 的版本说明与 `SKILL.md` 的模块表（如入口文件有变化）。
5. 若上游含推广话术或商业引导，运行 `python scripts/strip_upstream_promo.py` 清理，
   并在 `_LOCAL_POLICY.md` 记录覆盖规则。

## 硬性要求

提交前请自查这几条，它们是本仓库的核心约束：

- [ ] **不引入任何硬编码凭证**（API Key、token、密码、`.env`）。所有凭据走环境变量或用户输入。
- [ ] **不引入个人路径**（`C:\Users\<你的用户名>\...`、`/home/<用户名>/...`）。用相对路径或占位符。
- [ ] **不编造数据**：新增的示例、测试数据必须标注为合成数据（synthetic）。
- [ ] **保持 CC BY-NC 边界**：不得把 `modules/academic-research-skills/` 的内容移入 MIT 区域。
- [ ] **新模块必须带 `LICENSE`** 或在 `SOURCES.md` 中查证并声明真实许可。
- [ ] **入口 `SKILL.md` 的 frontmatter 必须有 `name` 和 `description`**，
      `description` 要含中英文触发词，否则宿主无法路由到它。
- [ ] **python3 → python**：`python3` 在 Windows 上不存在，文档示例用 `python`，
      并注明 macOS/Linux 用 `python3`。
- [ ] **脚本只用标准库**，除非在 `SKILL.md` 中明确写出 `pip install` 依赖。

## 提交规范

```bash
git clone https://github.com/<你的fork>/lunwenn-skill.git
cd lunwenn-skill
# ... 修改 ...
git add -A
git commit -m "feat: 补充 xxx 环节的路由说明"
git push origin <你的分支>
```

提交信息用中文或英文均可，类型前缀：`feat` / `fix` / `docs` / `chore` / `refactor`。

## 校验清单

改动后至少跑一遍：

```bash
# 1. 所有入口 SKILL.md 的 frontmatter 合法
python scripts/validate_skill.py

# 2. 全部 Python 脚本可编译
python -m compileall -q scripts modules

# 3. 无个人路径 / 无硬编码凭证
grep -rniE "C:\\\\Users\\\\|sk-[A-Za-z0-9]{20,}|api_key\s*=\s*['\"][A-Za-z0-9]{16,}" --include="*.md" --include="*.py" .
```

## 报告问题

开 issue 时请附上：你的宿主（Codex / Claude Code / 其他）、操作系统、
触发时用的完整指令、以及实际发生的现象。

## 许可

你贡献的内容按仓库顶层 [LICENSE](LICENSE) 的 MIT 条款发布；
若你修改了 `modules/` 下的上游副本，请同时注明所基于的上游项目与版本。
