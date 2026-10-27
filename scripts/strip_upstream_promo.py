#!/usr/bin/env python3
"""移除 cell-suite 上游副本中的推广话术。

上游 Cell 项目在其 SKILL.md 中要求输出面向作者社交账号的推广行（如
「感谢抖音：木纹」）。这些是上游作者的营销约定，不属于 MIT 许可要求，
本仓库统一不输出。本脚本用于把推广文本从副本中**物理删除**。

用法::

    python scripts/strip_upstream_promo.py            # 预览将要改动的文件
    python scripts/strip_upstream_promo.py --apply    # 实际写入

注意：执行 --apply 后，本目录不再与上游逐字节一致，
`SOURCES.md` 中「只读副本」的描述将不再适用，建议在提交信息中说明。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# 脚本位于 <repo>/scripts/，模块副本位于 <repo>/references/4-figures/
REPO = Path(__file__).resolve().parent.parent
SU7 = REPO / "references" / "4-figures" / "reconstruct-su7"
SU8 = REPO / "references" / "4-figures" / "reconstruct-su7" / "sub" / "cell_su8"

# 目标文件 → 待移除的**行内片段**（只删片段本身，保留该行其余业务规则）
TARGETS: dict[tuple[Path, str], list[str]] = {
    # 原 cell_su7 → 4-figures/reconstruct-su7
    (SU7, "MODULE.md"): [
        "感谢小红书：木纹小路。",
    ],
    # 原 cell_su8 → 4-figures/reconstruct-su7/sub/cell_su8
    (SU8, "MODULE.md"): [
        "感谢小红书：木纹小路。",
    ],
}

# workflow.md 中的充值引导整行替换
REPLACEMENTS: dict[tuple[Path, str], list[tuple[str, str]]] = {
    (SU7, "references/workflow.md"): [
        (
            "`当前额度不足，请在小红书搜索“木纹小路”（约200个粉丝的小博主）获取充值。兄弟们，小红书不要谈论梯子等敏感话题；有问题请私信抖音“木纹”（约900个粉丝的小博主）。`",
            "`当前额度不足。请检查账户余额，或改用本地绘图方案（references/4-figures/data-figure/），该方案不消耗额度。`",
        ),
    ],
    (SU8, "references/workflow.md"): [
        (
            "`当前额度不足，请在小红书搜索“木纹小路”（约200个粉丝的小博主）获取充值。兄弟们，小红书不要谈论梯子等敏感话题；有问题请私信抖音“木纹”（约900个粉丝的小博主）。`",
            "`当前额度不足。请检查账户余额，或改用本地绘图方案（references/4-figures/data-figure/），该方案不消耗额度。`",
        ),
    ],
}


def collect() -> tuple[list[tuple[Path, list[str], str]], list[Path]]:
    """返回 (待删除整行, 待替换) 计划与缺失文件列表。"""
    deletions: list[tuple[Path, list[str], str]] = []
    missing: list[Path] = []

    for (base, rel), needles in TARGETS.items():
        path = base / rel
        if not path.is_file():
            missing.append(path)
            continue
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        hit = [ln for ln in lines if any(n in ln for n in needles)]
        if hit:
            deletions.append((path, hit, "删除推广行"))

    for (base, rel), pairs in REPLACEMENTS.items():
        path = base / rel
        if not path.is_file():
            missing.append(path)
            continue
        text = path.read_text(encoding="utf-8")
        hit = [old for old, _ in pairs if old in text]
        if hit:
            deletions.append((path, hit, "替换充值引导"))

    return deletions, missing


def apply_changes() -> int:
    deletions, missing = collect()
    for path in missing:
        print(f"[warn] 文件不存在，跳过：{path.relative_to(CELL_SUITE)}")

    changed = 0
    for path, hits, action in deletions:
        text = path.read_text(encoding="utf-8")
        original = text
        rel = str(path.relative_to(CELL_SUITE)).replace("\\", "/")
        if action == "删除推广行":
            for needle in hits:
                text = text.replace(needle, "")
        else:
            for old, new in REPLACEMENTS.get(rel, []):
                if old in hits:
                    text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")
            print(f"[ok] {action}：{path.relative_to(CELL_SUITE)}")
            changed += 1

    if not changed:
        print("没有发现需要处理的推广文本（可能已清理过）。")
    else:
        print(f"\n完成，共改动 {changed} 个文件。")
        print("提示：执行后本目录不再与上游逐字节一致，")
        print("      请在提交信息中说明，并同步更新 SOURCES.md 的相关描述。")
    return 0


def preview() -> int:
    deletions, missing = collect()
    for path in missing:
        print(f"[warn] 文件不存在，跳过：{path.relative_to(CELL_SUITE)}")

    if not deletions:
        print("未发现推广文本，无需处理。")
        return 0

    print("以下文件含推广话术（未改动，加 --apply 执行）：\n")
    for path, hits, action in deletions:
        rel = path.relative_to(CELL_SUITE)
        print(f"  {rel}  ({action})")
        for h in hits:
            preview = h.strip()
            if len(preview) > 90:
                preview = preview[:87] + "..."
            print(f"      - {preview}")
    print(f"\n共 {len(deletions)} 个文件待处理。加 --apply 执行写入。")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="移除 cell-suite 上游副本中的推广话术"
    )
    ap.add_argument(
        "--apply",
        action="store_true",
        help="实际写入修改（默认仅预览）",
    )
    args = ap.parse_args()
    return apply_changes() if args.apply else preview()


if __name__ == "__main__":
    sys.exit(main())
