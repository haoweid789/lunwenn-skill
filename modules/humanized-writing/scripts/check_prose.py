#!/usr/bin/env python3
"""检查中英文成稿的硬禁令与模型化形状。只报警，不自动改文。

用法：
    python3 check_prose.py 稿件.md
    cat 稿件.md | python3 check_prose.py -

中文检查：黑话、翻案句、破折号、提示性冒号、模型路标、抒情词、名词化、
句长均匀、排比、借喻堆砌等（改编自 KKKKhazix/human-writing）。
英文检查：破折号（em/en dash）硬禁令 + Tier-1 AI 高频词提示（改编自
blader/humanizer 与 conorbronsdon/avoid-ai-writing）。
"""

from __future__ import annotations

import argparse
import collections
import re
import sys
from dataclasses import dataclass
from pathlib import Path


# ---------------------------------------------------------------------------
# 中文硬禁令词表
# ---------------------------------------------------------------------------

HARD_STOPS = ("说白了", "说穿了", "先说结论")

HARD_JARGON = (
    "赋能", "抓手", "商业闭环", "价值闭环", "能力沉淀", "拉通", "底层逻辑",
    "顶层设计", "认知跃迁", "价值释放", "能力建设", "降本增效", "内容矩阵",
    "全链路", "组合拳", "打开想象空间", "结构性机会", "关键命题", "深层逻辑",
    "技术底座", "公共底座", "技术主权", "单点风险", "主脊柱", "材料锚点",
    "认知增量", "迭代闭环",
)

CONTEXT_JARGON = (
    "沉淀", "颗粒度", "对齐", "协同", "链路", "生态位", "心智", "范式",
    "方法论", "核心变量", "打法", "想象空间", "闭环", "不丢",
)

LYRIC_WORDS = (
    "安放", "抵达", "微光", "褶皱", "丰盈", "滚烫", "轻盈", "赤裸", "剥开",
    "锋利", "坚硬", "柔软",
)

ROAD_SIGNS = (
    "更微妙的是", "还有一层", "只说对了一半", "值得注意的是", "需要指出的是",
    "从某种意义上说",
)

ROAD_STRIP_CHARS = "。！？!? \n"

FORBIDDEN_PUNCTUATION = {
    "：": "中文冒号",
    ":": "英文冒号",
    "—": "破折号",
    "–": "连接号式破折号",
}

PIVOT_PATTERNS = (
    re.compile(r"(?:并)?不是[^。！？\n]{0,90}而是"),
    re.compile(r"并非[^。！？\n]{0,90}而是"),
    re.compile(r"不在于[^。！？\n]{0,90}而在于"),
    re.compile(r"与其说[^。！？\n]{0,90}(?:不如|毋宁|倒不如)"),
    re.compile(r"[。！？!?]\s*而是"),
    re.compile(r"表面(?:上)?[^。！？\n]{0,90}(?:其实|实际|实则)"),
    re.compile(r"看似[^。！？\n]{0,90}(?:其实|实际|实则)"),
)

SEMANTIC_PIVOT_PATTERNS = (
    re.compile(r"(?:总|一直|曾|都)?以为[^！？\n]{2,60}?(?:其实|才发现|才明白|才知道|后来才)"),
    re.compile(r"(?:总|都|一直)以为[^！？\n]{2,60}?[。，](?:可|但|其实)"),
    re.compile(r"回头(?:看|一看)?才(?:发现|明白|知道)"),
    re.compile(r"(?:并)?不是[^。！？\n]{1,40}，(?:更|才)?是[^，。！？\n]"),
    re.compile(r"从来(?:都)?(?:不是|与[^。！？，\n]{1,12}无关)"),
    re.compile(r"答案(?:是否定的|恰恰相反)|恰恰相反"),
    re.compile(r"表面(?:上)?[^！？\n]{0,60}。[^！？\n]{0,12}(?:其实|实际|实则)"),
    re.compile(r"看似[^！？\n]{0,60}。[^！？\n]{0,12}(?:其实|实际|实则)"),
    re.compile(r"[^，。！？\n]{1,12}不重要，(?:重要|要紧)的是"),
    re.compile(r"真正[^，。！？\n]{0,16}的(?:，)?是"),
    re.compile(r"不只(?:是)?[^。！？\n]{0,90}(?:还|也)"),
)

NOMINALIZATION_PATTERNS = (
    re.compile(r"进行(?:了|一次|一场|着)?[^。，！？\n]{0,10}(?:调整|优化|升级|分析|讨论|沟通|梳理|复盘|迭代|探索|尝试|思考|规划|布局)"),
    re.compile(r"实现了?[^。，！？\n]{0,14}的?[^。，！？\n]{0,6}(?:提升|增长|突破|转变|跃升|落地)"),
    re.compile(r"完成了?对[^。，！？\n]{0,16}的"),
    re.compile(r"起到了?[^。，！？\n]{0,12}的?作用"),
    re.compile(r"具有[^。，！？\n]{0,10}(?:意义|价值)"),
)

CONJUNCTIONS = (
    "因为", "所以", "但是", "然而", "同时", "此外", "而且", "并且", "因此", "不仅",
)

ROAD_SIGN_PATTERNS = (
    re.compile(rf"(?:^|[。！？!?]\s*){re.escape(ROAD_SIGNS[0])}[^。！？!?\n]{{0,24}}", re.MULTILINE),
    re.compile(
        rf"(?:^|[。！？!?]\s*){re.escape(ROAD_SIGNS[1])}"
        r"(?=(?:更|原因|问题|意思|考虑|变化|逻辑|价值|作用|风险|影响|值得|很少|不容易|常被|往往))"
        r"[^。！？!?\n]{0,24}", re.MULTILINE),
    *(re.compile(rf"(?:^|[。！？!?]\s*){re.escape(p)}[^。！？!?\n]{{0,24}}", re.MULTILINE)
      for p in ROAD_SIGNS[2:]),
)

SOFT_MARKERS = (
    "真正", "本质上", "更深层次", "归根结底", "换句话说", "不可否认", "核心是",
    "关键在于", "这意味着",
)

REPEATED_OPENERS = (
    "其实", "不过", "当然", "所以", "但是", "后来", "当时", "很多人", "问题是",
    "更重要的是", "说到这里",
)

LEFT_BRANCH_PATTERNS = (
    re.compile(r"(?:^|[。！？]\s*)在[^，。！？\n]{12,70}(?:以后|之后|之前|以前|过程中|情况下|背景下)，"),
    re.compile(r"(?:^|[。！？]\s*)那些[^，。！？\n]{10,60}的[^，。！？\n]{2,30}[，。]"),
    re.compile(r"(?:^|[。！？]\s*)(?:真正|最终|最后)让[^，。！？\n]{8,70}的，是"),
)

METAPHOR_FIELDS = {
    "温度": ("降温", "升温", "冷却", "余温", "温度最高"),
    "生死战争": ("杀死", "死因", "枪响", "开火", "战场", "引爆", "弹药"),
    "建筑灾害": ("坍塌", "崩塌", "地基", "砖头", "支柱", "废墟"),
    "仓储租赁": ("仓库", "库房", "租金", "取货", "入库", "库存"),
    "道路竞赛": ("赛道", "跑道", "岔路", "十字路口", "终点线", "门票"),
    "机器器官": ("齿轮", "引擎", "发动机", "血管", "骨架", "肌肉"),
    "海洋航行": ("蓝海", "浪潮", "潮水", "航船", "灯塔", "彼岸"),
}


# ---------------------------------------------------------------------------
# 英文检查词表（Tier-1 高频词，需结合语境判断；不证明来自 AI）
# ---------------------------------------------------------------------------

EN_AI_WORDS = (
    "delve", "leverage", "robust", "seamless", "tapestry", "testament", "pivotal",
    "meticulous", "showcasing", "nuanced", "transformative", "ecosystem", "realm",
    "paradigm", "landscape", "holistic", "impactful", "vibrant", "thriving", "nestled",
    "embark", "beacon", "underscores", "intricate", "comprehensive", "cutting-edge",
    "game-changer", "unpack", "bustling", "ever-evolving", "enduring", "synergy",
    "interplay", "genuinely", "actionable", "empower", "foster", "unleash", "streamline",
    "catalyze", "galvanize", "juxtapose", "quintessential", "paramount", "burgeoning",
    "nascent", "overarching", "utilize", "commence", "ascertain", "endeavor",
)

EN_NOT_BUT = re.compile(
    r"\bnot (just |merely |only |simply )?(\w+\s+){0,3}but\b", re.IGNORECASE
)


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

@dataclass
class Paragraph:
    position: int
    text: str
    han: int
    sentences: int


def han_count(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def line_number(text: str, position: int) -> int:
    return text.count("\n", 0, position) + 1


def excerpt(value: str, width: int = 72) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    return value if len(value) <= width else value[: width - 1] + "…"


def mask_non_prose(text: str) -> str:
    """屏蔽代码、网址和机器元数据，同时保留字符位置与换行。"""

    def mask(match: re.Match[str]) -> str:
        return "".join("\n" if char == "\n" else " " for char in match.group())

    patterns = (
        re.compile(r"\A---\s*\n.*?\n---\s*(?:\n|\Z)", re.DOTALL),
        re.compile(r"```.*?```", re.DOTALL),
        re.compile(r"`[^`\n]*`"),
        re.compile(r"\]\([^\n)]*\)"),
        re.compile(r"https?://[^\s)>]+"),
        re.compile(r"<[^>\n]+>"),
    )
    masked = text
    for pattern in patterns:
        masked = pattern.sub(mask, masked)
    return masked


def non_overlapping_terms(text: str, terms: tuple[str, ...]):
    matches = []
    occupied = []
    for term in sorted(terms, key=len, reverse=True):
        for match in re.finditer(re.escape(term), text):
            start, end = match.span()
            if any(start < old_end and end > old_start for old_start, old_end in occupied):
                continue
            matches.append((start, term))
            occupied.append((start, end))
    return sorted(matches)


def all_matches(text: str, patterns: tuple[re.Pattern[str], ...]):
    matches = []
    for pattern in patterns:
        matches.extend(pattern.finditer(text))
    return sorted(matches, key=lambda match: match.start())


def heavy_de_sentences(text: str):
    matches = []
    pattern = re.compile(r"[^。！？!?\n]+(?:[。！？!?]|$)")
    for match in pattern.finditer(text):
        value = match.group()
        if han_count(value) >= 38 and value.count("的") >= 4:
            matches.append(match)
    return matches


def anaphora_runs(text: str, minimum: int = 3):
    matches = []
    for sentence in re.finditer(r"[^。！？!?\n]+(?:[。！？!?]|$)", text):
        clauses = [
            clause.strip()
            for clause in re.split(r"[，、；,;]", sentence.group())
            if han_count(clause) >= 3
        ]
        if len(clauses) < minimum:
            continue
        run = 1
        for previous, current in zip(clauses, clauses[1:]):
            if previous[:2] == current[:2] and re.match(r"[一-鿿]{2}", current):
                run += 1
                if run >= minimum:
                    matches.append(sentence)
                    break
            else:
                run = 1
    return matches


def sentence_length_cv(text: str):
    lengths = [
        han_count(match.group())
        for match in re.finditer(r"[^。！？!?\n]+[。！？!?]", text)
        if han_count(match.group()) >= 4
    ]
    if len(lengths) < 12:
        return None
    mean = sum(lengths) / len(lengths)
    if mean == 0:
        return None
    variance = sum((value - mean) ** 2 for value in lengths) / len(lengths)
    return (variance ** 0.5) / mean, len(lengths)


def bracket_highlights(text: str):
    return list(re.finditer(r"[「『][^」』\n]{1,6}[」』]", text))


def prose_paragraphs(text: str) -> list[Paragraph]:
    paragraphs = []
    cursor = 0
    for block in re.split(r"\n\s*\n", text):
        position = text.find(block, cursor)
        cursor = max(position + len(block), cursor)
        clean = re.sub(r"[>*_`]", "", block).strip()
        if not clean or clean.startswith(("#", "http", "![", "```")):
            continue
        if re.match(r"^(?:[-+*]|\d+[.、])\s", clean):
            continue
        count = han_count(clean)
        if count < 4:
            continue
        sentences = max(1, len(re.findall(r"[。！？!?]", clean)))
        paragraphs.append(Paragraph(position, clean, count, sentences))
    return paragraphs


def metaphor_cluster(text: str, distance: int = 800):
    hits = []
    for field, words in METAPHOR_FIELDS.items():
        for word in words:
            for match in re.finditer(re.escape(word), text):
                hits.append((match.start(), field, word))
    hits.sort()
    for index, (start, _, _) in enumerate(hits):
        window = [hit for hit in hits[index:] if hit[0] - start <= distance]
        fields = {hit[1] for hit in window}
        if len(fields) >= 3:
            return window, fields
    return None


def short_streak(paragraphs: list[Paragraph], limit: int = 4):
    streak = []
    for paragraph in paragraphs:
        if paragraph.han <= 24 and paragraph.sentences <= 1:
            streak.append(paragraph)
            if len(streak) >= limit:
                return streak
        else:
            streak = []
    return None


def opener_counts(paragraphs: list[Paragraph]):
    counts = collections.Counter()
    examples = {}
    for paragraph in paragraphs:
        value = paragraph.text.lstrip("“‘\"（(")
        for opener in REPEATED_OPENERS:
            if value.startswith(opener):
                counts[opener] += 1
                examples.setdefault(opener, paragraph.position)
                break
    return counts, examples


def read_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# 中文检查
# ---------------------------------------------------------------------------

def chinese_pass(prose: str, text: str, total_han: int, failures, warnings):
    quote_colons = []
    for symbol, label in FORBIDDEN_PUNCTUATION.items():
        matches = list(re.finditer(re.escape(symbol), prose))
        if symbol in ("：", ":"):
            hard = []
            for match in matches:
                tail = prose[match.end(): match.end() + 2].lstrip()
                if tail[:1] in ("「", "『", "“", "‘", '"'):
                    quote_colons.append(match)
                else:
                    hard.append(match)
            matches = hard
        if matches:
            lines = "、".join(str(line_number(text, m.start())) for m in matches[:8])
            failures.append(f"{label}共 {len(matches)} 处，出现在第 {lines} 行。")
    if quote_colons:
        lines = "、".join(str(line_number(text, m.start())) for m in quote_colons[:8])
        warnings.append(
            f"引出原话的冒号 {len(quote_colons)} 处，第 {lines} 行。"
            "确认引号里确实是原话，且不是提示性用法。"
        )

    for position, phrase in non_overlapping_terms(prose, HARD_STOPS):
        failures.append(f"硬停词，第 {line_number(text, position)} 行，{phrase}")
    for position, phrase in non_overlapping_terms(prose, HARD_JARGON):
        failures.append(f"黑话，第 {line_number(text, position)} 行，{phrase}")

    context_jargon = non_overlapping_terms(prose, CONTEXT_JARGON)
    hard_spans = [(p, p + len(ph)) for p, ph in non_overlapping_terms(prose, HARD_JARGON)]
    context_jargon = [
        (p, ph) for p, ph in context_jargon
        if not any(p < e and p + len(ph) > s for s, e in hard_spans)
    ]
    if context_jargon:
        samples = "、".join(dict.fromkeys(ph for _, ph in context_jargon))
        lines = "、".join(dict.fromkeys(str(line_number(text, p)) for p, _ in context_jargon[:8]))
        warnings.append(
            f"有 {len(context_jargon)} 处词语需结合语境判断。第 {lines} 行出现 {samples}。"
            "本义准确时保留，用来抬价时改写。"
        )

    for match in all_matches(prose, ROAD_SIGN_PATTERNS):
        failures.append(
            f"模型路标，第 {line_number(text, match.start())} 行，"
            f"“{excerpt(match.group().lstrip(ROAD_STRIP_CHARS))}”"
        )

    pivots = all_matches(prose, PIVOT_PATTERNS)
    for match in pivots:
        failures.append(
            f"禁用翻案句，第 {line_number(text, match.start())} 行，"
            f"“{excerpt(match.group())}”"
        )
    occupied_spans = [m.span() for m in pivots]
    semantic_pivots = []
    for match in all_matches(prose, SEMANTIC_PIVOT_PATTERNS):
        if any(match.start() < e and match.end() > s for s, e in occupied_spans):
            continue
        semantic_pivots.append(match)
        occupied_spans.append(match.span())
    for match in semantic_pivots:
        warnings.append(
            f"疑似翻案腔变形，第 {line_number(text, match.start())} 行，"
            f"“{excerpt(match.group(), 44)}”。先立误解再推翻就改成正面陈述，正常用法保留。"
        )

    for match in anaphora_runs(prose)[:4]:
        warnings.append(
            f"三连以上同构排比，第 {line_number(text, match.start())} 行，"
            f"“{excerpt(match.group(), 44)}”。留两项，第三项换说法或删掉。"
        )

    lyric = non_overlapping_terms(prose, LYRIC_WORDS)
    if len(lyric) >= 2:
        samples = "、".join(dict.fromkeys(t for _, t in lyric))
        warnings.append(
            f"模型偏爱抒情词 {len(lyric)} 处。{samples}。"
            "写具体事物时保留，给抽象概念穿衣服时删掉。"
        )

    for match in all_matches(prose, NOMINALIZATION_PATTERNS)[:4]:
        warnings.append(
            f"名词化句式，第 {line_number(text, match.start())} 行，"
            f"“{excerpt(match.group(), 36)}”。还原成直接的动词。"
        )

    conj_hits = non_overlapping_terms(prose, CONJUNCTIONS)
    if total_han >= 600 and len(conj_hits) * 1000 / total_han > 7:
        samples = "、".join(
            f"{t} {c} 次" for t, c in collections.Counter(t for _, t in conj_hits).most_common(4)
        )
        warnings.append(
            f"连词密度偏高，每千字 {len(conj_hits) * 1000 // total_han} 个。{samples}。"
            "中文小句靠语序和事理相接，删掉一半试试。"
        )

    highlights = bracket_highlights(prose)
    if len(highlights) > max(3, total_han // 700):
        samples = "、".join(dict.fromkeys(m.group() for m in highlights[:6]))
        warnings.append(f"「」括起短语共 {len(highlights)} 处。{samples}。太密说明在批量造金句。")

    cv = sentence_length_cv(prose)
    if cv and cv[0] < 0.42:
        warnings.append(
            f"全文 {cv[1]} 个句子长度过于接近（变异系数 {cv[0]:.2f}）。"
            "放开几句，压短几句。"
        )

    marker = non_overlapping_terms(prose, SOFT_MARKERS)
    if len(marker) > max(2, total_han // 900):
        samples = "、".join(dict.fromkeys(t for _, t in marker))
        warnings.append(f"洞察路标共 {len(marker)} 处，重点检查 {samples}。")

    left = all_matches(prose, LEFT_BRANCH_PATTERNS)
    if len(left) > max(2, total_han // 1200):
        samples = "；".join(
            f"第 {line_number(text, m.start())} 行“{excerpt(m.group(), 44)}”" for m in left[:4]
        )
        warnings.append(f"长前置成分共 {len(left)} 处，可能让主干来得太晚。{samples}")

    dense_de = heavy_de_sentences(prose)
    if len(dense_de) > max(1, total_han // 1500):
        samples = "；".join(
            f"第 {line_number(text, m.start())} 行“{excerpt(m.group(), 44)}”" for m in dense_de[:4]
        )
        warnings.append(f"有 {len(dense_de)} 个长句含四个以上“的”。{samples}")

    paragraphs = prose_paragraphs(prose)
    if len(paragraphs) >= 10:
        one_sentence = sum(p.sentences <= 1 for p in paragraphs)
        ratio = one_sentence / len(paragraphs)
        if ratio >= 0.75:
            warnings.append(f"可识别段落中有 {ratio:.0%} 只有一句话，可能形成统一短段鼓点。")
    streak = short_streak(paragraphs)
    if streak:
        warnings.append(
            f"从第 {line_number(text, streak[0].position)} 行起连续 {len(streak)} 个短促单句段，"
            "检查是否在排队喊结论。"
        )
    counts, opener_ex = opener_counts(paragraphs)
    repeated = [(o, c) for o, c in counts.items() if c >= 4]
    if repeated:
        details = "、".join(f"{o} {c} 次" for o, c in repeated)
        first = min(opener_ex[o] for o, _ in repeated)
        warnings.append(f"段落开场重复，从第 {line_number(text, first)} 行附近。{details}。")
    metaphors = metaphor_cluster(prose)
    if metaphors:
        window, fields = metaphors
        samples = "、".join(dict.fromkeys(h[2] for h in window))
        warnings.append(f"八百字内出现 {len(fields)} 套借喻。{'、'.join(sorted(fields))}。例词 {samples}。")


# ---------------------------------------------------------------------------
# 英文检查
# ---------------------------------------------------------------------------

def english_pass(prose: str, text: str, failures, warnings):
    # em dash 硬禁令（除非作者样本用，由调用方判断）
    em = list(re.finditer(r"—", prose))
    if em:
        lines = "、".join(str(line_number(text, m.start())) for m in em[:8])
        failures.append(f"英文破折号 em dash 共 {len(em)} 处，第 {lines} 行。改写掉（除非作者样本用）。")

    # en dash：数字范围（如 2020–2023）保留，作连接词时提示
    en_word = list(re.finditer(r"(?<!\d)–(?!\d)", prose))
    if en_word:
        lines = "、".join(str(line_number(text, m.start())) for m in en_word[:8])
        warnings.append(f"连接号式 en dash 共 {len(en_word)} 处，第 {lines} 行。数字范围外建议改写。")

    # Tier-1 高频词（整词匹配，大小写不敏感）；作为需语境判断提示
    hits = []
    for word in EN_AI_WORDS:
        for m in re.finditer(rf"\b{re.escape(word)}\b", prose, re.IGNORECASE):
            hits.append((m.start(), word))
    if hits:
        by_word = collections.Counter(w for _, w in hits)
        samples = "、".join(f"{w}({c})" for w, c in by_word.most_common(8))
        warnings.append(
            f"英文 Tier-1 高频词共 {len(hits)} 处：{samples}。"
            "结合语境替换为朴实词（见 ai-vocab.md）；技术本义或作者样本用法保留。"
        )

    # Not X but Y 桥接（需语境判断）
    nb = list(EN_NOT_BUT.finditer(prose))
    if nb:
        lines = "、".join(str(line_number(text, m.start())) for m in nb[:6])
        warnings.append(
            f"“not … but …”桥接共 {len(nb)} 处，第 {lines} 行。"
            "可直接正面陈述；只有纠正读者真实误解或两半都带信息时才保留。"
        )


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="检查中英文成稿的硬禁令与模型化形状")
    parser.add_argument("path", help="Markdown 或文本文件路径。使用 - 从标准输入读取")
    args = parser.parse_args()

    try:
        text = read_text(args.path)
    except (OSError, UnicodeError) as error:
        print(f"无法读取稿件。{error}", file=sys.stderr)
        return 2

    prose = mask_non_prose(text)
    total_han = han_count(prose)
    failures: list[str] = []
    warnings: list[str] = []

    if total_han > 0:
        chinese_pass(prose, text, total_han, failures, warnings)
    english_pass(prose, text, failures, warnings)

    print(f"汉字数 {total_han}")
    if failures:
        print("\n需要修改")
        for item in failures:
            print(f"- {item}")
    if warnings:
        print("\n需要人工判断")
        for item in warnings:
            print(f"- {item}")
    if not failures and not warnings:
        print("\n未发现这份检查器覆盖的问题。")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
