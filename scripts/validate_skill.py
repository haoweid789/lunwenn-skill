#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验 lunwenn 仓库的结构完整性（v5 结构）。

检查项：
1. 入口唯一性：全仓库只允许 1 个 `SKILL.md`（宿主会递归扫描并逐个注册，多一个就多一个技能）
2. 入口 frontmatter 是否有合法的 name / description
3. 文档里引用的 `references/...` 路径是否真实存在
4. 每个模块目录是否带 LICENSE
5. 是否存在硬编码凭证或个人路径（--strict 时启用）

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
REFS = REPO / "references"

# 六族（顺序即 SKILL.md 里的编号）
FAMILIES = [
    "0-orchestration",
    "1-literature",
    "2-writing",
    "3-review",
    "4-figures",
    "5-submission",
    "6-infra",
]

# 需要校验路径引用的文档
DOCS_WITH_PATHS = ["SKILL.md", "README.md", "CONTRIBUTING.md", "MIGRATION.md"]

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

# 这些目录/文件出现在上游文档里属于正常示例，不算泄露
PERSONAL_PATH_ALLOWLIST = [
    "references/1-literature/reader/evals",
    "references/1-literature/downloader/docs",
    "references/6-infra/chat-history/helpers",
    "references/2-writing/paperspine/references",
]

# 明显是占位/测试桩的值，不算泄露
FAKE_CREDENTIAL_HINTS = (
    "publisher-secret",
    "test-secret",
    "dummy",
    "fake-",
    "example",
    "placeholder",
    "no-key-required",
)

TEXT_EXT = {".md", ".py", ".sh", ".json", ".yaml", ".yml", ".toml", ".txt", ".ps1"}


def parse_frontmatter(text: str) -> dict | None:
    """解析 YAML frontmatter，返回 dict；无 frontmatter 返回 None。"""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fm = m.group(1)
    out: dict[str, str] = {}
    dm = re.search(r"^description:\s*(.*)$", fm, re.M)
    if dm:
        val = dm.group(1).strip()
        if val in (">", ">-", "|", "|-"):
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


def all_skill_files() -> list[Path]:
    return sorted(p for p in REPO.rglob("SKILL.md") if ".git" not in p.parts)


def check_entry_uniqueness(errors: list, warnings: list) -> int:
    files = all_skill_files()
    if not files:
        errors.append("[结构] 找不到入口 SKILL.md")
        return 0
    if len(files) > 1:
        for p in files[1:]:
            rel = p.relative_to(REPO).as_posix()
            errors.append(
                f"[结构] 多余的 SKILL.md：{rel}（宿主会把它注册成独立技能，应改名 MODULE.md）"
            )
    if not (REPO / "SKILL.md").is_file():
        errors.append("[结构] 入口必须放在仓库根目录：SKILL.md")
    return len(files)


def check_families(errors: list, warnings: list) -> int:
    if not REFS.is_dir():
        errors.append("[结构] 缺少 references/ 目录")
        return 0
    present = sorted(d.name for d in REFS.iterdir() if d.is_dir())
    for fam in FAMILIES:
        if fam not in present:
            errors.append(f"[结构] 缺少族目录：references/{fam}/")
        elif not (REFS / fam / "_index.md").is_file():
            warnings.append(f"[结构] references/{fam}/ 缺 _index.md（族级路由）")
    for extra in present:
        if extra not in FAMILIES:
            warnings.append(f"[结构] references/{extra}/ 不属于六族，确认是否有意为之")
    return len([p for p in present if p in FAMILIES])


def check_frontmatter(errors: list, warnings: list) -> int:
    checked = 0
    for p in all_skill_files():
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
    for name in DOCS_WITH_PATHS:
        md = REPO / name
        if not md.is_file():
            warnings.append(f"[文档] 缺少 {name}")
            continue
        text = md.read_text(encoding="utf-8", errors="replace")
        for rel in sorted(set(re.findall(r"`(references/[A-Za-z0-9_\-/\.]+?)`", text))):
            target = rel.rstrip("/")
            if "<" in target or "*" in target:
                continue
            count += 1
            if not (REPO / target).exists():
                errors.append(f"[路径] {name} 引用了不存在的路径：{target}")
    return count


def check_licenses(errors: list, warnings: list) -> int:
    if not (REPO / "LICENSE").exists():
        errors.append("[许可] 仓库根目录缺少 LICENSE 文件")
    count = 0
    for mod in sorted(REFS.rglob("MODULE.md")):
        d = mod.parent
        count += 1
        if any(d.glob("LICENSE*")):
            continue
        # papi-* 这类挂在父模块下的子命令，随父目录的 LICENSE
        if any(d.parent.glob("LICENSE*")):
            warnings.append(
                f"[许可] {d.relative_to(REPO).as_posix()}/ 无独立 LICENSE，沿用父目录"
            )
        else:
            errors.append(f"[许可] {d.relative_to(REPO).as_posix()}/ 缺少 LICENSE")
    return count


def scan_sensitive(errors: list, warnings: list) -> int:
    hits = 0
    allow_dirs = [(REPO / a) for a in PERSONAL_PATH_ALLOWLIST]
    for p in REPO.rglob("*"):
        if not p.is_file() or ".git" in p.parts:
            continue
        if p.suffix.lower() not in TEXT_EXT:
            continue
        if any(d == p or d in p.parents for d in allow_dirs):
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
                if any(x in low for x in FAKE_CREDENTIAL_HINTS):
                    continue
                if any(x in low for x in ("your-", "xxx", "<", "example", "placeholder")):
                    continue
                if "/tests/" in rel or rel.endswith("test_*.py"):
                    warnings.append(f"[疑似测试桩] {rel}：{label}（请人工确认）")
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
    ap = argparse.ArgumentParser(description="校验 lunwenn 仓库结构（v5）")
    ap.add_argument("--strict", action="store_true", help="追加敏感信息扫描")
    ap.add_argument("--json", action="store_true", help="以 JSON 输出结果")
    args = ap.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    n_entries = check_entry_uniqueness(errors, warnings)
    n_fams = check_families(errors, warnings)
    check_frontmatter(errors, warnings)
    n_paths = check_referenced_paths(errors, warnings)
    n_mods = check_licenses(errors, warnings)
    n_sensitive = scan_sensitive(errors, warnings) if args.strict else 0

    result = {
        "entry_files": n_entries,
        "families": n_fams,
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
        print(f"入口 SKILL.md：{n_entries} 个（应恒为 1）")
        print(f"族目录：{n_fams} 个")
        print(f"路径引用：{n_paths} 处")
        print(f"模块（MODULE.md）：{n_mods} 个")
        if args.strict:
            print(f"敏感信息扫描：{n_sensitive} 处命中")
        print()
        if warnings:
            print(f"警告 {len(warnings)} 条：")
            for w in warnings[:30]:
                print(f"  {w}")
            if len(warnings) > 30:
                print(f"  …… 另有 {len(warnings) - 30} 条")
            print()
        if errors:
            print(f"错误 {len(errors)} 条：")
            for e in errors[:30]:
                print(f"  {e}")
            if len(errors) > 30:
                print(f"  …… 另有 {len(errors) - 30} 条")
        else:
            print("✅ 全部检查通过")
        print()
        print("提示：加 --strict 可扫描硬编码凭证与个人路径。")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
