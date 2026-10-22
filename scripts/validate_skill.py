#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验 lunwenn-skill 仓库的结构完整性。

检查项：
1. 入口 SKILL.md 的 frontmatter 是否有合法的 name / description
2. SKILL.md 中引用的 modules/... 路径是否真实存在
3. 每个模块目录是否带 LICENSE
4. 是否存在硬编码凭证或个人路径（可 --strict 时启用）

用法::

    python scripts/validate_skill.py                # 基础校验
    python scripts/validate_skill.py --strict       # 追加敏感信息扫描
    python scripts/validate_skill.py --json         # 输出 JSON，便于 CI

退出码：0 = 全部通过（可能有 warning）；1 = 存在 error。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# 入口文件：宿主会读取这些 SKILL.md 作为技能入口
ENTRY_GLOBS = [
    "SKILL.md",
    "modules/*/SKILL.md",
    "modules/*/*/SKILL.md",
]

# 敏感信息扫描规则
SECRET_PATTERNS = [
    (r"sk-[A-Za-z0-9]{20,}", "疑似 OpenAI 风格 API Key"),
    (r"ghp_[A-Za-z0-9]{30,}", "疑似 GitHub Personal Access Token"),
    (r"github_pat_[A-Za-z0-9_]{50,}", "疑似 GitHub Fine-grained PAT"),
    (r"AKIA[0-9A-Z]{16}", "疑似 AWS Access Key ID"),
    (r"api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]", "硬编码 API Key"),
    (r"secret\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]", "硬编码 secret"),
    (r"password\s*[:=]\s*['\"][^\s'\"]{8,}['\"]", "硬编码 password"),
]
PERSONAL_PATH_PATTERNS = [
    (r"C:\\Users\\[A-Za-z0-9_.\-]+", "Windows 个人路径"),
    (r"/home/[A-Za-z0-9_.\-]+/", "Linux 个人路径"),
    (r"/Users/[A-Za-z0-9_.\-]+/", "macOS 个人路径"),
]

# 这些路径出现在上游文档里属于正常示例，不算泄露
PERSONAL_PATH_ALLOWLIST = [
    "modules/paperspine/references/interactive-intake.md",
    "modules/sci-brain/dump-chat-history/helpers/extract_dialog.py",
    "modules/cell-suite/cell-cns-figure/docs/INSTALL.md",
    # 上游作者本机的示例 PDF 路径（非本仓库贡献者信息）
    "modules/nature-skills/nature-reader/evals/evals.json",
]

# 单元测试里的假凭证：出现在 tests/ 目录且为明显占位值
FAKE_CREDENTIAL_HINTS = (
    "publisher-secret",
    "test-secret",
    "dummy",
    "fake-",
    "example",
    "placeholder",
    "no-key-required",
)


def parse_frontmatter(text: str) -> dict | None:
    """解析 YAML frontmatter，返回 dict；无 frontmatter 返回 None。"""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fm = m.group(1)
    out: dict[str, str] = {}
    # 折叠式 / 多行式 description
    dm = re.search(r"^description:\s*(.*)$", fm, re.M)
    if dm:
        val = dm.group(1).strip()
        if val in (">", ">-", "|", "|-"):
            # 收集后续缩进行
            lines = fm[dm.end():].split("\n")
            buf = []
            for ln in lines:
                if ln.strip() and not ln.startswith((" ", "\t")):
                    break
                buf.append(ln.strip())
            val = " ".join(x for x in buf if x)
        out["description"] = val.strip('"\'')
    nm = re.search(r"^name:\s*(.+)$", fm, re.M)
    if nm:
        out["name"] = nm.group(1).strip().strip('"\'')
    return out


def iter_entry_files() -> list[Path]:
    seen: set[Path] = set()
    for pattern in ENTRY_GLOBS:
        for p in REPO.glob(pattern):
            if p.is_file() and p not in seen:
                seen.add(p)
    return sorted(seen)


def check_frontmatter(errors: list, warnings: list) -> int:
    checked = 0
    for p in iter_entry_files():
        rel = p.relative_to(REPO).as_posix()
        text = p.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text)
        if fm is None:
            errors.append(f"[frontmatter] {rel}：缺少 frontmatter")
            continue
        name = fm.get("name", "")
        desc = fm.get("description", "")
        if not name:
            errors.append(f"[frontmatter] {rel}：缺少 name")
        elif not re.fullmatch(r"[a-z0-9][a-z0-9\-_]*", name):
            errors.append(f"[frontmatter] {rel}：name 不合规（应小写+连字符）: {name!r}")
        if not desc:
            errors.append(f"[frontmatter] {rel}：缺少 description")
        elif len(desc) < 20:
            warnings.append(f"[frontmatter] {rel}：description 过短（{len(desc)} 字符），可能难以触发")
        checked += 1
    return checked


def check_referenced_paths(errors: list, warnings: list) -> int:
    count = 0
    for md in [REPO / "SKILL.md", REPO / "README.md", REPO / "CONTRIBUTING.md"]:
        if not md.is_file():
            continue
        text = md.read_text(encoding="utf-8", errors="replace")
        for rel in sorted(set(re.findall(r"`(modules/[A-Za-z0-9_\-/\.]+?)`", text))):
            target = rel.rstrip("/")
            if "<" in target or "*" in target:
                continue
            count += 1
            if not (REPO / target).exists():
                errors.append(f"[路径] {md.name} 引用了不存在的路径：{target}")
    return count


def check_licenses(errors: list, warnings: list) -> int:
    mods = REPO / "modules"
    if not mods.is_dir():
        errors.append("[结构] 缺少 modules/ 目录")
        return 0
    count = 0
    for d in sorted(mods.iterdir()):
        if not d.is_dir():
            continue
        count += 1
        if not (d / "LICENSE").exists() and not (d / "LICENSE.txt").exists():
            errors.append(f"[许可] modules/{d.name}/ 缺少 LICENSE 文件")
    if not (REPO / "LICENSE").exists():
        errors.append("[许可] 仓库根目录缺少 LICENSE 文件")
    return count


def scan_sensitive(errors: list, warnings: list) -> int:
    hits = 0
    allow = {REPO / a for a in PERSONAL_PATH_ALLOWLIST}
    for p in REPO.rglob("*"):
        if not p.is_file() or p in allow:
            continue
        if p.suffix.lower() not in (".md", ".py", ".json", ".yaml", ".yml", ".toml", ".txt", ".sh", ".ps1"):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = p.relative_to(REPO).as_posix()
        for pat, label in SECRET_PATTERNS:
            for m in re.finditer(pat, text):
                snippet = m.group(0)
                low = snippet.lower()
                # 允许示例值、占位符与单元测试里的假凭证
                if any(x in low for x in FAKE_CREDENTIAL_HINTS):
                    continue
                if any(x in low for x in ("your-", "xxx", "<", "example", "placeholder")):
                    continue
                if "/tests/" in rel or rel.endswith("test_*.py"):
                    warnings.append(f"[疑似测试桩] {rel}：{label}（位于测试目录，请人工确认）")
                    hits += 1
                    continue
                errors.append(f"[密钥] {rel}：{label} —— {snippet[:40]}")
                hits += 1
        for pat, label in PERSONAL_PATH_PATTERNS:
            for m in re.finditer(pat, text):
                snippet = m.group(0)
                if "C:\\Users\\qw123" in snippet:
                    continue  # 作者本机路径，随仓库历史保留
                warnings.append(f"[隐私] {rel}：{label} —— {snippet[:40]}")
                hits += 1
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description="校验 lunwenn-skill 仓库结构")
    ap.add_argument("--strict", action="store_true", help="追加敏感信息扫描")
    ap.add_argument("--json", action="store_true", help="以 JSON 输出结果")
    args = ap.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    n_entries = check_frontmatter(errors, warnings)
    n_paths = check_referenced_paths(errors, warnings)
    n_mods = check_licenses(errors, warnings)
    n_sensitive = scan_sensitive(errors, warnings) if args.strict else 0

    result = {
        "entries_checked": n_entries,
        "paths_checked": n_paths,
        "modules_checked": n_mods,
        "sensitive_hits": n_sensitive,
        "errors": errors,
        "warnings": warnings,
        "passed": not errors,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"入口 SKILL.md：{n_entries} 个")
        print(f"路径引用：{n_paths} 处")
        print(f"模块目录：{n_mods} 个")
        if args.strict:
            print(f"敏感信息扫描：{n_sensitive} 处命中")
        print()
        if warnings:
            print(f"警告 {len(warnings)} 条：")
            for w in warnings:
                print(f"  {w}")
            print()
        if errors:
            print(f"错误 {len(errors)} 条：")
            for e in errors:
                print(f"  {e}")
        else:
            print("✅ 全部检查通过")
        print()
        print("提示：加 --strict 可扫描硬编码凭证与个人路径。")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
